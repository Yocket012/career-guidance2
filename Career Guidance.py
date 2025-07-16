import streamlit as st
import pandas as pd
from fpdf import FPDF
import os

def calculate_scores(responses, questions):
    score_categories = {
        "STEM": 0, "Humanities": 0, "Business": 0, "Creative": 0,
        "Specialist": 0, "Leadership": 0, "Creative_Role": 0, "Admin": 0,
        "Technical": 0, "Generalist": 0
    }
    for q_num, ans in responses.items():
        tags = questions[q_num]["options"][ans]
        for tag in tags:
            score_categories[tag] += 1
    return score_categories

def generate_pdf_report(scores, academic_scores, student_name):
    pdf = FPDF()
    pdf.add_page()
    pdf.set_font("Arial", size=12)

    pdf.cell(200, 10, f"Career Guidance Report for {student_name}", ln=True, align='C')
    pdf.ln(10)

    pdf.set_font("Arial", 'B', 12)
    pdf.cell(200, 10, "Top Career Inclinations:", ln=True)
    top_domains = sorted(scores.items(), key=lambda x: x[1], reverse=True)[:3]
    for domain, score in top_domains:
        pdf.set_font("Arial", size=11)
        pdf.cell(200, 10, f"{domain}: {score}", ln=True)

    pdf.ln(5)
    pdf.set_font("Arial", 'B', 12)
    pdf.cell(200, 10, "Academic Scores Snapshot:", ln=True)
    pdf.set_font("Arial", size=10)
    for index, row in academic_scores.iterrows():
        pdf.cell(200, 10,
                 f"{row['Subject']}: Class 9 - {row['Class 9 (%)']}%, Class 10 - {row['Class 10 (%)']}%",
                 ln=True)

    major_minor = {
        ("STEM", "Business"): ("Computer Science", "Business Analytics"),
        ("Humanities", "Creative"): ("Psychology", "Media Studies"),
        ("Creative", "Business"): ("Design", "Marketing"),
    }
    top_tags = tuple(sorted([d[0] for d in top_domains if d[0] in ["STEM", "Humanities", "Creative", "Business"]])[:2])
    major, minor = major_minor.get(top_tags, ("General Studies", "Communication"))

    pdf.ln(5)
    pdf.set_font("Arial", 'B', 12)
    pdf.cell(200, 10, "Suggested Major & Minor:", ln=True)
    pdf.set_font("Arial", size=11)
    pdf.cell(200, 10, f"Major: {major}", ln=True)
    pdf.cell(200, 10, f"Minor: {minor}", ln=True)

    pdf.ln(5)
    pdf.set_font("Arial", 'B', 12)
    pdf.cell(200, 10, "Top Global Universities:", ln=True)
    universities = {
        "Computer Science": ["University of Toronto", "University of Michigan", "NUS"],
        "Psychology": ["UCL", "University of Amsterdam", "University of British Columbia"],
        "Design": ["Parsons School of Design", "RMIT", "University of the Arts London"],
        "General Studies": ["Arizona State University", "Monash University", "York University"]
    }
    for uni in universities.get(major, []):
        pdf.set_font("Arial", size=10)
        pdf.cell(200, 10, f"- {uni}", ln=True)

    pdf.ln(5)
    pdf.set_font("Arial", 'B', 12)
    pdf.cell(200, 10, "Career Paths & Entry Roles:", ln=True)
    if major == "Computer Science":
        careers = ["Product Analyst at Google", "Data Analyst at Amazon", "Software Intern at Atlassian"]
    elif major == "Psychology":
        careers = ["Research Assistant at WHO", "Policy Analyst at UNDP", "Behavioural Analyst at Deloitte"]
    elif major == "Design":
        careers = ["UX Designer at Canva", "Visual Designer at Ogilvy", "Intern at IDEO"]
    else:
        careers = ["Content Creator", "Program Manager", "Marketing Intern"]

    for job in careers:
        pdf.set_font("Arial", size=10)
        pdf.cell(200, 10, f"- {job}", ln=True)

    pdf.ln(5)
    pdf.set_font("Arial", 'I', 11)
    pdf.multi_cell(0, 10, "You're on the path to a promising global career. Continue exploring your strengths and building real-world exposure. Your journey has just begun!")

    file_path = f"/mnt/data/{student_name.replace(' ', '_')}_Career_Report.pdf"
    pdf.output(file_path)
    return file_path

st.title("Class 9–10 Career Guidance Psychometric Test")
student_name = st.text_input("Enter your name")

