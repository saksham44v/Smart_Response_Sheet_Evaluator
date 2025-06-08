# import requests
# from bs4 import BeautifulSoup

# def scrape_response_sheet(url):
#     """
#     Scrapes the JEE Mains response sheet, extracts questions, subjects, and student responses.
#     """
#     headers = {
#         "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/91.0.4472.124 Safari/537.36"
#     }

#     response = requests.get(url, headers=headers)
#     if response.status_code != 200:
#         return None

#     soup = BeautifulSoup(response.text, "html.parser")

#     # Save the scraped HTML for debugging
#     with open("scraped_page.html", "w", encoding="utf-8") as file:
#         file.write(str(soup))

#     # Extract Exam Date & Slot
#     exam_date = soup.find("td", string="Test Date").find_next_sibling("td").text.strip()
#     exam_time = soup.find("td", string="Test Time").find_next_sibling("td").text.strip()
#     exam_slot = exam_time.split("-")[0].strip()

#     questions = []
#     current_subject = None  # Track subject based on section headers

#     # Iterate through all elements in the response sheet
#     for element in soup.find_all(["span", "div"], class_=["bold", "question-pnl"]):
#         # Detect section headers (Physics, Chemistry, Mathematics) and merge Section A & B
#         if element.name == "span" and "Section" in element.text:
#             if "Physics" in element.text:
#                 current_subject = "Physics"
#             elif "Chemistry" in element.text:
#                 current_subject = "Chemistry"
#             elif "Mathematics" in element.text:
#                 current_subject = "Mathematics"

#         # Detect question panels
#         elif element.name == "div" and "question-pnl" in element.get("class", []):
#             q_id = element.find("td", string="Question ID :").find_next_sibling("td").text.strip()
#             q_type = element.find("td", string="Question Type :").find_next_sibling("td").text.strip()
#             status = element.find("td", string="Status :").find_next_sibling("td").text.strip()

#             if q_type == "MCQ":
#                 chosen_option = element.find("td", string="Chosen Option :").find_next_sibling("td").text.strip()
#                 option_ids = [element.find("td", string=f"Option {i} ID :").find_next_sibling("td").text.strip() for i in range(1, 5)]

#                 questions.append({
#                     "question_id": q_id,
#                     "question_type": q_type,
#                     "subject": current_subject,  # Assign question to detected subject
#                     "option_ids": option_ids,
#                     "chosen_option": chosen_option if status == "Answered" else "--",
#                     "status": status
#                 })
#             elif q_type == "SA":
#                 given_answer = element.find("td", string="Given Answer :").find_next_sibling("td").text.strip()
#                 questions.append({
#                     "question_id": q_id,
#                     "question_type": q_type,
#                     "subject": current_subject,  # Assign question to detected subject
#                     "given_answer": given_answer if status == "Answered" else "--",
#                     "status": status
#                 })

#     return {"exam_date": exam_date, "slot_time": exam_slot, "questions": questions}


import requests
from bs4 import BeautifulSoup
import json

