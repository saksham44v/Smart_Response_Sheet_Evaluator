import json
import os
from jee_main_question_scrap import extract_image_data_with_subject

def update_question_data(url, question_data_path="question_data.json"):
    # Load existing data if exists
    if os.path.exists(question_data_path):
        try:  # Try to load JSON data
            with open(question_data_path, "r") as f:
                question_data = json.load(f)
        except json.JSONDecodeError:  # Handle empty or invalid JSON
            question_data = {}  # Initialize with an empty dictionary
    else:
        question_data = {}

    extracted = extract_image_data_with_subject(url)
    if not extracted:
        print("No data extracted.")
        return

    exam_date = extracted["exam_date"]
    slot_time = extracted["slot_time"]
    question_map = extracted["questions"]

    if exam_date not in question_data:
        question_data[exam_date] = {}

    # Replace existing slot_time data
    question_data[exam_date][slot_time] = question_map

    # Save updated data
    with open(question_data_path, "w") as f:
        json.dump(question_data, f, indent=2)

    print(f"Updated question data for {exam_date} - {slot_time} ✅")



#just paste the link of the url here and everything will be handleshd tehn
url="https://cdn3.digialm.com//per/g28/pub/2083/touchstone/AssessmentQPHTMLMode1//2083O2581/2083O2581S2D29464/1743762910852900/UK01201339_2083O2581S2D29464E1.html"
update_question_data(url, "question_tagging_logic\question_data.json")