questions = {
    1: {"question": "How do you prefer to start your school projects?", "options": {"A": ["Admin"], "B": ["Creative"], "C": ["Specialist"], "D": ["Generalist"]}},
    2: {"question": "When working in a group, what role do you usually take?", "options": {"A": ["Leadership"], "B": ["Specialist"], "C": ["Creative"], "D": ["Admin"]}},
    3: {"question": "What motivates you to complete a task?", "options": {"A": ["Leadership"], "B": ["Specialist"], "C": ["Technical"], "D": ["Admin"]}},
    4: {"question": "You’re given a topic to present. You would:", "options": {"A": ["Creative"], "B": ["Specialist"], "C": ["Admin"], "D": ["Generalist"]}},
    5: {"question": "What frustrates you the most in a school setting?", "options": {"A": ["Admin"], "B": ["Creative"], "C": ["Specialist"], "D": ["Generalist"]}},
    6: {"question": "You enjoy subjects that are:", "options": {"A": ["Technical"], "B": ["Creative"], "C": ["Admin"], "D": ["Specialist"]}},
    7: {"question": "Which subject do you enjoy the most?", "options": {"A": ["STEM"], "B": ["Humanities"], "C": ["Creative"], "D": ["Business"]}},
    8: {"question": "How do you usually score in Math?", "options": {"A": ["STEM"], "B": ["STEM"], "C": ["STEM"], "D": ["STEM"]}},
    9: {"question": "Which best describes your learning style?", "options": {"A": ["STEM"], "B": ["Creative"], "C": ["Humanities"], "D": ["Business"]}},
    10: {"question": "Which activity do you enjoy the most in class?", "options": {"A": ["STEM"], "B": ["Humanities"], "C": ["Creative"], "D": ["Business"]}},
    11: {"question": "How would you prefer to be tested?", "options": {"A": ["STEM"], "B": ["Humanities"], "C": ["Creative"], "D": ["Business"]}},
    12: {"question": "What kind of homework do you usually do first?", "options": {"A": ["STEM"], "B": ["Humanities"], "C": ["Creative"], "D": ["Business"]}},
    13: {"question": "In your free time, you enjoy:", "options": {"A": ["STEM"], "B": ["Creative"], "C": ["Humanities"], "D": ["Business"]}},
    14: {"question": "Which magazine would you pick up?", "options": {"A": ["STEM"], "B": ["Humanities"], "C": ["Creative"], "D": ["Business"]}},
    15: {"question": "You love school events where you can:", "options": {"A": ["STEM"], "B": ["Humanities"], "C": ["Creative"], "D": ["Business"]}},
    16: {"question": "What’s your idea of a fun weekend project?", "options": {"A": ["STEM"], "B": ["Creative"], "C": ["Humanities"], "D": ["Business"]}},
    17: {"question": "You admire people who:", "options": {"A": ["STEM"], "B": ["Humanities"], "C": ["Creative"], "D": ["Business"]}},
    18: {"question": "What excites you the most?", "options": {"A": ["STEM"], "B": ["Humanities"], "C": ["Creative"], "D": ["Business"]}},
    19: {"question": "You prefer working:", "options": {"A": ["Specialist"], "B": ["Generalist"], "C": ["Admin"], "D": ["Leadership"]}},
    20: {"question": "When meeting new people, you:", "options": {"A": ["Technical"], "B": ["Generalist"], "C": ["Leadership"], "D": ["Creative"]}},
    21: {"question": "Your teachers describe you as:", "options": {"A": ["Specialist"], "B": ["Leadership"], "C": ["Creative"], "D": ["Admin"]}},
    22: {"question": "What’s your preferred communication style?", "options": {"A": ["Admin"], "B": ["Creative"], "C": ["Leadership"], "D": ["Technical"]}},
    23: {"question": "You enjoy roles where you can:", "options": {"A": ["Leadership"], "B": ["Admin"], "C": ["Creative"], "D": ["Technical"]}},
    24: {"question": "In a class discussion, you usually:", "options": {"A": ["Specialist"], "B": ["Leadership"], "C": ["Creative"], "D": ["Admin"]}},
    25: {"question": "What’s most important in your future job?", "options": {"A": ["STEM"], "B": ["Humanities"], "C": ["Creative"], "D": ["Business"]}},
    26: {"question": "If given ₹10,000 today, you would:", "options": {"A": ["STEM"], "B": ["Humanities"], "C": ["Creative"], "D": ["Business"]}},
    27: {"question": "Which quote do you relate to most?", "options": {"A": ["Creative"], "B": ["Humanities"], "C": ["STEM"], "D": ["Business"]}},
    28: {"question": "Your dream project would involve:", "options": {"A": ["STEM"], "B": ["Humanities"], "C": ["Creative"], "D": ["Business"]}},
    29: {"question": "How do you make big decisions?", "options": {"A": ["STEM"], "B": ["Humanities"], "C": ["Creative"], "D": ["Business"]}},
    30: {"question": "Ten years from now, you want to be:", "options": {"A": ["STEM"], "B": ["Humanities"], "C": ["Creative"], "D": ["Business"]}},
}

responses = {}
st.header("Section 1: Psychometric Questions")
for q_no, q_data in questions.items():
    responses[q_no] = st.radio(q_data["question"], list(q_data["options"].keys()), key=f"q{q_no}")

st.header("Section 2: Academic Scores (Last 2 Years)")
academic_scores = st.data_editor(pd.DataFrame({
    "Subject": ["Math", "Science", "English", "Social Studies", "Second Language", "Computer", "Business Studies"],
    "Class 9 (%)": [None]*7,
    "Class 10 (%)": [None]*7,
}))

if st.button("Generate Report"):
    if student_name and all(responses.values()):
        scores = calculate_scores(responses, questions)
        pdf_path = generate_pdf_report(scores, academic_scores, student_name)
        with open(pdf_path, "rb") as f:
            st.download_button("Download Your Career Report", f, file_name=os.path.basename(pdf_path), mime="application/pdf")
    else:
        st.warning("Please fill out your name and answer all questions.")
