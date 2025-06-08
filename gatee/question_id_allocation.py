import requests
from bs4 import BeautifulSoup
import os
import re
# --- OCR and Text Similarity ---
import pytesseract
from difflib import SequenceMatcher
# --- Image Handling ---
from PIL import Image
import io
# --- Standard Libraries ---
import collections
import logging

# --- Configuration ---
logging.basicConfig(level=logging.INFO, format='%(levelname)s: %(message)s')
# logging.basicConfig(level=logging.DEBUG, format='%(levelname)s: %(message)s') # Use DEBUG for more detail

# --- Helper Functions ---

def extract_text_from_image_data(image_data):
    """Extracts text from image binary data using Tesseract OCR."""
    try:
        img = Image.open(io.BytesIO(image_data))
        # Perform OCR
        # You might need to configure the path to tesseract executable if not in PATH
        # pytesseract.pytesseract.tesseract_cmd = r'/path/to/your/tesseract' # Example for Windows/Linux
        text = pytesseract.image_to_string(img)
        # Basic text cleaning (remove extra whitespace/newlines)
        cleaned_text = " ".join(text.split())
        # logging.debug(f"OCR Extracted Text: '{cleaned_text[:100]}...'") # Log first 100 chars
        return cleaned_text
    except ImportError:
        logging.error("pytesseract library not found. Please install it (`pip install pytesseract`).")
        raise # Re-raise error to stop execution if OCR isn't available
    except pytesseract.TesseractNotFoundError:
        logging.error("Tesseract executable not found or not in PATH. Please install Tesseract OCR engine.")
        raise
    except Exception as e:
        logging.error(f"Error during OCR processing: {e}")
        return None # Return None on other errors

def calculate_text_similarity(text1, text2):
    """Calculates similarity ratio between two strings."""
    if not text1 or not text2:
        return 0.0
    return SequenceMatcher(None, text1, text2).ratio()

def download_image_data(image_url):
    """Downloads image data from a URL."""
    try:
        headers = {'User-Agent': 'Mozilla/5.0'}
        response = requests.get(image_url, headers=headers, timeout=15) # Increased timeout
        response.raise_for_status()
        return response.content
    except requests.exceptions.RequestException as e:
        logging.error(f"Error downloading image {image_url}: {e}")
        return None

def find_best_text_match(response_text, snapshot_texts, threshold=0.7):
    """Finds the best snapshot match based on text similarity."""
    if not response_text:
        return None, 0.0

    best_match_key = None
    max_similarity = 0.0

    for snap_key, snap_text in snapshot_texts.items():
        if not snap_text:
            continue
        similarity = calculate_text_similarity(response_text, snap_text)
        # logging.debug(f"  Comparing with {snap_key}: similarity = {similarity:.4f}")
        if similarity > max_similarity:
            max_similarity = similarity
            best_match_key = snap_key

    if max_similarity >= threshold:
        # logging.debug(f"  Found best text match: {best_match_key} with similarity {max_similarity:.4f}")
        return best_match_key, max_similarity
    else:
        logging.warning(f"  No text match found within threshold ({threshold}). Max similarity: {max_similarity:.4f} to {best_match_key}")
        return None, max_similarity


# --- Main Logic ---

