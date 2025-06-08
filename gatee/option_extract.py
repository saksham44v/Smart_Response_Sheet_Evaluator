import fitz  # PyMuPDF
import re
import os
import collections
import logging

# Setup basic logging
logging.basicConfig(level=logging.INFO, format='%(levelname)s: %(message)s')

def is_horizontally_aligned(rect1, rect2, tolerance=0.1):
    page_width = rect1.page.rect.width if hasattr(rect1, 'page') else 1000
    allowed_offset = page_width * tolerance
    return (abs(rect1.x0 - rect2.x0) < allowed_offset or
            abs(rect1.x1 - rect2.x1) < allowed_offset or
            (rect1.x0 <= rect2.x0 and rect1.x1 >= rect2.x1) or
            (rect2.x0 <= rect1.x0 and rect2.x1 >= rect1.x1))

def get_block_text(block):
    try:
        return block['lines'][0]['spans'][0]['text'].strip()
    except (IndexError, KeyError, TypeError):
        return ""

def expand_rect_with_images(base_rect, image_bboxes, page_rect, vertical_threshold=0.05, included_images=None):
    if included_images is None:
        included_images = set()
    expanded_rect = fitz.Rect(base_rect)
    newly_included = []
    max_vertical_gap = page_rect.height * vertical_threshold

    for i, img_bbox_orig in enumerate(image_bboxes):
        if i in included_images:
            continue
        img_bbox = fitz.Rect(img_bbox_orig)
        horizontal_overlap = max(0, min(base_rect.x1, img_bbox.x1) - max(base_rect.x0, img_bbox.x0))
        significant_horizontal_overlap = horizontal_overlap > min(base_rect.width, img_bbox.width) * 0.5
        vertical_gap = img_bbox.y0 - base_rect.y1
        is_vertically_close = -img_bbox.height * 0.5 < vertical_gap < max_vertical_gap
        is_vertically_centered = abs((base_rect.y0 + base_rect.y1)/2 - (img_bbox.y0 + img_bbox.y1)/2) < base_rect.height
        is_horizontally_relevant = significant_horizontal_overlap or is_horizontally_aligned(base_rect, img_bbox, tolerance=0.2)
        if (is_vertically_close or is_vertically_centered) and is_horizontally_relevant:
            expanded_rect.include_rect(img_bbox)
            newly_included.append(i)

    included_images.update(newly_included)
    return expanded_rect

