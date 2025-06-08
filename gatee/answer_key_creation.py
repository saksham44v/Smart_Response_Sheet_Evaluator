import pdfplumber
import re
from typing import Dict, Any

def update_question_data_use_questionid_as_key(
    questions_data: Dict[str, Dict[str, Any]],
    answer_key_pdf_path: str,
    starting_question_id: int = 6420084963,
) -> Dict[int, Dict[str, Any]]:
    """
    Updates question data with answer key information extracted from a PDF.

    Args:
        questions_data: A dictionary where keys are question identifiers (e.g., "Q1")
                      and values are dictionaries containing question details
                      (e.g., "page", "question_image", "option_images").
        answer_key_pdf_path: The path to the PDF file containing the answer key.
        starting_question_id: The initial question ID to use for the updated data.

    Returns:
        A dictionary where keys are integer question IDs and values are dictionaries
        containing the combined question and answer key information.
    """

    answer_key_list = []

    with pdfplumber.open(answer_key_pdf_path) as pdf:
        for page in pdf.pages:
            text = page.extract_text()
            if text:
                lines = text.split("\n")
                for line in lines:
                    line = line.strip()
                    # Even more flexible regex to capture various formats
                    match = re.match(
                        r"^(\d+)\s+(\d+)\s+(MCQ|MSQ|NAT)\s+(GA|CS-2)\s+([A-Za-z0-9;\s\.\-to,]+)\s+(\d+)$",
                        line,
                    )
                    if match:
                        q_no, session, q_type, section, key_or_range, marks = match.groups()
                        # print(f"Debug: Matched line - {line}")  # Print the matched line
                        # print(f"Debug: q_no={q_no}, session={session}, q_type={q_type}, section={section}, key_or_range={key_or_range}, marks={marks}") # Print captured groups
                        answer_key_list.append(
                            {
                                "q_no": int(q_no),
                                "session": int(session),
                                "question_type": q_type,
                                "section": section,
                                "key_or_range": key_or_range.strip(),
                                "marks": int(marks),
                            }
                        )
                    else:
                        print(f"Debug: No match - {line}")  # Print lines that don't match

    answer_key_dict = {item["q_no"]: item for item in answer_key_list}

    updated_questions_data = {}
    question_id = starting_question_id

    for q_key, q_value in questions_data.items():
        match = re.search(r"(\d+)", q_key)
        if not match:
            print(f"Warning: No number found in key: {q_key}, skipping...")
            continue
        q_no = int(match.group(1))

        if q_no not in answer_key_dict:
            print(f"Warning: Question {q_no} not found in answer key, skipping...")
            continue

        ans_data = answer_key_dict[q_no]

        updated_questions_data[question_id] = {
            "session": ans_data["session"],
            "question_type": ans_data["question_type"],
            "section": ans_data["section"],
            "key_or_range": ans_data["key_or_range"],
            "marks": ans_data["marks"],
            "page": q_value["page"],
            "question_image": q_value["question_image"],
            "option_images": q_value["option_images"],
        }
        question_id += 1

    return updated_questions_data