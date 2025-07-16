import streamlit as st
import pandas as pd
from fpdf import FPDF
import os
import numpy as np


def calculate_scores(responses, questions):
    score_categories = {
        "STEM": 0, "Humanities": 0, "Business": 0, "Creative": 0,
        "Specialist": 0, "Leadership": 0, "Creative_Role": 0, "Admin": 0,
        "Technical": 0, "Generalist": 0
    }
    for q_num, ans in responses.items():
        for text, tags in questions[q_num]["options"].items():
            if ans == text:
                for tag in tags:
                    score_categories[tag] += 1
    return score_categories

def generate_pdf_report(scores, academic_scores, student_name):
    pdf = FPDF()
    pdf.add_page()
    pdf.set_auto_page_break(auto=True, margin=15)
    pdf.set_font("Arial", 'B', 16)
    pdf.set_text_color(0, 102, 204)
    pdf.cell(0, 10, "Career Guidance Report", ln=True, align='C')

    pdf.set_font("Arial", 'I', 12)
    pdf.set_text_color(100, 100, 100)
    pdf.cell(0, 10, f"Student Name: {student_name}", ln=True)

    pdf.set_text_color(0, 0, 0)
    pdf.set_font("Arial", 'B', 13)
    pdf.ln(5)
    pdf.cell(0, 10, "Your Career Personality & Interests", ln=True)
    pdf.set_font("Arial", size=11)
    pdf.multi_cell(0, 8, "Based on your answers, we've identified the dominant areas of interest and working styles that best define you. This gives a glimpse into the kind of environments and careers you may thrive in.")

    top_domains = sorted(scores.items(), key=lambda x: x[1], reverse=True)[:3]
    pdf.ln(2)
    for domain, score in top_domains:
        pdf.cell(0, 8, f"- {domain} (score: {score})", ln=True)

    pdf.ln(5)
    pdf.set_font("Arial", 'B', 13)
    pdf.cell(0, 10, "Your Academic Strengths", ln=True)
    pdf.set_font("Arial", size=11)
    pdf.multi_cell(0, 8, "Here's a summary of your self-reported scores from Class 9 and 10. These help us understand which subjects you're most confident in.")
    pdf.ln(1)
    for index, row in academic_scores.iterrows():
        pdf.cell(0, 8, f"{row['Subject']}: Class 9 - {row['Class 9 (%)']}%, Class 10 - {row['Class 10 (%)']}%", ln=True)

    major_minor = {
        ("STEM", "Business"): ("Computer Science", "Business Analytics"),
        ("Humanities", "Creative"): ("Psychology", "Media Studies"),
        ("Creative", "Business"): ("Design", "Marketing"),
    }

    academic_boost = {"STEM": 0, "Humanities": 0, "Creative": 0, "Business": 0}
    for index, row in academic_scores.iterrows():
        subject = row['Subject'].lower()
        score9 = pd.to_numeric(row['Class 9 (%)'], errors='coerce')
        score10 = pd.to_numeric(row['Class 10 (%)'], errors='coerce')
        avg_score = np.nanmean([score9, score10])
        if "math" in subject or "science" in subject or "computer" in subject:
            academic_boost["STEM"] += avg_score
        elif "social" in subject:
            academic_boost["Humanities"] += avg_score
        elif "english" in subject or "language" in subject:
            academic_boost["Creative"] += avg_score
        elif "business" in subject:
            academic_boost["Business"] += avg_score

    combined_scores = {k: scores.get(k, 0)*2 + academic_boost.get(k, 0)/20 for k in ["STEM", "Humanities", "Creative", "Business"]}
    top_tags = tuple(sorted(combined_scores, key=combined_scores.get, reverse=True)[:2])
    major, minor = major_minor.get(top_tags, ("General Studies", "Communication"))

    pdf.ln(5)
    pdf.set_font("Arial", 'B', 13)
    pdf.cell(0, 10, "Recommended Major & Minor", ln=True)
    pdf.set_font("Arial", size=11)
    pdf.multi_cell(0, 8, f"""Based on your strengths and interests — drawn from both your responses and academic subject scores — we recommend this personalised academic path:

Major: {major}
Minor: {minor}

Why this recommendation?
Your psychometric responses show a strong alignment with {top_tags[0]} and {top_tags[1]} fields. Additionally, your academic performance in subjects such as:

- STEM Boost: {academic_boost['STEM']:.1f}
- Humanities Boost: {academic_boost['Humanities']:.1f}
- Creative Boost: {academic_boost['Creative']:.1f}
- Business Boost: {academic_boost['Business']:.1f}

...indicates that you are well-prepared to explore this combination at a deeper academic level.""")

    pdf.ln(5)
    pdf.set_font("Arial", 'B', 13)
    pdf.cell(0, 10, "Top Global Universities to Explore", ln=True)
    universities = {
        "Computer Science": ["University of Toronto", "University of Michigan", "NUS"],
        "Psychology": ["UCL", "University of Amsterdam", "University of British Columbia"],
        "Design": ["Parsons School of Design", "RMIT", "University of the Arts London"],
        "General Studies": ["Arizona State University", "Monash University", "York University"]
    }
    pdf.set_font("Arial", size=10)
    for uni in universities.get(major, []):
        pdf.cell(0, 8, f"- {uni}", ln=True)

    pdf.ln(5)
    pdf.set_font("Arial", 'B', 13)
    pdf.cell(0, 10, "Potential Career Paths & Entry Roles", ln=True)
    pdf.set_font("Arial", size=10)
    if major == "Computer Science":
        careers = ["Product Analyst at Google", "Data Analyst at Amazon", "Software Intern at Atlassian"]
    elif major == "Psychology":
        careers = ["Research Assistant at WHO", "Policy Analyst at UNDP", "Behavioural Analyst at Deloitte"]
    elif major == "Design":
        careers = ["UX Designer at Canva", "Visual Designer at Ogilvy", "Intern at IDEO"]
    else:
        careers = ["Content Creator", "Program Manager", "Marketing Intern"]

    for job in careers:
        pdf.cell(0, 8, f"- {job}", ln=True)

    pdf.ln(5)
    pdf.set_font("Arial", 'B', 13)
    pdf.cell(0, 10, "Final Thoughts", ln=True)
    pdf.set_font("Arial", 'I', 11)
    pdf.set_text_color(80, 80, 80)
    pdf.multi_cell(0, 8, "You're on the path to a promising global career. Remember, career discovery is a journey. Use this insight to explore, experiment, and grow into your full potential. Stay curious, stay inspired.")

    file_path = f"/mnt/data/{student_name.replace(' ', '_')}_Career_Report.pdf"
    pdf.output(file_path)
    return file_path

