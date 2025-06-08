# import requests
# from bs4 import BeautifulSoup
# import json
# import os

# def download_image(image_url, save_path, referer_url):
#     """Downloads image from full URL with headers and saves it locally."""
#     full_url = f"https://cdn.digialm.com{image_url}"
#     headers = {
#         "User-Agent": "Mozilla/5.0",
#         "Referer": referer_url  # Add this line to avoid 403 Forbidden
#     }

#     try:
#         response = requests.get(full_url, headers=headers, stream=True)
#         response.raise_for_status()
#         with open(save_path, "wb") as f:
#             for chunk in response.iter_content(chunk_size=8192):
#                 f.write(chunk)
#         return save_path
#     except Exception as e:
#         print(f"Failed to download {full_url}: {e}")
#         return None
# def scrape_and_download_images(url, config_path="config.json", image_dir="downloaded_images"):
#     """
#     Scrapes GATE response sheet to extract and download question and option images.
#     Returns a dict keyed by question_id with local image paths and a blank correct_ans key.
#     """
#     headers = {
#         "User-Agent": "Mozilla/5.0"
#     }

#     os.makedirs(image_dir, exist_ok=True)

#     try:
#         response = requests.get(url, headers=headers)
#         response.raise_for_status()
#     except requests.exceptions.RequestException as e:
#         print(f"Error fetching URL: {e}")
#         return None

#     soup = BeautifulSoup(response.text, "html.parser")

#     try:
#         with open(config_path, "r") as f:
#             config = json.load(f)
#     except (FileNotFoundError, json.JSONDecodeError):
#         config = {}

#     question_data = {}

#     question_divs = soup.find_all("div", class_="question-pnl")

#     for q_div in question_divs:
#         try:
#             # Question ID
#             q_id_td = q_div.find("td", string="Question ID :")
#             q_id = int(q_id_td.find_next_sibling("td").text.strip()) if q_id_td else None
#             if q_id is None:
#                 continue

#             # Question Type
#             q_type_td = q_div.find("td", string="Question Type :")
#             q_type = q_type_td.find_next_sibling("td").text.strip() if q_type_td else "Unknown"

#             # Image Tags
#             img_tags = q_div.find_all("img")
#             question_image_url = img_tags[0].get("src") if img_tags else None

#             question_local_path = None
#             if question_image_url:
#                 question_filename = f"{q_id}_question.png"
#                 question_local_path = os.path.join(image_dir, question_filename)
#                 download_image(question_image_url, question_local_path, url)


#             question_entry = {
#                 "question_image_url": question_local_path,
#                 "correct_ans": ""
#             }

#             # If not NAT, download and attach option images
#             if q_type != "NAT":
#                 option_image_urls = []
#                 for idx, img_tag in enumerate(img_tags[1:]):
#                     option_src = img_tag.get("src")
#                     if option_src:
#                         option_filename = f"{q_id}_option_{idx + 1}.png"
#                         option_local_path = os.path.join(image_dir, option_filename)
#                         download_image(option_src, option_local_path, url)

#                         option_image_urls.append(option_local_path)

#                 while len(option_image_urls) < 4:
#                     option_image_urls.append(None)

#                 question_entry["option_image_urls"] = option_image_urls

#             question_data[q_id] = question_entry

#         except Exception as e:
#             print(f"Error processing question block: {e}")
#             continue

#     # Sort by question_id
#     sorted_data = dict(sorted(question_data.items()))
#     return sorted_data

# if __name__ == "__main__":
#     url = input("Enter GATE Response Sheet URL: ").strip()
#     result = scrape_and_download_images(url)

#     if result:
#         with open("gate_cse_answer_key.json", "w", encoding="utf-8") as f:
#             json.dump(result, f, indent=2)
#         print("Scraping and image downloading completed. Data saved to 'scraped_questions.json'")
#     else:
#         print("Failed to scrape.")
