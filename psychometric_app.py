import pandas as pd
from fpdf import FPDF
from collections import Counter

def run_psychometric_test():
    """
    This function runs the psychometric test, collects user data,
    and generates a career guidance report in PDF format.
    """

    # --- 1. Load Data ---
    try:
        questions_df = pd.read_csv("30-Questions_test.xlsx - questions_set.csv")
        weights_df = pd.read_csv("30-Questions_test.xlsx - weights_set.csv")
        stem_df = pd.read_csv("Career Guidance Test.xlsx - stem_set.csv")
        humanities_df = pd.read_csv("Career Guidance Test.xlsx - humanities_set.csv")
        arts_df = pd.read_csv("Career Guidance Test.xlsx - arts_set.csv")
    except FileNotFoundError as e:
        print(f"Error loading data files: {e}")
        return

    # --- 2. Personal and Academic Info (Simulated) ---
    student_name = "Test User"
    student_number = "1234567890"
    academic_scores = {
        "Maths": 95,
        "Physics": 92,
        "Chemistry": 88,
        "Computer Science": 98,
        "English": 85,
    }

    # --- 3. Determine Subject Interest ---
    subject_categories = {
        "STEM": ["Maths", "Physics", "Chemistry", "Biology", "Computer Science", "Statistics"],
        "Humanities": ["History", "Civics", "Geography", "Economics"],
        "Arts": ["English"],
    }

    def get_subject_interest(scores):
        category_scores = {"STEM": 0, "Humanities": 0, "Arts": 0}
        for subject in scores:
            for category, subjects_in_category in subject_categories.items():
                if subject in subjects_in_category:
                    category_scores[category] += 1
        return max(category_scores, key=category_scores.get)

    subject_interest = get_subject_interest(academic_scores)

    # --- 4. Psychometric Test (Simulated Answers) ---
    answers = ['a'] * 30  # Simulate answering 'a' for all questions
    
    role_type_answers = []
    career_line_answers = []

    option_map = {
        'a': 'Option A Weights',
        'b': 'Option B Weights',
        'c': 'Option C Weights',
        'd': 'Option D Weights'
    }

    for i, answer_choice in enumerate(answers):
        question_number = i + 1
        weight_row = weights_df[weights_df['Q#'] == question_number]
        
        if not weight_row.empty:
            career_line = weight_row.iloc[0]['Theme']
            career_line_answers.append(career_line)
            
            option_column = option_map.get(answer_choice.lower())
            if option_column and option_column in weight_row:
                role_type_string = weight_row.iloc[0][option_column]
                if isinstance(role_type_string, str):
                    roles = role_type_string.split(',')
                    for role in roles:
                        role_name = role.split('=')[0].strip()
                        role_type_answers.append(role_name)
                else:
                    role_type_answers.append(role_type_string)

    determined_role_type = Counter(role_type_answers).most_common(1)[0][0]
    determined_career_line = Counter(career_line_answers).most_common(1)[0][0]


    # --- 5. Get Career Guidance ---
    def get_career_guidance(interest, role, line):
        df = None
        if interest == "STEM":
            df = stem_df.rename(columns={'Top Universities  Globally': 'Top Universities Abroad'})
        elif interest == "Humanities":
            df = humanities_df
        elif interest == "Arts":
            df = arts_df

        if df is not None:
            guidance = df[(df['Role Type'] == role) & (df['Career Line'] == line)]
            if not guidance.empty:
                return guidance.iloc[0]
        return None

    career_guidance = get_career_guidance(subject_interest, determined_role_type, determined_career_line)

    # --- 6. Generate PDF Report ---
    class PDF(FPDF):
        def header(self):
            self.set_font('Arial', 'B', 12)
            self.cell(0, 10, 'Psychometric Test Report', 1, 1, 'C')

        def chapter_title(self, title):
            self.set_font('Arial', 'B', 12)
            self.cell(0, 10, title, 0, 1, 'L')
            self.ln(5)

        def chapter_body(self, body):
            self.set_font('Arial', '', 12)
            body = str(body).encode('latin-1', 'replace').decode('latin-1')
            self.multi_cell(0, 10, body)
            self.ln()

        def add_section(self, title, content):
            self.chapter_title(title)
            if isinstance(content, dict):
                for key, value in content.items():
                    self.chapter_body(f"{key}: {value}")
            else:
                self.chapter_body(content)

    pdf = PDF()
    pdf.add_page()

    pdf.add_section("Personal Information", {"Name": student_name, "Number": student_number})
    pdf.add_section("Academic Scores", academic_scores)
    pdf.add_section("Determined Subject Interest", subject_interest)
    pdf.add_section("Psychometric Test Results", {
        "Determined Role Type": determined_role_type,
        "Determined Career Line": determined_career_line,
    })

    if career_guidance is not None:
        pdf.add_section("Career Guidance Message", career_guidance.get('Message', 'N/A'))
        pdf.add_section("Example Career Options", career_guidance.get('Example Career Options', 'N/A'))
        pdf.add_section("Potential Companies to Aim For", career_guidance.get('Potential Companies to Aim For', 'N/A'))
        pdf.add_section("Entry-Level Designations", career_guidance.get('Entry-Level Designations', 'N/A'))
        pdf.add_section("Top Universities in India", career_guidance.get('Top Universities India', 'N/A'))
        pdf.add_section("Top Universities Abroad", career_guidance.get('Top Universities Abroad', 'N/A'))
    else:
        pdf.add_section("Career Guidance", "No specific guidance found for this combination.")

    report_filename = "psychometric_report_final.pdf"
    pdf.output(report_filename)
    print(f"Final report generated: {report_filename}")

# Run the test
run_psychometric_test()
