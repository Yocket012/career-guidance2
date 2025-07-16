import streamlit as st
import pandas as pd
from fpdf import FPDF
import os
import numpy as np
import matplotlib.pyplot as plt
from io import BytesIO

# Define 30 psychometric questions
questions = {
    1: {"question": "How do you prefer to start your school projects?", "options": {
        "Planning and outlining everything": ["Admin"],
        "Getting straight into it creatively": ["Creative_Role"],
        "Researching and gathering data": ["Specialist"],
        "Talking with friends to brainstorm": ["Generalist"]}},
    2: {"question": "When working in a group, what role do you usually take?", "options": {
        "Leader": ["Leadership"],
        "Researcher/Analyst": ["Specialist"],
        "Designer/Idea person": ["Creative_Role"],
        "Coordinator or Communicator": ["Admin"]}},
    3: {"question": "What motivates you to complete a task?", "options": {
        "Recognition": ["Leadership"],
        "Learning something new": ["Specialist"],
        "Solving a problem": ["Technical"],
        "Finishing on time": ["Admin"]}},
    4: {"question": "You’re given a topic to present. You would:", "options": {
        "Make slides with visuals and stories": ["Creative_Role"],
        "Deep dive into facts and stats": ["Specialist"],
        "Keep it structured and timed": ["Admin"],
        "Add jokes and involve the audience": ["Generalist"]}},
    5: {"question": "What frustrates you the most in a school setting?", "options": {
        "Lack of structure": ["Admin"],
        "No room for creativity": ["Creative_Role"],
        "Vague instructions": ["Specialist"],
        "No chance to collaborate": ["Generalist"]}},
    6: {"question": "You enjoy subjects that are:", "options": {
        "Practical and hands-on": ["Technical"],
        "Imaginative and open-ended": ["Creative_Role"],
        "Rule-based and structured": ["Admin"],
        "Analytical and logic-based": ["Specialist"]}},
    7: {"question": "Which subject do you enjoy the most?", "options": {
        "Math/Science": ["STEM"],
        "Social Studies": ["Humanities"],
        "English/Languages": ["Creative"],
        "Business/Accounts": ["Business"]}},
    8: {"question": "How do you usually score in Math?", "options": {
        "Above 90%": ["STEM"],
        "75–89%": ["STEM"],
        "60–74%": ["STEM"],
        "Below 60%": []}},
    9: {"question": "Which best describes your learning style?", "options": {
        "Logical problem-solver": ["STEM"],
        "Storyteller & writer": ["Creative"],
        "Curious & likes asking 'why'": ["Humanities"],
        "Likes data, numbers & trends": ["Business"]}},
    10: {"question": "Which activity do you enjoy the most in class?", "options": {
        "Solving puzzles or experiments": ["STEM"],
        "Debating or expressing opinions": ["Humanities"],
        "Writing stories or making art": ["Creative"],
        "Working with money or planning": ["Business"]}},
    11: {"question": "How would you prefer to be tested?", "options": {
        "MCQs and problems to solve": ["STEM"],
        "Essays and long answers": ["Humanities"],
        "Projects or creative presentations": ["Creative"],
        "Real-life business case studies": ["Business"]}},
    12: {"question": "What kind of homework do you usually do first?", "options": {
        "The one with formulas/calculations": ["STEM"],
        "Essays or reports": ["Humanities"],
        "Presentations or art projects": ["Creative"],
        "Case studies or graphs": ["Business"]}},
    13: {"question": "In your free time, you enjoy:", "options": {
        "Coding/tech experiments": ["STEM"],
        "Making art/videos": ["Creative"],
        "Reading about people & society": ["Humanities"],
        "Watching Shark Tank or finance news": ["Business"]}},
    14: {"question": "Which magazine would you pick up?", "options": {
        "Popular Science": ["STEM"],
        "National Geographic or TIME": ["Humanities"],
        "Vogue or Filmfare": ["Creative"],
        "Forbes or Entrepreneur": ["Business"]}},
    15: {"question": "You love school events where you can:", "options": {
        "Compete in quizzes/tech fests": ["STEM"],
        "Participate in debates/social talks": ["Humanities"],
        "Perform or showcase designs": ["Creative"],
        "Organise stalls or manage funds": ["Business"]}},
    16: {"question": "What’s your idea of a fun weekend project?", "options": {
        "Build something or solve a logic puzzle": ["STEM"],
        "Make a film, write, or design": ["Creative"],
        "Research or read on a social issue": ["Humanities"],
        "Create a budget or start a mini business": ["Business"]}},
    17: {"question": "You admire people who:", "options": {
        "Invent or discover things": ["STEM"],
        "Change society through ideas": ["Humanities"],
        "Create beauty and impact through art": ["Creative"],
        "Build companies or manage money": ["Business"]}},
    18: {"question": "What excites you the most?", "options": {
        "New gadgets and AI": ["STEM"],
        "Campaigning or public speaking": ["Humanities"],
        "Expressing stories or visuals": ["Creative"],
        "Stocks, brands, and entrepreneurship": ["Business"]}},
    19: {"question": "You prefer working:", "options": {
        "Alone with full control": ["Specialist"],
        "With a team, bouncing ideas": ["Generalist"],
        "With clear structure and roles": ["Admin"],
        "Leading and taking initiative": ["Leadership"]}},
    20: {"question": "When meeting new people, you:", "options": {
        "Feel reserved but observant": ["Technical"],
        "Get curious and ask questions": ["Generalist"],
        "Talk confidently and share your views": ["Leadership"],
        "Prefer visual or creative conversations": ["Creative_Role"]}},
    21: {"question": "Your teachers describe you as:", "options": {
        "Quiet but intelligent": ["Specialist"],
        "Confident and participative": ["Leadership"],
        "Fun and imaginative": ["Creative_Role"],
        "Friendly and organised": ["Admin"]}},
    22: {"question": "What’s your preferred communication style?", "options": {
        "Clear, detailed, and written": ["Admin"],
        "Visual and expressive": ["Creative_Role"],
        "Debating and convincing": ["Leadership"],
        "Practical and result-oriented": ["Technical"]}},
    23: {"question": "You enjoy roles where you can:", "options": {
        "Guide others": ["Leadership"],
        "Collaborate and support": ["Admin"],
        "Present or create content": ["Creative_Role"],
        "Find solutions to problems": ["Technical"]}},
    24: {"question": "In a class discussion, you usually:", "options": {
        "Observe and speak when needed": ["Specialist"],
        "Lead and moderate the talk": ["Leadership"],
        "Share out-of-the-box ideas": ["Creative_Role"],
        "Add structure and summary": ["Admin"]}},
    25: {"question": "What’s most important in your future job?", "options": {
        "Innovation & challenge": ["STEM"],
        "Purpose & impact": ["Humanities"],
        "Expression & freedom": ["Creative"],
        "Stability & income": ["Business"]}},
    26: {"question": "If given INR 10,000 today, you would:", "options": {
        "Buy tech/tools to build something": ["STEM"],
        "Donate or fund a cause": ["Humanities"],
        "Buy art gear or upgrade a camera": ["Creative"],
        "Invest or save": ["Business"]}},
    27: {"question": "Which quote do you relate to most?", "options": {
        "Think different.": ["Creative"],
        "Be the change.": ["Humanities"],
        "Logic will get you from A to B.": ["STEM"],
        "Make your money work for you.": ["Business"]}},
    28: {"question": "Your dream project would involve:", "options": {
        "Creating something new": ["STEM"],
        "Influencing society or people": ["Humanities"],
        "Designing stories or visuals": ["Creative"],
        "Launching a business idea": ["Business"]}},
    29: {"question": "How do you make big decisions?", "options": {
        "Based on facts and logic": ["STEM"],
        "Through discussions and input": ["Humanities"],
        "On intuition and creativity": ["Creative"],
        "By weighing cost and benefits": ["Business"]}},
    30: {"question": "Ten years from now, you want to be:", "options": {
        "An inventor or engineer": ["STEM"],
        "A social changemaker": ["Humanities"],
        "A filmmaker/artist": ["Creative"],
        "A CEO or investor": ["Business"]}}
}