def correlate_response_with_snapshots_ocr(
    html_content,
    snapshot_folder,
    base_url,
    similarity_threshold=0.6 # Similarity ratio threshold (0.0 to 1.0)
    ):
    """
    Correlates questions from HTML response sheet with snapshots using OCR text matching.

    Args:
        html_content (str): Full HTML content of the response sheet.
        snapshot_folder (str): Path to the folder containing snapshot images.
        base_url (str): Base URL for constructing full image URLs.
        similarity_threshold (float): Minimum similarity ratio (0.0 to 1.0) for a match.

    Returns:
        dict: Dictionary mapping Question Number (from snapshot) to response sheet data.
              Returns None if snapshot folder is invalid or OCR fails critically.
    """
    if not os.path.isdir(snapshot_folder):
        logging.error(f"Snapshot folder not found: {snapshot_folder}")
        return None

    logging.info("Loading snapshots and extracting text using OCR...")
    snapshot_texts = {}
    snapshot_files = {} # Store full paths associated with question keys

    # 1. Load Snapshot Images and Extract Text via OCR
    for filename in os.listdir(snapshot_folder):
        if filename.lower().endswith("_question.png"):
            match = re.match(r"(Q\d+)_question\.png", filename, re.IGNORECASE)
            if match:
                question_key = match.group(1).upper() # e.g., "Q1"
                filepath = os.path.join(snapshot_folder, filename)
                snapshot_files[question_key] = filepath # Store path regardless of OCR success
                try:
                    with open(filepath, "rb") as f:
                        img_data = f.read()
                    extracted_text = extract_text_from_image_data(img_data)
                    if extracted_text:
                        snapshot_texts[question_key] = extracted_text
                        logging.info(f"  Extracted text for snapshot {question_key} (len: {len(extracted_text)})")
                    else:
                         logging.warning(f"  Could not extract text via OCR for snapshot: {filename}")

                except (pytesseract.TesseractNotFoundError, ImportError) as ocr_err:
                     logging.error(f"OCR setup error for {filename}: {ocr_err}. Aborting.")
                     return None # Stop if OCR isn't set up
                except Exception as e:
                    logging.error(f"Error processing snapshot {filename}: {e}")

    if not snapshot_texts:
        logging.error("No text could be extracted from any question snapshots.")
        return {}

    logging.info(f"Successfully extracted text from {len(snapshot_texts)} question snapshots.")

    # 2. Parse HTML and Process Response Sheet Questions
    logging.info("Parsing HTML response sheet...")
    soup = BeautifulSoup(html_content, 'html.parser')
    question_panels = soup.find_all('div', class_='question-pnl')
    logging.info(f"Found {len(question_panels)} question panels in HTML.")

    correlation_results = collections.OrderedDict()

    for panel_index, panel in enumerate(question_panels):
        logging.info(f"--- Processing Response Panel {panel_index + 1}/{len(question_panels)} ---")
        try:
            # Find Question ID
            q_id = "Unknown"
            menu_tbl = panel.find('table', class_='menu-tbl')
            if menu_tbl:
                # Simplified QID extraction
                 q_id_cell = menu_tbl.find('td', string=re.compile(r'Question ID\s*:'))
                 if q_id_cell and q_id_cell.find_next_sibling('td'):
                     q_id = q_id_cell.find_next_sibling('td').get_text(strip=True)
            logging.info(f"  Found Response Question ID: {q_id}")


            # Find the main question image URL
            question_img_tag = None
            question_row_tbl = panel.find('table', class_='questionRowTbl')
            if question_row_tbl:
                 q_num_cell = question_row_tbl.find('td', string=re.compile(r'^\s*Q\.\d+\s*$'))
                 if q_num_cell and q_num_cell.find_next_sibling('td'):
                     img_cell = q_num_cell.find_next_sibling('td')
                     question_img_tag = img_cell.find('img')
                     if not question_img_tag:
                        question_img_tag = q_num_cell.find_next('img')


            if not question_img_tag or not question_img_tag.get('src'):
                logging.warning(f"  Could not find question image tag/src for QID {q_id}. Skipping.")
                continue

            relative_q_img_url = question_img_tag['src']
            full_q_img_url = f"{base_url.rstrip('/')}/{relative_q_img_url.lstrip('/')}"
            logging.info(f"  Response Question Image URL: {full_q_img_url}")

            # Find option image URLs (same logic as before)
            option_img_urls = {}
            if question_row_tbl:
                option_rows = question_row_tbl.find_all('tr')
                for row in option_rows:
                     cells = row.find_all('td')
                     if len(cells) == 2:
                          option_text = cells[1].get_text(strip=True)
                          # Updated regex to handle options like A., B., etc.
                          option_match = re.match(r"^\s*([ABCD])\.", option_text)
                          if option_match:
                               marker = option_match.group(1)
                               img_tag = cells[1].find('img')
                               if img_tag and img_tag.get('src'):
                                    relative_opt_url = img_tag['src']
                                    full_opt_url = f"{base_url.rstrip('/')}/{relative_opt_url.lstrip('/')}"
                                    option_img_urls[marker] = full_opt_url


            # 3. Download Response Image and Extract Text via OCR
            logging.info(f"  Downloading image for QID {q_id}...")
            response_img_data = download_image_data(full_q_img_url)
            if not response_img_data:
                logging.warning(f"  Failed to download image for QID {q_id}. Skipping.")
                continue

            logging.info(f"  Extracting text via OCR for QID {q_id}...")
            response_text = extract_text_from_image_data(response_img_data)
            if not response_text:
                 logging.warning(f"  Failed to extract text from response image for QID {q_id}. Skipping.")
                 continue
            logging.info(f"  Extracted response text (len: {len(response_text)})")

            # 4. Find Best Snapshot Match based on Text Similarity
            logging.info(f"  Comparing response text (QID {q_id}) against snapshot texts...")
            matched_key, similarity = find_best_text_match(response_text, snapshot_texts, similarity_threshold)

            # 5. Store Results
            if matched_key:
                logging.info(f"  MATCH FOUND: Response QID {q_id} matches Snapshot {matched_key} (Similarity: {similarity:.4f})")
                if matched_key in correlation_results:
                     logging.warning(f"  Duplicate match! Snapshot {matched_key} already matched to QID {correlation_results[matched_key]['question_id']}. Overwriting with QID {q_id} (check threshold/images).")

                correlation_results[matched_key] = {
                    "question_id": q_id,
                    "snapshot_question_image": snapshot_files.get(matched_key, "N/A"),
                    "response_question_image_url": full_q_img_url,
                    "response_option_image_urls": option_img_urls,
                    "match_similarity_score": similarity
                }
            else:
                 logging.warning(f"  NO MATCH FOUND for Response QID {q_id} within threshold.")

        except (pytesseract.TesseractNotFoundError, ImportError) as ocr_err:
             logging.error(f"OCR setup error during panel processing: {ocr_err}. Aborting.")
             return None # Stop if OCR isn't set up
        except Exception as e:
            logging.error(f"Error processing panel {panel_index + 1} (QID {q_id}): {e}", exc_info=True)

    logging.info(f"Correlation complete. Matched {len(correlation_results)} questions based on text similarity.")
    return correlation_results

