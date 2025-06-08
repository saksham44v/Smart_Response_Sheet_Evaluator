import json

# Load the original JSON data
with open("gate_cse_answer_key.json", "r") as f:
    data = json.load(f)

# Extract the list of marks from the PDF data in serial order (total 65 entries)
marks_list = (
    [1]*10 +           # Q1–Q10
    [1]*12 +           # Q11–Q22
    [1]*7 +            # Q23–Q29
    [1]*4 +            # Q30–Q33
    [1]*2 +            # Q34–Q35
    [2]*10 +           # Q36–Q45
    [2]*7 +            # Q46–Q52
    [2]*13             # Q53–Q65
)

# Now inject marks serial-wise into the JSON
question_ids = list(data.keys())
for i, qid in enumerate(question_ids):
    if i < len(marks_list):
        data[qid]["marks"] = float(marks_list[i])
    else:
        break  # If somehow extra questions exist

# Save the updated JSON
output_path = "gate_cse_answer_key_with_marks.json"
with open(output_path, "w") as f:
    json.dump(data, f, indent=2)

output_path
