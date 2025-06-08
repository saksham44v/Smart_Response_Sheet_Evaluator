import os
import json
import requests
from tqdm import tqdm

BASE_URL = "https://cdn3.digialm.com"
QUESTION_DATA_FILE = "question_tagging_logic\question_data.json"
SAVE_DIR = "question_tagging_logic\question_image_data"

def sanitize_folder_name(name):
    return name.replace("/", "-").replace(":", "-").replace(" ", "_")

def download_image(url, path):
    try:
        response = requests.get(BASE_URL + url, timeout=10)
        response.raise_for_status()
        with open(path, "wb") as f:
            f.write(response.content)
        return True
    except Exception as e:
        print(f"Failed to download {url}: {e}")
        return False

def download_all_images():
    if not os.path.exists(SAVE_DIR):
        os.makedirs(SAVE_DIR)

    with open(QUESTION_DATA_FILE, "r") as f:
        question_data = json.load(f)

    for date, shifts in question_data.items():
        for shift, questions in shifts.items():
            folder_name = f"{sanitize_folder_name(date)}_{sanitize_folder_name(shift)}"
            folder_path = os.path.join(SAVE_DIR, folder_name)
            os.makedirs(folder_path, exist_ok=True)

            print(f"\n⬇️ Downloading images for {date} - {shift}...")
            for qid, img_url in tqdm(questions.items()):
                filename = f"{qid}.jpg"
                file_path = os.path.join(folder_path, filename)

                if os.path.exists(file_path):
                    continue  # Skip if already downloaded

                download_image(img_url, file_path)

if __name__ == "__main__":
    download_all_images()
