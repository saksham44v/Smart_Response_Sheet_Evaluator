import numpy as np
from sentence_transformers import SentenceTransformer
from sklearn.metrics.pairwise import cosine_similarity
import re

# Predefined tags as provided in the query
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

# Load pre-trained SBERT model
model = SentenceTransformer('all-MiniLM-L6-v2')

# Function to preprocess text
def preprocess_text(text):
    text = re.sub(r'\s+', ' ', text)  # Remove extra spaces
    text = text.lower().strip()       # Lowercase and strip
    return text

# Generate embeddings for all tags
def generate_tag_embeddings():
    tag_embeddings = {}
    for subject, chapters in predefined_tags.items():
        tag_embeddings[subject] = {}
        for chapter, subtopics in chapters.items():
            tag_embeddings[subject][chapter] = {}
            for subtopic in subtopics:
                embedding = model.encode(subtopic)
                tag_embeddings[subject][chapter][subtopic] = embedding
    return tag_embeddings

# Compute similarity and assign tags
def assign_tags(question, tag_embeddings):
    question = preprocess_text(question)
    question_embedding = model.encode(question)
    
    best_subject = None
    best_chapter = None
    best_subtopic = None
    max_similarity = -1
    
    for subject, chapters in tag_embeddings.items():
        for chapter, subtopics in chapters.items():
            for subtopic, embedding in subtopics.items():
                similarity = cosine_similarity([question_embedding], [embedding])[0][0]
                if similarity > max_similarity:
                    max_similarity = similarity
                    best_subject = subject
                    best_chapter = chapter
                    best_subtopic = subtopic
    
    return best_subject, best_chapter, best_subtopic, max_similarity

# Example usage
if __name__ == "__main__":
    tag_embeddings = generate_tag_embeddings()
    question = "Space between the plates of a parallel plate capacitor of plate area 4 cm2 and separation of 1.77 mm, is filled with uniform dielectric materials with dielectric constants (3 and 5) as shown in figure. Another capacitor of capacitance 7.5 pF is connected in parallel with it. The effective capacitance of this combination is _ pF.(Given F/m) give this question a tag for which unit of jee syllabus this topic is and from which subtopic"
    subject, chapter, subtopic, similarity = assign_tags(question, tag_embeddings)
    print(f"Question: {question}")
    print(f"Assigned Tags: Subject={subject}, Chapter={chapter}, Subtopic={subtopic}, Similarity={similarity:.4f}")