# --- Example Usage ---
if __name__ == "__main__":
    # --- !!! IMPORTANT INPUTS - MODIFY THESE !!! ---

    # 1. Provide the FULL HTML content as a string or read from a file
    try:
        with open("response.html", "r", encoding="utf-8") as f:
            html_content_string = f.read()
    except FileNotFoundError:
        logging.error("Error: response_sheet.html not found. Please provide the HTML content.")
        html_content_string = None

    # 2. Set the path to the folder containing your snapshots
    snapshot_dir = "gate_cs_snapshots_v4" # Make sure this exists and has _question.png files

    # 3. Set the BASE URL of the website hosting the response sheet images
    exam_base_url = "https://g21.tcsion.com" # <--- *** REPLACE WITH ACTUAL BASE URL ***

    # 4. (Optional) Adjust the text similarity threshold (0.0 to 1.0)
    #    Higher values mean stricter matching. Start around 0.6-0.7 maybe.
    match_threshold = 0.6

    # 5. (Optional) If Tesseract is not in your system's PATH, uncomment and set the path below
    # pytesseract.pytesseract.tesseract_cmd = r'C:\Program Files\Tesseract-OCR\tesseract.exe' # Example for Windows
    # pytesseract.pytesseract.tesseract_cmd = r'/usr/bin/tesseract' # Example for Linux (often default)
    # pytesseract.pytesseract.tesseract_cmd = r'/opt/homebrew/bin/tesseract' # Example for macOS (Homebrew)


    # --- Run the correlation ---
    if html_content_string and exam_base_url:
        # Use the new function name
        results = correlate_response_with_snapshots_ocr(
            html_content=html_content_string,
            snapshot_folder=snapshot_dir,
            base_url=exam_base_url,
            similarity_threshold=match_threshold
        )

        if results is not None:
            print("\n--- Correlation Results (OCR Text Matching) ---")
            if not results:
                 print("No matches found.")
            else:
                # Sort by question number numerically for printing
                try:
                    sorted_q_keys = sorted(results.keys(), key=lambda q: int(re.search(r'\d+', q).group()))
                except: # Fallback if keys aren't like 'Q1'
                    sorted_q_keys = sorted(results.keys())

                for q_key in sorted_q_keys:
                    data = results[q_key]
                    print(f"{q_key}:")
                    print(f"  - Response Question ID: {data['question_id']}")
                    print(f"  - Matched Snapshot File: {os.path.basename(data['snapshot_question_image'])}")
                    # print(f"  - Response Img URL: {data['response_question_image_url']}") # Uncomment if needed
                    print(f"  - Match Similarity: {data['match_similarity_score']:.4f}")
                    # print(f"  - Option URLs: {data['response_option_image_urls']}") # Uncomment to print option URLs
                print(f"\nSuccessfully correlated {len(results)} questions.")
        else:
            print("\nCorrelation process failed. Check logs for errors (especially OCR setup).")
    else:
         if not html_content_string:
              print("\nError: HTML content not provided. Please edit the script.")
         if not exam_base_url:
              print("\nError: Base URL (`exam_base_url`) not set. Please edit the script.")