def scrape_response_sheet(url, config_path="config.json"):
    """
    Scrapes the JEE Mains response sheet, extracts questions, subjects, and student responses,
    including image URLs for questions and options.
    """
    headers = {
        "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/91.0.4472.124 Safari/537.36"
    }

    try:
        response = requests.get(url, headers=headers)
        response.raise_for_status()
    except requests.exceptions.RequestException as e:
        print(f"Error fetching URL: {e}")
        return None

    soup = BeautifulSoup(response.text, "html.parser")

    try:
        with open(config_path, "r") as f:
            config = json.load(f)
    except (FileNotFoundError, json.JSONDecodeError) as e:
        print(f"Error loading or parsing config file: {e}. Using default selectors.")
        config = {}

    with open("scraped_page.html", "w", encoding="utf-8") as file:
        file.write(str(soup))

    exam_date_selector = config.get("exam_date_selector", "td:contains('Test Date') + td")
    exam_time_selector = config.get("exam_time_selector", "td:contains('Test Time') + td")

    try:
        exam_date = soup.select_one(exam_date_selector).text.strip()
        exam_time = soup.select_one(exam_time_selector).text.strip()
        exam_slot = exam_time.split("-")[0].strip()
    except AttributeError:
        print("Error extracting exam date/time. HTML structure may have changed.")
        exam_date = "N/A"
        exam_slot = "N/A"

    questions = []
    current_subject = None

    for element in soup.find_all(["span", "div"]):
        if element.name == "span" and "Section" in element.text:
            if "Physics" in element.text:
                current_subject = "Physics"
            elif "Chemistry" in element.text:
                current_subject = "Chemistry"
            elif "Mathematics" in element.text:
                current_subject = "Mathematics"

        elif element.name == "div" and "question-pnl" in element.get("class", []):
            # Selectors
            q_id_selector = config.get("question_id_selector", "td:contains('Question ID :') + td")
            q_type_selector = config.get("question_type_selector", "td:contains('Question Type :') + td")
            status_selector = config.get("status_selector", "td:contains('Status :') + td")
            chosen_option_selector = config.get("chosen_option_selector", "td:contains('Chosen Option :') + td")
            given_answer_selector = config.get("given_answer_selector", "td:contains('Given Answer :') + td")
            question_image_selector = config.get("question_image_selector", "img[name]")

            try:
                q_id = element.select_one(q_id_selector).text.strip()
                q_type = element.select_one(q_type_selector).text.strip()
                status = element.select_one(status_selector).text.strip()
            except AttributeError:
                print(f"Error extracting question data. HTML structure may have changed for question block.")
                continue

            question_image_element = element.select_one(question_image_selector)
            question_image_url = question_image_element.get("src") if question_image_element else None

            if q_type == "MCQ":
                try:
                    chosen_option = element.select_one(chosen_option_selector).text.strip() if status == "Answered" else "--"

                    # Extract option IDs
                    option_ids = []
                    for i in range(1, 5):
                        option_selector = config.get(f"option_{i}_id_selector", f"td:contains('Option {i} ID :') + td")
                        option_element = element.select_one(option_selector)
                        option_id = option_element.text.strip() if option_element else "N/A"
                        option_ids.append(option_id)

                    # # Extract option image URLs
                    # question_image_name = question_image_element.get("name") if question_image_element else ""
                    # question_prefix = question_image_name.rsplit("_q", 1)[0] if "_q" in question_image_name else ""

                    # option_image_elements = element.select("img[name]")
                    # option_image_urls = []

                    # for i in range(1, 5):
                    #     expected_suffix = f"_o{i}.jpg"
                    #     option_img = next(
                    #         (img for img in option_image_elements if img.get("name", "").startswith(question_prefix) and img.get("name", "").endswith(expected_suffix)),
                    #         None
                    #     )
                    #     option_image_urls.append(option_img.get("src") if option_img else None)
                    image_elements = element.select("img[name]")

                    # Question image is assumed to be the first image
                    question_image_url = image_elements[0].get("src") if image_elements else None
                    
                    # Option image URLs are the rest
                    option_image_urls = [img.get("src") for img in image_elements[1:5]]  # Get up to 4 options


                    questions.append({
                        "question_id": q_id,
                        "question_type": q_type,
                        "subject": current_subject,
                        "option_ids": option_ids,
                        "chosen_option": chosen_option,
                        "status": status,
                        "question_image_url": question_image_url,
                        "option_image_urls": option_image_urls
                    })
                except AttributeError:
                    print(f"Error extracting MCQ data. HTML structure may have changed for question: {q_id}")
                    continue

            elif q_type == "SA":
                try:
                    given_answer = element.select_one(given_answer_selector).text.strip() if status == "Answered" else "--"
                    questions.append({
                        "question_id": q_id,
                        "question_type": q_type,
                        "subject": current_subject,
                        "given_answer": given_answer,
                        "status": status,
                        "question_image_url": question_image_url
                    })
                except AttributeError:
                    print(f"Error extracting SA data. HTML structure may have changed for question: {q_id}")
                    continue

    return {
        "exam_date": exam_date,
        "slot_time": exam_slot,
        "questions": questions
    }
