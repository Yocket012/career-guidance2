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
        df_questions = pd.read_excel("30_Questions_test.xlsx", sheet_name="Questions")
        df_weights = pd.read_excel("30_Questions_test.xlsx", sheet_name="Weights")
    except FileNotFoundError:
        print("\nError: '30_Questions_test.xlsx' not found. Please ensure the file is in the correct directory.")
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

    # Calculate scores
    role_type_scores = {role: 0 for role in df_weights['Role Type'].unique()}
    career_line_scores = {line: 0 for line in df_weights['Career Line'].unique()}

    for i, answer in enumerate(answers):
        question_weights = df_weights[df_weights['Question No.'] == i + 1]
        selected_option_weights = question_weights[question_weights['Option'] == answer]

        for _, row in selected_option_weights.iterrows():
            if pd.notna(row['Role Type']):
                role_type_scores[row['Role Type']] += 1
            if pd.notna(row['Career Line']):
                career_line_scores[row['Career Line']] += 1

    dominant_role_type = max(role_type_scores, key=role_type_scores.get)
    dominant_career_line = max(career_line_scores, key=career_line_scores.get)

    return dominant_role_type, dominant_career_line

def determine_subject_interest(academic_scores):
    """Determines the student's primary subject interest."""
    stem_subjects = ["Maths", "Physics", "Chemistry", "Biology", "Statistics", "Computer Science"]
    humanities_subjects = ["History", "Civics", "Geography", "Economics", "English"]
    arts_subjects = [] # Can be expanded based on available subjects

    stem_score = sum(score for subject, score in academic_scores.items() if subject in stem_subjects)
    humanities_score = sum(score for subject, score in academic_scores.items() if subject in humanities_subjects)
    # arts_score = sum(score for subject, score in academic_scores.items() if subject in arts_subjects)

    if stem_score >= humanities_score:
        return "STEM"
    else:
        return "Humanities"


def generate_career_report(subject_interest, role_type, career_line):
    """Generates a career report based on the test results."""
    try:
        df_guidance = pd.read_excel("Career Guidance Test.xlsx", sheet_name="Guidance")
    except FileNotFoundError:
        print("\nError: 'Career Guidance Test.xlsx' not found. Please ensure the file is in the correct directory.")
        return

    report = df_guidance[
        (df_guidance['Subject Interest'] == subject_interest) &
        (df_guidance['Role Type'] == role_type) &
        (df_guidance['Career Line'] == career_line)
    ]

    if not report.empty:
        report_data = report.iloc[0]
        print("\n--- Your Personalized Career Guidance Report ---")
        print(f"\nMessage: {report_data['Message']}")
        print(f"\nExample Career Options: {report_data['Example Career Options']}")
        print(f"\nPotential Companies to Aim For: {report_data['Potential Companies to Aim For']}")
        print(f"\nEntry-Level Designations: {report_data['Entry-Level Designations']}")
        print(f"\nTop Universities in India: {report_data['Top Universities India']}")
        print(f"\nTop Universities Abroad: {report_data['Top Universities Abroad']}")
    else:
        print("\nCould not find a specific career recommendation for your combination of results.")
        print("This may indicate a unique profile. Consider exploring interdisciplinary fields.")

if __name__ == "__main__":
    print("--- Welcome to the Psychometric Career Guidance Test ---")

    # Step 1: Personal Info
    name, number = get_personal_info()

    # Step 2: Academic Scores
    academic_scores = get_academic_scores()

    # Step 3: MCQ Test
    role_type, career_line = run_mcq_test()

    if role_type and career_line:
        # Determine Subject Interest
        subject_interest = determine_subject_interest(academic_scores)

        # Display Results
        print("\n--- Your Test Results ---")
        print(f"Name: {name}")
        print(f"Mobile Number: {number}")
        print(f"Subject Interest: {subject_interest}")
        print(f"Dominant Role Type: {role_type}")
        print(f"Dominant Career Line: {career_line}")

        # Generate and display the final report
        generate_career_report(subject_interest, role_type, career_line)