# Calculate Scores

def calculate_scores(responses):
    scores = {}
    for qid, answer in responses.items():
        tags = questions[qid]["options"].get(answer, [])
        for tag in tags:
            scores[tag] = scores.get(tag, 0) + 1
    return scores

# Radar Chart Generator

def plot_radar_chart(scores, title="Radar Chart"):
    categories = list(scores.keys())
    values = list(scores.values())
    N = len(categories)
    values += values[:1]
    angles = [n / float(N) * 2 * np.pi for n in range(N)]
    angles += angles[:1]

    fig, ax = plt.subplots(figsize=(6, 6), subplot_kw=dict(polar=True))
    ax.plot(angles, values, linewidth=2)
    ax.fill(angles, values, alpha=0.25)
    ax.set_xticks(angles[:-1])
    ax.set_xticklabels(categories)
    ax.set_yticklabels([])
    plt.title(title)

    buf = BytesIO()
    plt.savefig(buf, format="png")
    plt.close(fig)
    buf.seek(0)
    return buf

# Major and Minor Recommendation

def suggest_major_minor(scores, academic_df):
    domain_boost = {"STEM": 0, "Humanities": 0, "Creative": 0, "Business": 0}
    if academic_df is not None:
        for _, row in academic_df.iterrows():
            try:
                score9 = pd.to_numeric(row['Class 9 (%)'], errors='coerce')
                score10 = pd.to_numeric(row['Class 10 (%)'], errors='coerce')
                avg = np.nanmean([score9, score10])
                subject = row['Subject'].lower()
                if "math" in subject or "science" in subject or "computer" in subject:
                    domain_boost["STEM"] += avg
                elif "social" in subject:
                    domain_boost["Humanities"] += avg
                elif "english" in subject:
                    domain_boost["Creative"] += avg
                elif "business" in subject or "accounts" in subject:
                    domain_boost["Business"] += avg
            except:
                continue

    final_scores = {k: scores.get(k, 0) + domain_boost.get(k, 0)/20 for k in domain_boost}
    sorted_domains = sorted(final_scores.items(), key=lambda x: x[1], reverse=True)
    major = sorted_domains[0][0]
    minor = sorted_domains[1][0]
    return major, minor, domain_boost

