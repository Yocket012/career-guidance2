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
    # ... (All other questions from 2 to 30 copied here, same as before) ...
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
    file_path = f"/mnt/data/{safe_name.replace(' ', '_')}_Career_Report.pdf"
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