st.title("Class 9–10 Career Guidance Psychometric Test")
student_name = st.text_input("Enter your name")

questions = {
    1: {"question": "How do you prefer to start your school projects?", "options": {
        "Planning and outlining everything (Admin)": ["Admin"],
        "Getting straight into it creatively (Creative)": ["Creative"],
        "Researching and gathering data (Specialist)": ["Specialist"],
        "Talking with friends to brainstorm (Generalist)": ["Generalist"]}},
    2: {"question": "When working in a group, what role do you usually take?", "options": {
        "Leader (Leadership)": ["Leadership"],
        "Researcher/Analyst (Specialist)": ["Specialist"],
        "Designer/Idea person (Creative)": ["Creative"],
        "Coordinator or Communicator (Administrative)": ["Admin"]}},
    3: {"question": "What motivates you to complete a task?", "options": {
        "Recognition (Leadership)": ["Leadership"],
        "Learning something new (Specialist)": ["Specialist"],
        "Solving a problem (Technical)": ["Technical"],
        "Finishing on time (Administrative)": ["Admin"]}},
    4: {"question": "You're given a topic to present. You would:", "options": {
        "Make slides with visuals and stories (Creative)": ["Creative"],
        "Deep dive into facts and stats (Specialist)": ["Specialist"],
        "Keep it structured and timed (Admin)": ["Admin"],
        "Add jokes and involve the audience (Generalist)": ["Generalist"]}},
    5: {"question": "What frustrates you the most in a school setting?", "options": {
        "Lack of structure (Admin)": ["Admin"],
        "No room for creativity (Creative)": ["Creative"],
        "Vague instructions (Specialist)": ["Specialist"],
        "No chance to collaborate (Generalist)": ["Generalist"]}},
    6: {"question": "You enjoy subjects that are:", "options": {
        "Practical and hands-on (Technical)": ["Technical"],
        "Imaginative and open-ended (Creative)": ["Creative"],
        "Rule-based and structured (Administrative)": ["Admin"],
        "Analytical and logic-based (Specialist)": ["Specialist"]}},
    7: {"question": "Which subject do you enjoy the most?", "options": {
        "Math/Science (STEM)": ["STEM"],
        "Social Studies (Humanities)": ["Humanities"],
        "English/Languages (Creative)": ["Creative"],
        "Business/Accounts (Business)": ["Business"]}},
    8: {"question": "How do you usually score in Math?", "options": {
        "Above 90% (STEM)": ["STEM"],
        "75–89% (STEM)": ["STEM"],
        "60–74% (STEM)": ["STEM"],
        "Below 60% (STEM)": ["STEM"]}},
    9: {"question": "Which best describes your learning style?", "options": {
        "Logical problem-solver (STEM)": ["STEM"],
        "Storyteller & writer (Creative)": ["Creative"],
        "Curious & likes asking 'why' (Humanities)": ["Humanities"],
        "Likes data, numbers & trends (Business)": ["Business"]}},
    10: {"question": "Which activity do you enjoy the most in class?", "options": {
        "Solving puzzles or experiments (STEM)": ["STEM"],
        "Debating or expressing opinions (Humanities)": ["Humanities"],
        "Writing stories or making art (Creative)": ["Creative"],
        "Working with money or planning (Business)": ["Business"]}},
    11: {"question": "How would you prefer to be tested?", "options": {
        "MCQs and problems to solve (STEM)": ["STEM"],
        "Essays and long answers (Humanities)": ["Humanities"],
        "Projects or creative presentations (Creative)": ["Creative"],
        "Real-life business case studies (Business)": ["Business"]}},
    12: {"question": "What kind of homework do you usually do first?", "options": {
        "The one with formulas/calculations (STEM)": ["STEM"],
        "Essays or reports (Humanities)": ["Humanities"],
        "Presentations or art projects (Creative)": ["Creative"],
        "Case studies or graphs (Business)": ["Business"]}},
    13: {"question": "In your free time, you enjoy:", "options": {
        "Coding/tech experiments (STEM)": ["STEM"],
        "Making art/videos (Creative)": ["Creative"],
        "Reading about people & society (Humanities)": ["Humanities"],
        "Watching Shark Tank or finance news (Business)": ["Business"]}},
    14: {"question": "Which magazine would you pick up?", "options": {
        "Popular Science (STEM)": ["STEM"],
        "National Geographic or TIME (Humanities)": ["Humanities"],
        "Vogue or Filmfare (Creative)": ["Creative"],
        "Forbes or Entrepreneur (Business)": ["Business"]}},
    15: {"question": "You love school events where you can:", "options": {
        "Compete in quizzes/tech fests (STEM)": ["STEM"],
        "Participate in debates/social talks (Humanities)": ["Humanities"],
        "Perform or showcase designs (Creative)": ["Creative"],
        "Organise stalls or manage funds (Business)": ["Business"]}},
    16: {"question": "What's your idea of a fun weekend project?", "options": {
        "Build something or solve a logic puzzle (STEM)": ["STEM"],
        "Make a film, write, or design (Creative)": ["Creative"],
        "Research or read on a social issue (Humanities)": ["Humanities"],
        "Create a budget or start a mini business (Business)": ["Business"]}},
    17: {"question": "You admire people who:", "options": {
        "Invent or discover things (STEM)": ["STEM"],
        "Change society through ideas (Humanities)": ["Humanities"],
        "Create beauty and impact through art (Creative)": ["Creative"],
        "Build companies or manage money (Business)": ["Business"]}},
    18: {"question": "What excites you the most?", "options": {
        "New gadgets and AI (STEM)": ["STEM"],
        "Campaigning or public speaking (Humanities)": ["Humanities"],
        "Expressing stories or visuals (Creative)": ["Creative"],
        "Stocks, brands, and entrepreneurship (Business)": ["Business"]}},
    19: {"question": "You prefer working:", "options": {
        "Alone with full control (Specialist)": ["Specialist"],
        "With a team, bouncing ideas (Generalist)": ["Generalist"],
        "With clear structure and roles (Admin)": ["Admin"],
        "Leading and taking initiative (Leadership)": ["Leadership"]}},
    20: {"question": "When meeting new people, you:", "options": {
        "Feel reserved but observant (Technical)": ["Technical"],
        "Get curious and ask questions (Generalist)": ["Generalist"],
        "Talk confidently and share your views (Leadership)": ["Leadership"],
        "Prefer visual or creative conversations (Creative)": ["Creative"]}},
    21: {"question": "Your teachers describe you as:", "options": {
        "Quiet but intelligent (Specialist)": ["Specialist"],
        "Confident and participative (Leadership)": ["Leadership"],
        "Fun and imaginative (Creative)": ["Creative"],
        "Friendly and organised (Admin)": ["Admin"]}},
    22: {"question": "What's your preferred communication style?", "options": {
        "Clear, detailed, and written (Admin)": ["Admin"],
        "Visual and expressive (Creative)": ["Creative"],
        "Debating and convincing (Leadership)": ["Leadership"],
        "Practical and result-oriented (Technical)": ["Technical"]}},
    23: {"question": "You enjoy roles where you can:", "options": {
        "Guide others (Leadership)": ["Leadership"],
        "Collaborate and support (Admin)": ["Admin"],
        "Present or create content (Creative)": ["Creative"],
        "Find solutions to problems (Technical)": ["Technical"]}},
    24: {"question": "In a class discussion, you usually:", "options": {
        "Observe and speak when needed (Specialist)": ["Specialist"],
        "Lead and moderate the talk (Leadership)": ["Leadership"],
        "Share out-of-the-box ideas (Creative)": ["Creative"],
        "Add structure and summary (Admin)": ["Admin"]}},
    25: {"question": "What's most important in your future job?", "options": {
        "Innovation & challenge (STEM)": ["STEM"],
        "Purpose & impact (Humanities)": ["Humanities"],
        "Expression & freedom (Creative)": ["Creative"],
        "Stability & income (Business)": ["Business"]}},
    26: {"question": "If given ₹10,000 today, you would:", "options": {
        "Buy tech/tools to build something (STEM)": ["STEM"],
        "Donate or fund a cause (Humanities)": ["Humanities"],
        "Buy art gear or upgrade a camera (Creative)": ["Creative"],
        "Invest or save (Business)": ["Business"]}},
    27: {"question": "Which quote do you relate to most?", "options": {
        "Think different. (Creative)": ["Creative"],
        "Be the change. (Humanities)": ["Humanities"],
        "Logic will get you from A to B. (STEM)": ["STEM"],
        "Make your money work for you. (Business)": ["Business"]}},
    28: {"question": "Your dream project would involve:", "options": {
        "Creating something new (STEM)": ["STEM"],
        "Influencing society or people (Humanities)": ["Humanities"],
        "Designing stories or visuals (Creative)": ["Creative"],
        "Launching a business idea (Business)": ["Business"]}},
    29: {"question": "How do you make big decisions?", "options": {
        "Based on facts and logic (STEM)": ["STEM"],
        "Through discussions and input (Humanities)": ["Humanities"],
        "On intuition and creativity (Creative)": ["Creative"],
        "By weighing cost and benefits (Business)": ["Business"]}},
    30: {"question": "Ten years from now, you want to be:", "options": {
        "An inventor or engineer (STEM)": ["STEM"],
        "A social changemaker (Humanities)": ["Humanities"],
        "A filmmaker/artist (Creative)": ["Creative"],
        "A CEO or investor (Business)": ["Business"]}},
}

responses = {}
st.header("Section 1: Psychometric Questions")
for q_no, q_data in questions.items():
    option_labels = list(q_data["options"].keys())
    responses[q_no] = st.radio(q_data["question"], option_labels, key=f"q{q_no}")

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

