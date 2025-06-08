import pytesseract
from PIL import Image
import re
from sentence_transformers import SentenceTransformer, util

# --- Step 1: Define your predefined topic list ---
predefined_tags = {
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

# --- Step 2: Flatten topic list ---
flat_topics = []
topic_map = []

for subject, chapters in predefined_tags.items():
    for chapter, topics in chapters.items():
        for topic in topics:
            flat_topics.append(f"{subject} → {chapter} → {topic}")
            topic_map.append((subject, chapter, topic))

# --- Step 3: Load Sentence Transformer ---
model = SentenceTransformer("all-MiniLM-L6-v2")

# --- Step 4: OCR Function ---
def extract_text_from_image(image_path):
    image = Image.open(image_path).convert("RGB")
    text = pytesseract.image_to_string(image)
    text = re.sub(r'\s+', ' ', text).strip()
    return text

# --- Step 5: Predict Function ---
def predict_topic_from_image(image_path):
    question_text = extract_text_from_image(image_path)
    print("Extracted Question Text:\n", question_text)

    if not question_text:
        return "Could not read the question properly."

    # Encode question and topics
    question_embedding = model.encode(question_text, convert_to_tensor=True)
    topic_embeddings = model.encode(flat_topics, convert_to_tensor=True)

    # Compute similarity
    cosine_scores = util.cos_sim(question_embedding, topic_embeddings)[0]
    best_match_idx = cosine_scores.argmax()
    best_score = cosine_scores[best_match_idx].item()

    subject, chapter, topic = topic_map[best_match_idx]

    return {
        "predicted_subject": subject,
        "chapter": chapter,
        "topic": topic,
        "similarity_score": round(best_score, 3)
    }

# --- Example usage ---
if __name__ == "__main__":
    img_path = "/content/7364751051.jpg"  # Replace with your path
    prediction = predict_topic_from_image(img_path)
    print("\nPrediction:\n", prediction)

#using this method the accuracy is low
