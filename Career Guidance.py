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

def plot_radar_chart(scores):
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

    buf = BytesIO()
    plt.savefig(buf, format="png")
    plt.close(fig)
    buf.seek(0)
    return buf

# PDF Report Generator

def generate_pdf_report(scores, student_name):
    pdf = FPDF()
    pdf.add_page()
    pdf.set_font("Arial", 'B', 16)
    pdf.cell(0, 10, f"Career Guidance Report for {student_name}", ln=True)

    pdf.set_font("Arial", '', 12)
    pdf.ln(5)
    pdf.cell(0, 10, "Psychometric Summary:", ln=True)
    for trait, score in scores.items():
        pdf.cell(0, 8, f"- {trait}: {score}", ln=True)

    # Save radar chart to temp path for PDF
    radar_img = plot_radar_chart(scores)
    img_temp_path = "/tmp/radar_chart.png"
    with open(img_temp_path, "wb") as f:
        f.write(radar_img.read())
    pdf.image(img_temp_path, x=50, y=None, w=100)

    
    # Save final PDF
    safe_name = "".join(c for c in student_name if c.isalnum() or c in (" ", "_")).strip()
    file_path = f"/tmp/{safe_name.replace(' ', '_')}_Career_Report.pdf"
    pdf.output(file_path)
    return file_path, radar_img


# Streamlit UI
st.set_page_config(page_title="Career Guidance Test", layout="centered")
st.title("🧭 Class 9–10 Career Guidance Tool")
st.write("Answer the questions below to receive your personalised career report.")

student_name = st.text_input("Enter your name:")
responses = {}

with st.form("career_form"):
    for qid, q_data in questions.items():
        response = st.radio(q_data["question"], list(q_data["options"].keys()), key=qid)
        responses[qid] = response
    submitted = st.form_submit_button("Generate Report")

if submitted:
    if student_name and all(responses.values()):
        scores = calculate_scores(responses)
        report_path, radar_image = generate_pdf_report(scores, student_name)
        with open(report_path, "rb") as f:
            st.download_button("📥 Download Your Career Report", f, file_name=os.path.basename(report_path))
        st.success("Report generated successfully!")
        st.image(radar_image, caption="Your Career Profile")
    else:
        st.error("Please enter your name and complete all questions.")
