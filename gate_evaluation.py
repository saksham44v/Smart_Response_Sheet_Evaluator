# import requests
# from PIL import Image
# import io
# import os
# import logging
# from typing import List, Dict, Any, Optional

# # Configure logging
# logging.basicConfig(level=logging.INFO, format='%(asctime)s - %(levelname)s - %(message)s')

# # Base URL to access Digialm-hosted images
# DIGIALM_BASE_URL = "https://cdn.digialm.com/"


# def download_image(url: str, referer_url: str = None) -> Optional[Image.Image]:
#     headers = {
#         'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/120.0.0.0 Safari/537.36',
#         'Accept': 'image/webp,image/apng,image/*,*/*',
#         'Accept-Language': 'en-US,en;q=0.9',
#     }
#     if referer_url:
#         headers['Referer'] = referer_url

#     try:
#         response = requests.get(url, headers=headers, timeout=10)
#         response.raise_for_status()
#         return Image.open(io.BytesIO(response.content)).convert("RGB")
#     except requests.exceptions.RequestException as e:
#         logging.error(f"Failed to download image from {url}: {e}")
#     except Exception as e:
#         logging.error(f"Failed to open image from {url}: {e}")
#     return None


# def compare_images(image1: Optional[Image.Image], image2: Optional[Image.Image]) -> bool:
#     if image1 is None or image2 is None or image1.size != image2.size:
#         return False
#     try:
#         pixels1 = image1.load()
#         pixels2 = image2.load()
#         for x in range(image1.width):
#             for y in range(image1.height):
#                 if pixels1[x, y] != pixels2[x, y]:
#                     return False
#         return True
#     except Exception as e:
#         logging.error(f"Error comparing images: {e}")
#         return False


# def evaluate_gate_responses(questions: List[Dict[str, Any]], correct_answers: Dict[str, Dict[str, Any]]) -> Dict[str, Any]:
#     total_score = 0.0
#     correct_count = 0
#     incorrect_count = 0
#     unattempted_count = 0
#     total_questions = len(questions)

#     type_data = {
#         "MCQ": {"score": 0.0, "attempted": 0, "correct": 0, "incorrect": 0},
#         "MSQ": {"score": 0.0, "attempted": 0, "correct": 0, "incorrect": 0},
#         "NAT": {"score": 0.0, "attempted": 0, "correct": 0, "incorrect": 0},
#     }

#     for q in questions:
#         q_id = str(q.get("question_id"))
#         q_type = q.get("question_type")
#         status = q.get("status")
#         given_answer = q.get("given_answer", "").strip()
#         chosen_option = q.get("chosen_option", "").strip().upper()

#         if not q_id or q_id not in correct_answers:
#             logging.warning(f"Question ID {q_id} missing in answer key. Skipping.")
#             continue

#         ans_data = correct_answers[q_id]
#         correct_ans = ans_data.get("correct_ans", "")
#         marks = float(ans_data.get("marks", 0.0))
#         option_image_urls = q.get("option_image_urls", [])

#         q["status_correct"] = False

#         if status != "Answered":
#             unattempted_count += 1
#             continue

#         if q_type not in type_data:
#             logging.warning(f"Unknown question type: {q_type} for QID {q_id}. Skipping.")
#             incorrect_count += 1
#             continue

#         type_data[q_type]["attempted"] += 1

#         try:
#             if q_type == "NAT":
#                 low, high = map(float, correct_ans.split(' TO '))
#                 student_answer = float(given_answer)
#                 if low <= student_answer <= high:
#                     correct_count += 1
#                     total_score += marks
#                     type_data[q_type]["score"] += marks
#                     type_data[q_type]["correct"] += 1
#                     q["status_correct"] = True
#                 else:
#                     incorrect_count += 1
#                     type_data[q_type]["incorrect"] += 1

#             elif q_type == "MCQ":
#                 chosen_index = ord(chosen_option) - ord('A')
#                 correct_index = ord(correct_ans) - ord('A')

#                 if not (0 <= chosen_index < len(option_image_urls)) or not (0 <= correct_index < len(option_image_urls)):
#                     logging.warning(f"Invalid option index for QID {q_id}")
#                     incorrect_count += 1
#                     type_data[q_type]["incorrect"] += 1
#                     continue

#                 student_image = download_image(DIGIALM_BASE_URL + option_image_urls[chosen_index].lstrip("/"))
#                 correct_image = os.path.join("gatee", ans_data["option_image_urls"][correct_index])

#                 if compare_images(student_image, correct_image):
#                     correct_count += 1
#                     total_score += marks
#                     type_data[q_type]["score"] += marks
#                     type_data[q_type]["correct"] += 1
#                     q["status_correct"] = True
#                 else:
#                     incorrect_count += 1
#                     penalty = round(marks / 3, 2)
#                     total_score -= penalty
#                     type_data[q_type]["score"] -= penalty
#                     type_data[q_type]["incorrect"] += 1

