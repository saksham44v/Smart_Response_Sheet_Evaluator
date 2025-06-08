import requests
from bs4 import BeautifulSoup
import json
import os

def scrape_gate_response_sheet(url, config_path="config.json"):
    """
    Scrapes GATE response sheet, extracting questions, subject info, status, chosen options,
    and image URLs for questions and options.
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

    # # Save HTML locally for debug
    # with open("gate_scraped_page.html", "w", encoding="utf-8") as f:
    #     f.write(str(soup))

    try:
        with open(config_path, "r") as f:
            config = json.load(f)
    except (FileNotFoundError, json.JSONDecodeError) as e:
        print(f"Warning: Config file not found or invalid: {e}. Using defaults.")
        config = {}

    # --- Extract Exam Info ---
    exam_date_selector = config.get("exam_date_selector", "td:contains('Test Date') + td")
    exam_time_selector = config.get("exam_time_selector", "td:contains('Test Time') + td")
    subject_selector = config.get("subject_selector", "td:contains('Subject') + td")

    try:
        exam_date = soup.select_one(exam_date_selector).text.strip()
        exam_time = soup.select_one(exam_time_selector).text.strip()
        exam_slot = exam_time.split("-")[0].strip()
    except AttributeError:
        print("Warning: Could not extract exam date/time.")
        exam_date = "N/A"
        exam_slot = "N/A"

    try:
        subject = soup.select_one(subject_selector).text.strip()
    except AttributeError:
        print("Warning: Could not extract subject name.")
        subject = "N/A"

    # --- Extract Questions ---
    questions_data = []
    question_divs = soup.find_all("div", class_="question-pnl")

    for q_div in question_divs:
        try:
            # Question Number (Q.1, Q.2, etc.)
            q_number_td = q_div.find("td", class_="bold", align="center")
            q_number = q_number_td.get_text(strip=True) if q_number_td else "Unknown"

            # Question ID
            q_id_td = q_div.find("td", string="Question ID :")
            q_id = int(q_id_td.find_next_sibling("td").text.strip()) if q_id_td else None

            # Question Type
            q_type_td = q_div.find("td", string="Question Type :")
            q_type = q_type_td.find_next_sibling("td").text.strip() if q_type_td else "Unknown"

            # Status
            status_td = q_div.find("td", string="Status :")
            status = status_td.find_next_sibling("td").text.strip() if status_td else "Unknown"

            # Initialize given_answer and chosen_option
            given_answer = None
            chosen_option = "--"

            if q_type == "NAT":
                # NAT: Look for "Given Answer"
                given_answer_td = q_div.find("td", string="Given Answer :")
                if given_answer_td:
                    given_answer = given_answer_td.find_next_sibling("td").text.strip()
            else:
                # MCQ or MSQ: Look for "Chosen Option"
                chosen_option_td = q_div.find("td", string="Chosen Option :")
                if chosen_option_td:
                    chosen_option = chosen_option_td.find_next_sibling("td").text.strip()

            # --- Question and Option Images ---
            img_tags = q_div.find_all("img")

            # First image = Question Image
            question_img_tag = img_tags[0] if img_tags else None
            question_image_url = question_img_tag["src"] if question_img_tag else None

            # Option images for MCQ/MSQ (not NAT)
            option_image_urls = []
            if q_type != "NAT":
                for img_tag in img_tags[1:]:
                    src = img_tag.get("src")
                    if src:
                        option_image_urls.append(src)

                while len(option_image_urls) < 4:
                    option_image_urls.append(None)
            else:
                option_image_urls = []  # For NAT, no options

            # Add the question
            question_entry = {
                "question_number": q_number,
                "question_id": q_id,
                "question_type": q_type,
                "status": status,
                "question_image_url": question_image_url,
                "option_image_urls": option_image_urls
            }

            if q_type == "NAT":
                question_entry["given_answer"] = given_answer
            else:
                question_entry["chosen_option"] = chosen_option

            questions_data.append(question_entry)

        except Exception as e:
            print(f"Error parsing a question block: {e}")
            continue

    return {
        "exam_date": exam_date,
        "slot_time": exam_slot,
        "subject": subject,
        "questions": questions_data
    }


# --- Example Usage ---
# if __name__ == "__main__":
#     url = input("Enter GATE Response Sheet URL: ").strip()
#     result = scrape_gate_response_sheet(url)

#     if result:
#         print(json.dumps(result, indent=2))
#     else:
#         print("Failed to scrape.")
