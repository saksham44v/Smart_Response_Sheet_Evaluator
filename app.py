# from flask import Flask, render_template, request, jsonify
# from flask_cors import CORS
# from scrape import scrape_response_sheet
# from answer_key import ANSWER_KEY
# from evaluate import evaluate_responses

# app = Flask(__name__)
# CORS(app)

# @app.route("/")
# def home():
#     return render_template("home.html")

# @app.route("/evaluate", methods=["POST"])
# def evaluate():
#     data = request.json
#     response_url = data.get("response_url")

#     if not response_url:
#         return jsonify({"error": "No URL provided"}), 400

#     # Scrape response sheet
#     scraped_data = scrape_response_sheet(response_url)

#     if not scraped_data:
#         return jsonify({"error": "Failed to process response sheet"}), 500

#     exam_date = scraped_data["exam_date"]
#     slot_time = scraped_data["slot_time"]

#     # Check if answer key exists
#     if exam_date not in ANSWER_KEY or slot_time not in ANSWER_KEY[exam_date]:
#         return jsonify({"error": "Answer key not found for this date & slot"}), 500

#     correct_answers = ANSWER_KEY[exam_date][slot_time]

#     # Evaluate responses
#     result = evaluate_responses(scraped_data["questions"], correct_answers)

#     return jsonify({
#         "total_marks": result["total_marks"],
#         "correct": result["correct"],
#         "incorrect": result["incorrect"],
#         "unattempted": result["unattempted"],
#         "subject_scores": result["subject_scores"],
#         "subject_questions": result["subject_questions"],
#         "exam_date": exam_date,
#         "slot_time": slot_time
#     })

# if __name__ == "__main__":
#     app.run(host='0.0.0.0',debug=True)


# from flask import Flask, render_template

# app = Flask(__name__)

# @app.route("/")
# def home():
#     return render_template("home_page.html")

# @app.route("/jee-mains")
# def jee_mains():
#     return render_template("jee_main_homepage.html")

# @app.route("/gate")
# def gate():
#     return render_template("gate_home.html")



# if __name__ == "__main__":
#     app.run(host='0.0.0.0', port=5000, debug=True)






from flask import Flask, render_template, request,jsonify
import json
import traceback,logging

from evaluate import evaluate_responses  # Your evaluation logic
from scrape import scrape_response_sheet  # Your scraping logic


from gate_evaluation import evaluate_gate_responses  # Your evaluation logic
from gate_scrape import scrape_gate_response_sheet
from gate_answer_keys import answer
from jee_topics import topics

app = Flask(__name__)
app.secret_key = 'your_secret_key'

# Load correct answers
try:
    from answer_key import correct_answers
except ImportError:
    correct_answers = {}

@app.route("/")
def home():
    return render_template("home_page.html")


@app.route('/jee_main')
def jee_main():
    return render_template('jee_main_homepage.html')



@app.route("/jee-mains", methods=["GET", "POST"])
def jee_mains():
    if request.method == "POST":
        response_sheet_url = request.form.get("response_sheet_url")

        if not response_sheet_url:
            return jsonify({"error": "No URL provided"}), 400

        try:
            scraped_data = scrape_response_sheet(response_sheet_url)
        except Exception as e:
            print(f"Scraping error: {e}")
            return jsonify({"error": "Failed to scrape response sheet. Please check the URL and try again."}), 400

        if scraped_data is None:
            return jsonify({"error": "Invalid or broken URL."}), 400

        questions = scraped_data["questions"]
        exam_date = scraped_data["exam_date"]
        exam_slot = scraped_data["slot_time"]
        if exam_date not in correct_answers:
           return jsonify({"error": f"No answer key found for exam date {exam_date}."}), 400

        if exam_slot not in correct_answers[exam_date]:
           return jsonify({"error": f"No answer key found for exam slot {exam_slot}."}), 400

        #print(questions[0])

        evaluation_result = evaluate_responses(questions, correct_answers[exam_date][exam_slot])
        # /print(evaluation_result,exam_date,exam_slot)
        # print(questions)
        print(evaluation_result)
        # Return evaluated results as HTML string
        rendered = render_template("jee_main_results.html",
                                   result=evaluation_result,
                                   exam_date=exam_date,
                                   exam_slot=exam_slot,
                                   questions=questions,
                                   answers=correct_answers[exam_date][exam_slot]
                                   ,topics=topics[exam_date][exam_slot])

        return rendered  # Sending back the HTML directly

    return render_template("jee_main_homepage.html")


@app.route("/gate")
def gate():
    return render_template("gate_home.html")



@app.route("/gatee", methods=["GET", "POST"])
def gate_evaluation_route():
    """
    Handles the GATE evaluation request.
    """
    if request.method == "POST":
        response_sheet_url = request.form.get("response_sheet_url")

        if not response_sheet_url:
            return jsonify({"error": "No URL provided"}), 400

        try:
            scraped_data = scrape_gate_response_sheet(response_sheet_url)
        except Exception as e:
            print(f"Scraping error: {e}")
            return jsonify({"error": "Failed to scrape response sheet. Please check the URL and try again."}), 400

        if scraped_data is None:
            return jsonify({"error": "Invalid or broken URL."}), 400

        questions = scraped_data["questions"]
        exam_date = scraped_data["exam_date"]
        exam_slot = scraped_data["slot_time"]

        # if exam_date not in correct_answers:
        #     return jsonify({"error": f"No answer key found for exam date {exam_date}."}), 400
        # if exam_slot not in correct_answers[exam_date]:
        #     return jsonify({"error": f"No answer key found for exam slot {exam_slot}."}), 400

        try:
            evaluation_result = evaluate_gate_responses(questions, answer)
            print(evaluation_result)
            renderedd=render_template("gate_results.html", result=evaluation_result,questions=questions,answers=answer) # added template
            return renderedd
        except Exception as e:
            msg = f"Evaluation error: {e}\n{traceback.format_exc()}"
            logging.error(msg)
            return jsonify({"error": "Failed to evaluate responses: " + str(e)}), 500

    return render_template("gate_home.html")  #  create a form

if __name__ == "__main__":
    app.run(host='0.0.0.0', port=5000, debug=True)
