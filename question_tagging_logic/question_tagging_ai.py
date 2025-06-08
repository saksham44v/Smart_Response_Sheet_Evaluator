# import os
# import json
# import google.generativeai as genai
# from PIL import Image
# from tqdm import tqdm

# # Path to your Google Gemini API key (replace with your actual key or use env variable)
# API_KEY = "AIzaSyAujAacxeeCuH09wi8M7-17aKj6vBJ-YDg"
# genai.configure(api_key=API_KEY)

# # Load the model
# model = genai.GenerativeModel("gemini-2.0-flash")

# # Load the existing question data with image paths and subjects
# with open("question_tagging_logic\question_data.json", "r") as f:
#     question_data = json.load(f)

# predefined_tags_list = {
#     "Physics": {
#         "Units & Measurements": [
#             "Units and Measurements", "Vector Algebra"
#         ],
#         "Mechanics": [
#             "Motion in a Straight Line", "Motion in a Plane", "Circular Motion",
#             "Laws of Motion", "Work, Power & Energy", "Center of Mass and Collision",
#             "Rotational Motion", "Gravitation", "Properties of Matter"
#         ],
#         "Thermodynamics & Kinetic Theory": [
#             "Heat and Thermodynamics", "Thermal Expansion",
#             "Calorimetry", "Kinetic Theory of Gases"
#         ],
#         "Oscillations & Waves": [
#             "Simple Harmonic Motion", "Waves", "Sound Waves", "Doppler Effect"
#         ],
#         "Electrodynamics": [
#             "Electrostatics", "Current Electricity", "Capacitors",
#             "Magnetism and Magnetic Effects of Current",
#             "Electromagnetic Induction", "Alternating Current"
#         ],
#         "Optics": [
#             "Ray Optics", "Wave Optics"
#         ],
#         "Modern Physics": [
#             "Dual Nature of Matter & Radiation", "Nuclear Physics",
#             "Semiconductor Electronics", "Modern Physics"
#         ]
#     },

#     "Chemistry": {
#         "Physical Chemistry": [
#             "Some Basic Concepts of Chemistry", "Structure of Atom",
#             "States of Matter: Gases and Liquids", "Thermodynamics",
#             "Chemical Equilibrium", "Ionic Equilibrium", "Redox Reactions",
#             "Electrochemistry", "Chemical Kinetics", "Solid State",
#             "Surface Chemistry", "Solutions", "Colloids"
#         ],
#         "Inorganic Chemistry": [
#             "Periodic Table and Periodicity in Properties", "Hydrogen",
#             "The s-Block Element", "The p-Block Element",
#             "The d-Block and f-Block Elements", "Coordination Compounds",
#             "Metallurgy", "Environmental Chemistry", "Qualitative Analysis"
#         ],
#         "Organic Chemistry": [
#             "General Organic Chemistry", "Isomerism", "Hydrocarbons",
#             "Haloalkanes and Haloarenes", "Alcohols, Phenols and Ethers",
#             "Aldehydes, Ketones and Carboxylic Acids", "Amines",
#             "Biomolecules", "Polymers", "Chemistry in Everyday Life",
#             "Practical Organic Chemistry"
#         ]
#     },

#     "Mathematics": {
#         "Algebra": [
#             "Sets, Relations and Functions", "Complex Numbers",
#             "Quadratic Equations", "Sequences and Series",
#             "Binomial Theorem", "Permutations and Combinations",
#             "Mathematical Induction", "Logarithm"
#         ],
#         "Matrices & Determinants": [
#             "Matrices", "Determinants"
#         ],
#         "Trigonometry": [
#             "Trigonometric Ratios and Identities",
#             "Inverse Trigonometric Functions", "Properties of Triangles"
#         ],
#         "Coordinate Geometry": [
#             "Straight Lines", "Circles", "Parabola", "Ellipse", "Hyperbola", "3D Geometry"
#         ],
#         "Calculus": [
#             "Limits and Continuity", "Differentiation", "Applications of Derivatives",
#             "Integration", "Definite Integrals", "Differential Equations",
#             "Area Under Curves"
#         ],
#         "Vector Algebra": [
#             "Vector Algebra"
#         ],
#         "Statistics & Probability": [
#             "Statistics", "Probability"
#         ],
#         "Mathematical Reasoning": [
#             "Mathematical Reasoning"
#         ]
#     }
# }