#             elif q_type == "MSQ":
#                 chosen_options = [opt.strip().upper() for opt in chosen_option.split(',') if opt.strip()]
#                 correct_options = [opt.strip().upper() for opt in correct_ans.split(';') if opt.strip()]

#                 student_images = [
#                     download_image(DIGIALM_BASE_URL + option_image_urls[ord(opt) - ord('A')].lstrip("/"))
#                     if 0 <= ord(opt) - ord('A') < len(option_image_urls)
#                     else None
#                     for opt in chosen_options
#                 ]

#                 correct_images = [
#     "gatee\\" + ans_data["option_image_urls"][ord(opt) - ord('A')]
#     if 0 <= ord(opt) - ord('A') < len(ans_data["option_image_urls"])
#     else None
#     for opt in correct_options
# ]

#                 matches = []
#                 for student_img in student_images:
#                     match_found = any(compare_images(student_img, correct_img) for correct_img in correct_images if correct_img)
#                     matches.append(match_found)

#                 if all(matches) and len(matches) == len(correct_images):
#                     correct_count += 1
#                     total_score += marks
#                     type_data[q_type]["score"] += marks
#                     type_data[q_type]["correct"] += 1
#                     q["status_correct"] = True
#                 else:
#                     incorrect_count += 1
#                     type_data[q_type]["incorrect"] += 1

#         except Exception as e:
#             logging.error(f"Error evaluating QID {q_id}: {e}")
#             incorrect_count += 1
#             type_data[q_type]["incorrect"] += 1

#     attempted_count = total_questions - unattempted_count
#     completed_percentage = round((attempted_count / total_questions) * 100, 2) if total_questions else 0.0
#     accuracy = round((correct_count / attempted_count) * 100, 2) if attempted_count else 0.0

#     return {
#         "total_score": round(total_score, 2),
#         "attempted": attempted_count,
#         "correct": correct_count,
#         "incorrect": incorrect_count,
#         "skipped": unattempted_count,
#         "completed_percentage": completed_percentage,
#         "accuracy": accuracy,
#         "type_data": type_data,
#         "questions": questions,
#     }



import requests
from PIL import Image
import io
import os
import logging
from typing import List, Dict, Any, Optional

def normalize_image_path(path: str) -> str:
    return os.path.join("gatee", *path.split("\\"))  # Ensures platform-independent path
# Configure logging
logging.basicConfig(level=logging.INFO, format='%(asctime)s - %(levelname)s - %(message)s')

# Base URL to access Digialm-hosted images
DIGIALM_BASE_URL = "https://cdn.digialm.com/"

def download_image(url: str, referer_url: str = None) -> Optional[Image.Image]:
    headers = {
        'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/120.0.0.0 Safari/537.36',
        'Accept': 'image/webp,image/apng,image/*,*/*',
        'Accept-Language': 'en-US,en;q=0.9',
    }
    if referer_url:
        headers['Referer'] = referer_url

    try:
        response = requests.get(url, headers=headers, timeout=10)
        response.raise_for_status()  # Raise error if not successful
        return Image.open(io.BytesIO(response.content)).convert("RGB")
    except requests.exceptions.RequestException as e:
        logging.error(f"Failed to download image from {url}: {e}")
    except Exception as e:
        logging.error(f"Failed to open image from {url}: {e}")
    return None

# def compare_images(image1: Optional[Image.Image], image2: Optional[Image.Image]) -> bool:
#     # Check if either image is None
#     if image1 is None or image2 is None:
#         logging.error("One or both images are None")
#         return False
    
#     # Check if sizes match
#     if image1.size != image2.size:
#         logging.error(f"Image sizes do not match: {image1.size} vs {image2.size}")
#         return False
    
#     # Compare pixel-by-pixel
#     try:
#         pixels1 = image1.load()
#         pixels2 = image2.load()
#         for x in range(image1.width):
#             for y in range(image1.height):
#                 if pixels1[x, y] != pixels2[x, y]:
#                     return False
#         return True
#     except Exception as e:
#         logging.error(f"Error comparing images: {e}")
#         return False

import numpy as np

def compare_images(img1: Image.Image, img2: Image.Image) -> bool:
    try:
        return np.array_equal(np.array(img1), np.array(img2))
    except Exception as e:
        logging.error(f"Image comparison error: {e}")
        return False