# Career Info
career_data = {
    "STEM": {
        "careers": ["Software Engineer", "Data Analyst", "AI Researcher"],
        "universities": ["MIT", "Stanford", "ETH Zurich", "TUM", "University of Cambridge"],
        "entry_roles": ["Junior Developer", "Data Analyst", "Tech Consultant"]
    },
    "Humanities": {
        "careers": ["Policy Analyst", "Journalist", "NGO Manager"],
        "universities": ["Harvard", "LSE", "Sciences Po", "University of Oxford", "Ashoka University"],
        "entry_roles": ["Research Assistant", "Content Writer", "Project Coordinator"]
    },
    "Creative": {
        "careers": ["Graphic Designer", "Film Maker", "UI/UX Designer"],
        "universities": ["Parsons School of Design", "NID", "UCLA", "RISD", "London College of Fashion"],
        "entry_roles": ["Visual Designer", "Creative Intern", "Junior Animator"]
    },
    "Business": {
        "careers": ["Investment Analyst", "Product Manager", "Entrepreneur"],
        "universities": ["Wharton", "INSEAD", "London Business School", "IIM", "NYU Stern"],
        "entry_roles": ["Business Analyst", "Sales Associate", "Junior Consultant"]
    }
}

# PDF Report Generator

def generate_pdf_report(scores, academic_df, student_name):
    major, minor, academic_scores = suggest_major_minor(scores, academic_df)
    pdf = FPDF()
    pdf.add_page()
    pdf.set_font("Arial", 'B', 16)
    pdf.cell(0, 10, f"Career Guidance Report for {student_name}", ln=True)

    pdf.set_font("Arial", '', 12)
    pdf.ln(5)
    pdf.cell(0, 10, "Psychometric Summary:", ln=True)
    for trait, score in scores.items():
        pdf.cell(0, 8, f"- {trait}: {score}", ln=True)

    radar_img = plot_radar_chart(scores, "Psychometric Radar Chart")
    img_path_1 = "/tmp/radar_chart1.png"
    with open(img_path_1, "wb") as f:
        f.write(radar_img.read())
    pdf.image(img_path_1, x=50, y=None, w=100)

    radar_img2 = plot_radar_chart(academic_scores, "Academic Inclination Chart")
    img_path_2 = "/tmp/radar_chart2.png"
    with open(img_path_2, "wb") as f:
        f.write(radar_img2.read())
    pdf.image(img_path_2, x=50, y=None, w=100)

    pdf.ln(10)
    pdf.set_font("Arial", 'B', 12)
    pdf.cell(0, 10, f"Suggested Major: {major}", ln=True)
    pdf.cell(0, 10, f"Suggested Minor: {minor}", ln=True)

    pdf.set_font("Arial", '', 11)
    pdf.cell(0, 10, "Top Careers:", ln=True)
    for c in career_data[major]["careers"]:
        pdf.cell(0, 8, f"- {c}", ln=True)
    pdf.cell(0, 10, "Top Universities:", ln=True)
    for u in career_data[major]["universities"]:
        pdf.cell(0, 8, f"- {u}", ln=True)
    pdf.cell(0, 10, "Entry Roles:", ln=True)
    for r in career_data[major]["entry_roles"]:
        pdf.cell(0, 8, f"- {r}", ln=True)

    safe_name = "".join(c for c in student_name if c.isalnum() or c in (" ", "_")).strip()
    file_path = f"/tmp/{safe_name.replace(' ', '_')}_Career_Report.pdf"
    pdf.output(file_path)
    return file_path, img_path_1, img_path_2

# Streamlit UI
st.set_page_config(page_title="Career Guidance Test", layout="centered")
st.title("🧭 Class 9–10 Career Guidance Tool")

student_name = st.text_input("Enter your name:")
academic_df = st.data_editor(pd.DataFrame({
    "Subject": ["Math", "Science", "English", "Social Studies", "Computer"],
    "Class 9 (%)": ["", "", "", "", ""],
    "Class 10 (%)": ["", "", "", "", ""]
}), num_rows="dynamic", use_container_width=True)

responses = {}
with st.form("career_form"):
    for qid, q_data in questions.items():
        response = st.radio(q_data["question"], list(q_data["options"].keys()), key=qid)
        responses[qid] = response
    submitted = st.form_submit_button("Generate Report")

if submitted:
    if student_name and all(responses.values()):
        scores = calculate_scores(responses)
        report_path, radar_img_1, radar_img_2 = generate_pdf_report(scores, academic_df, student_name)
        with open(report_path, "rb") as f:
            st.download_button("📥 Download Career Report", f, file_name=os.path.basename(report_path))
        st.image(radar_img_1, caption="Psychometric Radar Chart")
        st.image(radar_img_2, caption="Academic Inclination Chart")
    else:
        st.error("Please fill all fields to proceed.")