# # Initialize output dict
# tagged_question_data = {}

# # --- Iterate through each shift ---
# for exam_date, shifts in tqdm(question_data.items(), desc="Processing Exam Dates"):
#     tagged_question_data.setdefault(exam_date, {})
#     for slot_time, questions in tqdm(shifts.items(), desc=f"Processing Slots - {exam_date}"):
#         tagged_question_data[exam_date].setdefault(slot_time, {})
#         for qid, qinfo in tqdm(questions.items(), desc=f"Tagging Questions - {exam_date} {slot_time}", leave=False):
#             image_path = os.path.join("question_tagging_logic\question_image_data", exam_date+"_"+slot_time, f"{qid}.jpg")

#             if not os.path.exists(image_path):
#                 print(f"[Skip] Image not found: {image_path}")    #question_tagging_logic\question_image_data\02-04-2025_3-00_PM\603421226.jpg
#                 continue

#             try:
#                 # Load image and prepare request
#                 with Image.open(image_path) as img:
#                     prompt = (
#                         f"You are tagging JEE question images. Choose the best matching tag from the list below.\n\n"
#                         f"Predefined Tags:\n{', '.join(predefined_tags_list)}\n\n"
#                         f"Your response should be:\nTag: <one exact tag from list>\nConcept: <short topic/concept>"
#                     )
#                     print("yaha ayya1")

#                     response = model.generate_content([
#                         {"mime_type": "image/jpg", "data": img.tobytes()},
#                         prompt
#                     ])

#                     print("yaha ayya 2")

#                     tagged_question_data[exam_date][slot_time][qid] = {
#                         "question_image_url": qinfo["question_image_url"],
#                         "subject": qinfo["subject"],
#                         "predicted_tag_info": response.text.strip()
#                     }

#             except Exception as e:
#                 print(f"[Error] Failed to process QID {qid}: {e}")

# # Save to a new JSON file
# with open("question_tagging_logic\tagged_question_data.json", "w") as f:
#     json.dump(tagged_question_data, f, indent=2)
# print("\n✅ All questions tagged and saved to 'tagged_question_data.json'")






import os
import json
from PIL import Image
from tqdm import tqdm
import google.generativeai as genai
from google.generativeai.types import Part




# === Configuration ===
API_KEY = "YOUR_API_KEY_HERE"
genai.configure(api_key=API_KEY)

# Use the correct model
model = genai.GenerativeModel("gemini-2.0-flash")

# Load question data
with open("question_tagging_logic/question_data.json", "r") as f:
    question_data = json.load(f)