def evaluate_gate_responses(questions: List[Dict[str, Any]], correct_answers: Dict[str, Dict[str, Any]]) -> Dict[str, Any]:
    total_score = 0.0
    correct_count = 0
    incorrect_count = 0
    unattempted_count = 0
    total_questions = len(questions)

    type_data = {
        "MCQ": {"score": 0.0, "attempted": 0, "correct": 0, "incorrect": 0},
        "MSQ": {"score": 0.0, "attempted": 0, "correct": 0, "incorrect": 0},
        "NAT": {"score": 0.0, "attempted": 0, "correct": 0, "incorrect": 0},
    }

    for q in questions:
        q_id = str(q.get("question_id"))
        q_type = q.get("question_type")
        status = q.get("status")
        given_answer = q.get("given_answer", "").strip()
        chosen_option = q.get("chosen_option", "").strip().upper()

        if not q_id or q_id not in correct_answers:
            logging.warning(f"Question ID {q_id} missing in answer key. Skipping.")
            continue

        ans_data = correct_answers[q_id]
        correct_ans = ans_data.get("correct_ans", "")
        marks = float(ans_data.get("marks", 0.0))
        option_image_urls = q.get("option_image_urls", [])

        q["status_correct"] = False

        if status != "Answered":
            unattempted_count += 1
            continue

        if q_type not in type_data:
            logging.warning(f"Unknown question type: {q_type} for QID {q_id}. Skipping.")
            incorrect_count += 1
            continue

        type_data[q_type]["attempted"] += 1

        try:
            if q_type == "NAT":
                low, high = map(float, correct_ans.split(' TO '))
                student_answer = float(given_answer)
                if low <= student_answer <= high:
                    correct_count += 1
                    total_score += marks
                    type_data[q_type]["score"] += marks
                    type_data[q_type]["correct"] += 1
                    q["status_correct"] = True
                else:
                    incorrect_count += 1
                    type_data[q_type]["incorrect"] += 1

            elif q_type == "MCQ":
                chosen_index = ord(chosen_option) - ord('A')
                correct_index = ord(correct_ans) - ord('A')

                if not (0 <= chosen_index < len(option_image_urls)) or not (0 <= correct_index < len(option_image_urls)):
                    logging.warning(f"Invalid option index for QID {q_id}")
                    incorrect_count += 1
                    type_data[q_type]["incorrect"] += 1
                    continue

                student_image = download_image(DIGIALM_BASE_URL + option_image_urls[chosen_index].lstrip("/"))
                if student_image is None:
                    logging.error(f"Failed to download image for option {chosen_option} of QID {q_id}")
                    incorrect_count += 1
                    type_data[q_type]["incorrect"] += 1
                    continue

                # Load the correct image as well
                correct_image_path_raw = ans_data["option_image_urls"][correct_index]
                correct_image_path = normalize_image_path(correct_image_path_raw)
                correct_image = None
                try:
                    correct_image = Image.open(correct_image_path).convert("RGB")
                except Exception as e:
                    logging.error(f"Failed to open correct image for QID {q_id} at {correct_image_path}: {e}")
                    incorrect_count += 1
                    type_data[q_type]["incorrect"] += 1
                    continue

                if compare_images(student_image, correct_image):
                    correct_count += 1
                    total_score += marks
                    type_data[q_type]["score"] += marks
                    type_data[q_type]["correct"] += 1
                    q["status_correct"] = True
                else:
                    incorrect_count += 1
                    penalty = round(marks / 3, 2)
                    total_score -= penalty
                    type_data[q_type]["score"] -= penalty
                    type_data[q_type]["incorrect"] += 1

            elif q_type == "MSQ":
                chosen_options = [opt.strip().upper() for opt in chosen_option.split(',') if opt.strip()]
                correct_options = [opt.strip().upper() for opt in correct_ans.split(';') if opt.strip()]

                student_images = [
                    download_image(DIGIALM_BASE_URL + option_image_urls[ord(opt) - ord('A')].lstrip("/"))
                    if 0 <= ord(opt) - ord('A') < len(option_image_urls)
                    else None
                    for opt in chosen_options
                ]

                correct_images = [
                normalize_image_path(ans_data["option_image_urls"][ord(opt) - ord('A')])
                if 0 <= ord(opt) - ord('A') < len(ans_data["option_image_urls"])
                else None
                for opt in correct_options
                ]

                matches = []
                for student_img in student_images:
                    match_found = any(compare_images(student_img, correct_img) for correct_img in correct_images if correct_img)
                    matches.append(match_found)

                if all(matches) and len(matches) == len(correct_images):
                    correct_count += 1
                    total_score += marks
                    type_data[q_type]["score"] += marks
                    type_data[q_type]["correct"] += 1
                    q["status_correct"] = True
                else:
                    incorrect_count += 1
                    type_data[q_type]["incorrect"] += 1

        except Exception as e:
            logging.error(f"Error evaluating QID {q_id}: {e}")
            incorrect_count += 1
            type_data[q_type]["incorrect"] += 1

    attempted_count = total_questions - unattempted_count
    completed_percentage = round((attempted_count / total_questions) * 100, 2) if total_questions else 0.0
    accuracy = round((correct_count / attempted_count) * 100, 2) if attempted_count else 0.0

    return {
        "total_score": round(total_score, 2),
        "attempted": attempted_count,
        "correct": correct_count,
        "incorrect": incorrect_count,
        "skipped": unattempted_count,
        "completed_percentage": completed_percentage,
        "accuracy": accuracy,
        "type_data": type_data,
        "questions": questions,
    }
