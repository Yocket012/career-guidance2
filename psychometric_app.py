import pandas as pd

def get_personal_info():
    """Gets the student's name and number."""
    name = input("Enter your full name: ")
    while True:
        number = input("Enter your 10-digit mobile number: ")
        if number.isdigit() and len(number) == 10:
            break
        else:
            print("Invalid mobile number. Please enter a 10-digit number.")
    return name, number

def get_academic_scores():
    """Gets the student's academic scores for their top 5 subjects."""
    subjects = [
        "Maths", "Physics", "Chemistry", "Biology", "History", "Civics",
        "Geography", "Economics", "Statistics", "Computer Science", "English"
    ]
    selected_subjects = {}
    print("\nPlease select your top 5 subjects from the list below and enter your scores (out of 100).")
    for i in range(5):
        while True:
            print("\nAvailable subjects:", ", ".join(subjects))
            subject = input(f"Enter subject {i+1}: ").strip().title()
            if subject in subjects and subject not in selected_subjects:
                while True:
                    try:
                        score = float(input(f"Enter score for {subject}: "))
                        if 0 <= score <= 100:
                            selected_subjects[subject] = score
                            break
                        else:
                            print("Invalid score. Please enter a number between 0 and 100.")
                    except ValueError:
                        print("Invalid input. Please enter a number.")
                break
            elif subject in selected_subjects:
                print("You have already entered a score for this subject.")
            else:
                print("Invalid subject. Please choose from the list.")
    return selected_subjects

def run_mcq_test():
    """Conducts the 30-question MCQ test and calculates scores."""
    try:
        df_questions = pd.read_csv("30-Questions_test.xlsx - questions_set.csv")
        df_weights = pd.read_csv("30-Questions_test.xlsx - weights_set.csv")
    except FileNotFoundError:
        print("\nError: Could not find the necessary test files.")
        return None, None

    answers = []
    print("\n--- Psychometric Test ---")
    print("Please answer the following 30 questions.")
    for index, row in df_questions.iterrows():
        print(f"\nQ{index+1}: {row['Question']}")
        print(f"  A. {row['Option A']}")
        print(f"  B. {row['Option B']}")
        print(f"  C. {row['Option C']}")
        print(f"  D. {row['Option D']}")
        while True:
            answer = input("Your choice (A/B/C/D): ").upper()
            if answer in ['A', 'B', 'C', 'D']:
                answers.append(answer)
                break
            else:
                print("Invalid choice. Please enter A, B, C, or D.")

    # Initialize score dictionaries
    role_types = ['Creative', 'Specialist', 'Generalist', 'Administrative',
                  'Entrepreneurial', 'Customer Service', 'Technical',
                  'Human Resources', 'Sales/Marketing', 'Leadership', 'Other']
    career_lines = ['Linear', 'Non-linear', 'Diagonal', 'Horizontal']
    role_type_scores = {role: 0 for role in role_types}
    career_line_scores = {line: 0 for line in career_lines}

    # Calculate scores
    for i, answer in enumerate(answers):
        weights_str = df_weights.loc[i, f'Option {answer} Weights']
        if isinstance(weights_str, str):
            parts = weights_str.split(', ')
            for part in parts:
                key, value = part.split(' = ')
                if key in role_type_scores:
                    role_type_scores[key] += int(value)
                elif key in career_line_scores:
                    career_line_scores[key] += int(value)

    dominant_role_type = max(role_type_scores, key=role_type_scores.get)
    dominant_career_line = max(career_line_scores, key=career_line_scores.get)

    return dominant_role_type, dominant_career_line


def determine_subject_interest(academic_scores):
    """Determines the student's primary subject interest."""
    stem_subjects = ["Maths", "Physics", "Chemistry", "Biology", "Statistics", "Computer Science"]
    humanities_subjects = ["History", "Civics", "Geography", "Economics", "English"]

    stem_score = sum(score for subject, score in academic_scores.items() if subject in stem_subjects)
    humanities_score = sum(score for subject, score in academic_scores.items() if subject in humanities_subjects)

    if stem_score > humanities_score:
        return "STEM"
    else:
        return "Humanities"

def generate_career_report(subject_interest, role_type, career_line):
    """Generates a career report based on the test results."""
    try:
        if subject_interest == "STEM":
            df_guidance = pd.read_csv("Career Guidance Test.xlsx - stem_set.csv")
        elif subject_interest == "Humanities":
            df_guidance = pd.read_csv("Career Guidance Test.xlsx - humanities_set.csv")
        else: # Assuming 'Art' is the other option
            df_guidance = pd.read_csv("Career Guidance Test.xlsx - arts_set.csv")
    except FileNotFoundError:
        print(f"\nError: Could not find the guidance file for '{subject_interest}'.")
        return

    report = df_guidance[
        (df_guidance['Role Type'] == role_type) &
        (df_guidance['Career Line'] == career_line)
    ]

    if not report.empty:
        report_data = report.iloc[0]
        print("\n\n--- Your Personalized Career Guidance Report ---")
        print(f"\nMessage: {report_data['Message']}")
        print(f"\nExample Career Options: {report_data['Example Career Options']}")
        print(f"\nPotential Companies to Aim For: {report_data['Potential Companies to Aim For']}")
        print(f"\nEntry-Level Designations: {report_data['Entry-Level Designations']}")
        print(f"\nTop Universities in India: {report_data['Top Universities India']}")
        print(f"\nTop Universities Abroad: {report_data['Top Universities  Globally']}") # Corrected column name
    else:
        print("\nCould not find a specific career recommendation for your unique combination of results.")
        print("This may indicate a very special profile. We encourage you to explore interdisciplinary fields "
              "that blend your interests and strengths.")

if __name__ == "__main__":
    print("--- Welcome to the Psychometric Career Guidance Test ---")

    name, number = get_personal_info()
    academic_scores = get_academic_scores()
    role_type, career_line = run_mcq_test()

    if role_type and career_line:
        subject_interest = determine_subject_interest(academic_scores)

        print("\n--- Your Test Results ---")
        print(f"\nName: {name}")
        print(f"Mobile Number: {number}")
        print(f"\nYour Academic Interest Area: {subject_interest}")
        print(f"Your Dominant Role Type: {role_type}")
        print(f"Your Natural Career Line: {career_line}")

        generate_career_report(subject_interest, role_type, career_line)
