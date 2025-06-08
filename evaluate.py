# def evaluate_responses(questions, correct_answers):
#   total_marks = 0
#   correct = incorrect = unattempted = 0

#   # Subject-wise scoring (Physics, Chemistry, Mathematics)
#   subject_scores = {"Physics": 0, "Chemistry": 0, "Mathematics": 0}
#   subject_questions = {"Physics": {"correct": 0, "incorrect": 0, "unattempted": 0},
#                        "Chemistry": {"correct": 0, "incorrect": 0, "unattempted": 0},
#                        "Mathematics": {"correct": 0, "incorrect": 0, "unattempted": 0}}

#   for q in questions:
#       q_id = q["question_id"]
#       q_type = q["question_type"]
#       subject = q["subject"]

#       if q_type == "MCQ":
#           chosen_option = q["chosen_option"]
#           if chosen_option == "--":
#               unattempted += 1
#               subject_questions[subject]["unattempted"] += 1
#               continue

#           chosen_option_id = q["option_ids"][int(chosen_option) - 1]
#           if correct_answers.get(q_id) == chosen_option_id:
#               correct += 1
#               total_marks += 4
#               subject_scores[subject] += 4
#               subject_questions[subject]["correct"] += 1
#           else:
#               incorrect += 1
#               total_marks -= 1
#               subject_scores[subject] -= 1
#               subject_questions[subject]["incorrect"] += 1

#       elif q_type == "SA":
#           given_answer = q["given_answer"]
#           if given_answer == "--":
#               unattempted += 1
#               subject_questions[subject]["unattempted"] += 1
#               continue

#           if correct_answers.get(q_id) == given_answer:
#               correct += 1
#               total_marks += 4
#               subject_scores[subject] += 4
#               subject_questions[subject]["correct"] += 1
#           else:
#               incorrect += 1
#               total_marks-=1
#               subject_scores[subject] -= 1
#               subject_questions[subject]["incorrect"] += 1

#   return {
#       "total_marks": total_marks,
#       "correct": correct,
#       "incorrect": incorrect,
#       "unattempted": unattempted,
#       "subject_scores": subject_scores,
#       "subject_questions": subject_questions
#   }


def evaluate_responses(questions, correct_answers):
    """
    Evaluates the JEE Mains responses and returns a dictionary containing all the data
    needed to populate the HTML placeholders in the frontend.

    Args:
        questions (list): A list of dictionaries, where each dictionary represents a question
                           and contains the question data extracted from the response sheet.
        correct_answers (dict): A dictionary containing the correct answers, where the keys
                             are the question IDs and the values are the correct answers.

    Returns:
        dict: A dictionary containing the following data:
            - total_score (int): The total score.
            - attempted (int): The total number of questions attempted.
            - correct (int): The total number of correct answers.
            - incorrect (int): The total number of incorrect answers.
            - skipped (int): The total number of questions skipped.
            - completed_percentage (float): The percentage of questions completed.
            - accuracy (float): The overall accuracy percentage.
            - subject_data (dict): A dictionary containing subject-wise analysis:
                {
                    "Physics": {
                        "score": int,
                        "attempted": int,
                        "correct": int,
                        "incorrect": int,
                        "accuracy": float
                    },
                    "Chemistry": { ... },
                    "Mathematics": { ... }
                }
    """
    total_marks = 0
    correct_count = 0
    incorrect_count = 0
    unattempted_count = 0
    total_questions = len(questions)

    subject_data = {
        "Physics": {"score": 0, "attempted": 0, "correct": 0, "incorrect": 0, "accuracy": 0},
        "Chemistry": {"score": 0, "attempted": 0, "correct": 0, "incorrect": 0, "accuracy": 0},
        "Mathematics": {"score": 0, "attempted": 0, "correct": 0, "incorrect": 0, "accuracy": 0},
    }

    for q in questions:
        q_id = q["question_id"]
        q_type = q["question_type"]
        subject = q["subject"]

        if q_type == "MCQ":
            chosen_option = q["chosen_option"]
            if chosen_option == "--":
                unattempted_count += 1
            else:
                subject_data[subject]["attempted"] += 1
                chosen_option_id = q["option_ids"][int(chosen_option) - 1]  # Get the option ID
                if correct_answers.get(q_id) == chosen_option_id:
                    correct_count += 1
                    total_marks += 4
                    subject_data[subject]["score"] += 4
                    subject_data[subject]["correct"] += 1
                else:
                    incorrect_count += 1
                    total_marks -= 1
                    subject_data[subject]["score"] -= 1
                    subject_data[subject]["incorrect"] += 1
        elif q_type == "SA":
            given_answer = q["given_answer"]
            if given_answer == "--":
                unattempted_count += 1
            else:
                subject_data[subject]["attempted"] += 1
                if correct_answers.get(q_id) == given_answer:
                    correct_count += 1
                    total_marks += 4
                    subject_data[subject]["score"] += 4
                    subject_data[subject]["correct"] += 1
                else:
                    incorrect_count += 1
                    total_marks -= 1
                    subject_data[subject]["score"] -= 1
                    subject_data[subject]["incorrect"] += 1

    attempted_count = 75-unattempted_count
    completed_percentage = round(((attempted_count / total_questions) * 100),2) if total_questions else 0
    accuracy = round(((correct_count / attempted_count) * 100),2) if attempted_count else 0

    for subject in subject_data:
        subject_attempted = subject_data[subject]["correct"] + subject_data[subject]["incorrect"]
        subject_data[subject]["accuracy"] = round(((subject_data[subject]["correct"] / subject_attempted) * 100),2) if subject_attempted else 0

    return {
        "total_score": total_marks,
        "attempted": attempted_count,
        "correct": correct_count,
        "incorrect": incorrect_count,
        "skipped": unattempted_count,
        "completed_percentage": completed_percentage,
        "accuracy": accuracy,
        "subject_data": subject_data,
    }
