import requests
from bs4 import BeautifulSoup
import json
import os

def extract_image_data_with_subject(url, config_path="config.json"):
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
    except (FileNotFoundError, json.JSONDecodeError):
        config = {}

    # Extract date and slot
    try:
        exam_date_selector = config.get("exam_date_selector", "td:contains('Test Date') + td")
        exam_time_selector = config.get("exam_time_selector", "td:contains('Test Time') + td")

        exam_date = soup.select_one(exam_date_selector).text.strip()
        exam_time = soup.select_one(exam_time_selector).text.strip()
        slot_time = exam_time.split("-")[0].strip()
    except AttributeError:
        print("Failed to extract date/slot.")
        return None

    question_map = {}
    current_subject = None

    for element in soup.find_all(["span", "div"]):
        # Update current_subject if the section header appears
        if element.name == "span" and "Section" in element.text:
            if "Physics" in element.text:
                current_subject = "Physics"
            elif "Chemistry" in element.text:
                current_subject = "Chemistry"
            elif "Mathematics" in element.text:
                current_subject = "Mathematics"

        elif element.name == "div" and "question-pnl" in element.get("class", []):
            q_id_selector = config.get("question_id_selector", "td:contains('Question ID :') + td")
            question_image_selector = config.get("question_image_selector", "img[name]")

            try:
                q_id = element.select_one(q_id_selector).text.strip()
            except AttributeError:
                continue

            question_image_element = element.select_one(question_image_selector)
            question_image_url = question_image_element.get("src") if question_image_element else None

            if q_id and question_image_url:
                question_map[q_id] = {
                    "question_image_url": question_image_url,
                    "subject": current_subject
                }

    return {
        "exam_date": exam_date,
        "slot_time": slot_time,
        "questions": question_map
    }