# Use predefined nested tag list
predefined_tags_list = {
    "Physics": {
        "Units & Measurements": [
            "Units and Measurements", "Vector Algebra"
        ],
        "Mechanics": [
            "Motion in a Straight Line", "Motion in a Plane", "Circular Motion",
            "Laws of Motion", "Work, Power & Energy", "Center of Mass and Collision",
            "Rotational Motion", "Gravitation", "Properties of Matter"
        ],
        "Thermodynamics & Kinetic Theory": [
            "Heat and Thermodynamics", "Thermal Expansion",
            "Calorimetry", "Kinetic Theory of Gases"
        ],
        "Oscillations & Waves": [
            "Simple Harmonic Motion", "Waves", "Sound Waves", "Doppler Effect"
        ],
        "Electrodynamics": [
            "Electrostatics", "Current Electricity", "Capacitors",
            "Magnetism and Magnetic Effects of Current",
            "Electromagnetic Induction", "Alternating Current"
        ],
        "Optics": [
            "Ray Optics", "Wave Optics"
        ],
        "Modern Physics": [
            "Dual Nature of Matter & Radiation", "Nuclear Physics",
            "Semiconductor Electronics", "Modern Physics"
        ]
    },

    "Chemistry": {
        "Physical Chemistry": [
            "Some Basic Concepts of Chemistry", "Structure of Atom",
            "States of Matter: Gases and Liquids", "Thermodynamics",
            "Chemical Equilibrium", "Ionic Equilibrium", "Redox Reactions",
            "Electrochemistry", "Chemical Kinetics", "Solid State",
            "Surface Chemistry", "Solutions", "Colloids"
        ],
        "Inorganic Chemistry": [
            "Periodic Table and Periodicity in Properties", "Hydrogen",
            "The s-Block Element", "The p-Block Element",
            "The d-Block and f-Block Elements", "Coordination Compounds",
            "Metallurgy", "Environmental Chemistry", "Qualitative Analysis"
        ],
        "Organic Chemistry": [
            "General Organic Chemistry", "Isomerism", "Hydrocarbons",
            "Haloalkanes and Haloarenes", "Alcohols, Phenols and Ethers",
            "Aldehydes, Ketones and Carboxylic Acids", "Amines",
            "Biomolecules", "Polymers", "Chemistry in Everyday Life",
            "Practical Organic Chemistry"
        ]
    },

    "Mathematics": {
        "Algebra": [
            "Sets, Relations and Functions", "Complex Numbers",
            "Quadratic Equations", "Sequences and Series",
            "Binomial Theorem", "Permutations and Combinations",
            "Mathematical Induction", "Logarithm"
        ],
        "Matrices & Determinants": [
            "Matrices", "Determinants"
        ],
        "Trigonometry": [
            "Trigonometric Ratios and Identities",
            "Inverse Trigonometric Functions", "Properties of Triangles"
        ],
        "Coordinate Geometry": [
            "Straight Lines", "Circles", "Parabola", "Ellipse", "Hyperbola", "3D Geometry"
        ],
        "Calculus": [
            "Limits and Continuity", "Differentiation", "Applications of Derivatives",
            "Integration", "Definite Integrals", "Differential Equations",
            "Area Under Curves"
        ],
        "Vector Algebra": [
            "Vector Algebra"
        ],
        "Statistics & Probability": [
            "Statistics", "Probability"
        ],
        "Mathematical Reasoning": [
            "Mathematical Reasoning"
        ]
    }
}
# --- Format tag list as string for prompt ---
formatted_tags = ""
for subject, chapters in predefined_tags_list.items():
    formatted_tags += f"{subject}:\n"
    for chapter, topics in chapters.items():
        formatted_tags += f"  {chapter}:\n"
        for topic in topics:
            formatted_tags += f"    - {topic}\n"

# Output dictionary
tagged_question_data = {}

# === Tagging Logic ===
for exam_date, shifts in tqdm(question_data.items(), desc="Processing Exam Dates"):
    tagged_question_data.setdefault(exam_date, {})
    for slot_time, questions in tqdm(shifts.items(), desc=f"Slots on {exam_date}"):
        tagged_question_data[exam_date].setdefault(slot_time, {})
        for qid, qinfo in tqdm(questions.items(), desc=f"Tagging {exam_date} {slot_time}", leave=False):
            image_path = os.path.join("question_tagging_logic", "question_image_data", f"{exam_date}_{slot_time}", f"{qid}.jpg")

            if not os.path.exists(image_path):
                print(f"[Skip] Image not found: {image_path}")
                continue

            try:
                with Image.open(image_path).convert("RGB") as img:
                    prompt = (
                        "You are tagging a JEE image-based question. Choose the best matching topic from the list below.\n\n"
                        + formatted_tags +
                        "\n\nReturn your response in this format:\n"
                        "Tag: <exact topic from the list>\nConcept: <brief concept from question>"
                    )

                    # Prepare Gemini-style image + prompt
                    response = model.generate_content([
                        genai.types.content.Part.from_image(img),
                        genai.types.content.Part(text=prompt)
                    ])

                    tagged_question_data[exam_date][slot_time][qid] = {
                        "question_image_url": qinfo["question_image_url"],
                        "subject": qinfo["subject"],
                        "predicted_tag_info": response.text.strip()
                    }

            except Exception as e:
                print(f"[Error] Failed for QID {qid}: {e}")

# Save tagged data
output_path = "question_tagging_logic/tagged_question_data.json"
with open(output_path, "w") as f:
    json.dump(tagged_question_data, f, indent=2)

print(f"\n✅ Tagging complete. Saved to '{output_path}'")