def extract_question_snapshots(pdf_path, output_dir="question_cs_snapshots_v3"):
    questions_data = collections.OrderedDict()
    margin = 8
    dpi = 200
    vertical_text_gap_threshold_q = 0.05
    vertical_text_gap_threshold_opt = 0.03
    image_vertical_proximity_threshold = 0.04

    if not os.path.exists(pdf_path):
        logging.error(f"PDF file not found at {pdf_path}")
        return None
    if not os.path.exists(output_dir):
        os.makedirs(output_dir)
        logging.info(f"Created output directory: {output_dir}")

    try:
        doc = fitz.open(pdf_path)
    except Exception as e:
        logging.error(f"Error opening PDF file: {e}")
        return None

    logging.info(f"Processing PDF: {pdf_path}...")

    for page_num in range(len(doc)):
        page = doc.load_page(page_num)
        page_rect = page.rect
        logging.info(f"Processing Page {page_num + 1}/{len(doc)}")

        blocks = page.get_text("dict", flags=fitz.TEXTFLAGS_TEXT)["blocks"]
        try:
            page_images_info = page.get_images(full=True)
            image_bboxes_with_indices = [(i, fitz.Rect(img[7])) for i, img in enumerate(page_images_info)
                                         if len(img) > 7 and img[7] and fitz.Rect(img[7]).width > 0 and fitz.Rect(img[7]).height > 0]
        except Exception as img_e:
            logging.warning(f"Could not extract images from page {page_num + 1}: {img_e}")
            image_bboxes_with_indices = []

        min_y = page_rect.height * 0.08
        max_y = page_rect.height * 0.95
        content_blocks = [b for b in blocks if b['bbox'][1] > min_y and b['bbox'][3] < max_y and b['lines']]

        processed_block_indices = set()
        included_image_indices = set()

        i = 0
        while i < len(content_blocks):
            if i in processed_block_indices:
                i += 1
                continue

            block = content_blocks[i]
            block_rect = fitz.Rect(block['bbox'])
            first_line_text = get_block_text(block)
            q_match = re.match(r"^\s*Q\.(\d+)", first_line_text)

            if q_match:
                question_num_str = q_match.group(1)
                question_key = f"Q{question_num_str}"
                logging.info(f"  Found potential {question_key} starting at block {i}...")

                question_text_rect = fitz.Rect(block_rect)
                current_question_blocks = {i}
                last_text_block_idx = i
                j = i + 1
                while j < len(content_blocks):
                    if j in processed_block_indices:
                        j += 1
                        continue

                    next_block = content_blocks[j]
                    next_block_rect = fitz.Rect(next_block['bbox'])
                    next_block_first_line = get_block_text(next_block)

                    if re.match(r"^\s*Q\.(\d+)", next_block_first_line):
                        break
                    if re.match(r"^\s*\([ABCD]\)", next_block_first_line):
                        break

                    vertical_gap = next_block_rect.y0 - content_blocks[last_text_block_idx]['bbox'][3]
                    if vertical_gap > page_rect.height * vertical_text_gap_threshold_q:
                        break

                    if not is_horizontally_aligned(block_rect, next_block_rect, tolerance=0.2):
                        prev_block_rect = fitz.Rect(content_blocks[last_text_block_idx]['bbox'])
                        if not is_horizontally_aligned(prev_block_rect, next_block_rect, tolerance=0.1):
                            break

                    question_text_rect.include_rect(next_block_rect)
                    current_question_blocks.add(j)
                    last_text_block_idx = j
                    j += 1

                question_final_rect = expand_rect_with_images(
                    question_text_rect,
                    [img_bbox for idx, img_bbox in image_bboxes_with_indices],
                    page_rect,
                    image_vertical_proximity_threshold,
                    included_image_indices
                )

                option_rects = collections.OrderedDict()
                option_markers = ['A', 'B', 'C', 'D']
                current_option_idx = 0
                found_options = False
                option_search_start_idx = max(current_question_blocks) + 1
                k = option_search_start_idx

                while k < len(content_blocks) and current_option_idx < len(option_markers):
                    if k in processed_block_indices or k in current_question_blocks:
                        k += 1
                        continue

                    opt_block = content_blocks[k]
                    opt_block_rect = fitz.Rect(opt_block['bbox'])
                    opt_block_first_line = get_block_text(opt_block)

                    if re.match(r"^\s*Q\.(\d+)", opt_block_first_line):
                        break

                    expected_marker = option_markers[current_option_idx]
                    opt_match = re.match(r"^\s*\(" + re.escape(expected_marker) + r"\)", opt_block_first_line)

                    if opt_match:
                        found_options = True
                        option_text_rect = fitz.Rect(opt_block_rect)
                        current_option_blocks = {k}
                        last_opt_block_idx = k
                        l = k + 1
                        while l < len(content_blocks):
                            if l in processed_block_indices or l in current_question_blocks:
                                l += 1
                                continue

                            next_opt_block = content_blocks[l]
                            next_opt_block_rect = fitz.Rect(next_opt_block['bbox'])
                            next_opt_block_first_line = get_block_text(next_opt_block)

                            if re.match(r"^\s*Q\.(\d+)", next_opt_block_first_line):
                                break
                            if current_option_idx < len(option_markers) - 1 and \
                               re.match(r"^\s*\(" + re.escape(option_markers[current_option_idx+1]) + r"\)", next_opt_block_first_line):
                                break

                            vertical_gap = next_opt_block_rect.y0 - content_blocks[last_opt_block_idx]['bbox'][3]
                            if vertical_gap > page_rect.height * vertical_text_gap_threshold_opt:
                                break

                            if not is_horizontally_aligned(opt_block_rect, next_opt_block_rect, tolerance=0.1):
                                break

                            option_text_rect.include_rect(next_opt_block_rect)
                            current_option_blocks.add(l)
                            last_opt_block_idx = l
                            l += 1

                        option_final_rect = expand_rect_with_images(
                            option_text_rect,
                            [img_bbox for idx, img_bbox in image_bboxes_with_indices],
                            page_rect,
                            image_vertical_proximity_threshold,
                            included_image_indices
                        )

                        option_rects[expected_marker] = (option_final_rect, current_option_blocks)
                        processed_block_indices.update(current_option_blocks)
                        current_option_idx += 1
                        k = max(current_option_blocks)
                    elif found_options:
                        break
                    k += 1

                processed_block_indices.update(current_question_blocks)

                if option_rects:
                    first_option_marker = list(option_rects.keys())[0]
                    first_option_rect, _ = option_rects[first_option_marker]
                    if question_final_rect.y1 > first_option_rect.y0:
                        question_final_rect.y1 = first_option_rect.y0 - margin / 2.0

                # --- Saving the snapshots now ---
                page_number_prefix = f"p{page_num+1:02d}"
                question_image_path = os.path.join(output_dir, f"{page_number_prefix}_{question_key}_Q.png")
                clip_rect_q = (question_final_rect + (-margin, -margin, margin, margin)) & page_rect
                pix_q = page.get_pixmap(dpi=dpi, clip=clip_rect_q)
                pix_q.save(question_image_path)

                option_image_paths = []
                for marker, (opt_rect, _) in option_rects.items():
                    option_image_path = os.path.join(output_dir, f"{page_number_prefix}_{question_key}_{marker}.png")
                    clip_rect_opt = (opt_rect + (-margin, -margin, margin, margin)) & page_rect
                    pix_opt = page.get_pixmap(dpi=dpi, clip=clip_rect_opt)
                    pix_opt.save(option_image_path)
                    option_image_paths.append(option_image_path)

                questions_data[question_key] = {
                    "page": page_num + 1,
                    "question_image": question_image_path,
                    "option_images": option_image_paths
                }

            i += 1

    doc.close()
    logging.info("Snapshot extraction completed.")
    #print(questions_data)
    return questions_data


#extract_question_snapshots('pdfs\CS224S6.pdf','question_images')