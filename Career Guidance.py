import streamlit as st
import pandas as pd
from fpdf import FPDF
import numpy as np
import matplotlib.pyplot as plt
from io import BytesIO
import tempfile
import os

st.set_page_config(page_title="Career Guidance Test", layout="centered")

# Define 60 psychometric questions (10 per dimension)
questions = {
# Personality Types
    1: {"question": "How do you behave in new social situations?", "options": {
        "I observe quietly": ["Introvert"],
        "I talk to a few people": ["Ambivert"],
        "I mingle with everyone": ["Extrovert"],
        "I wait for someone to talk to me": ["Reserved"]}},
    2: {"question": "What describes you best at school?", "options": {
        "Organised and timely": ["Structured"],
        "Casual but meet deadlines": ["Balanced"],
        "I work last minute": ["Spontaneous"],
        "I need help to manage work": ["Dependent"]}},
    3: {"question": "Your desk at home is usually:", "options": {
        "Neat and organised": ["Structured"],
        "A little messy but I know where things are": ["Balanced"],
        "Super messy": ["Spontaneous"],
        "Varies depending on mood": ["Dependent"]}},
    4: {"question": "How do you deal with unexpected tasks?", "options": {
        "Make a plan first": ["Structured"],
        "Jump into it": ["Spontaneous"],
        "Ask for help": ["Dependent"],
        "Balance between planning and action": ["Balanced"]}},
    5: {"question": "Your friends describe you as:", "options": {
        "Quiet and thoughtful": ["Introvert"],
        "Friendly and outgoing": ["Extrovert"],
        "Balanced": ["Ambivert"],
        "Only open with close friends": ["Reserved"]}},
    6: {"question": "When given choices, you:", "options": {
        "Weigh all pros and cons": ["Structured"],
        "Go with what feels right": ["Spontaneous"],
        "Get overwhelmed sometimes": ["Dependent"],
        "Mix logic with instinct": ["Balanced"]}},
    7: {"question": "How do you plan your day?", "options": {
        "Create a checklist": ["Structured"],
        "Have a rough idea only": ["Spontaneous"],
        "Don’t plan – go with the flow": ["Dependent"],
        "Some parts planned, some flexible": ["Balanced"]}},
    8: {"question": "You feel most productive when:", "options": {
        "You have a fixed routine": ["Structured"],
        "You’re doing something exciting": ["Spontaneous"],
        "You have someone guiding you": ["Dependent"],
        "You have space to adapt": ["Balanced"]}},
    9: {"question": "You prefer to work:", "options": {
        "Alone and focused": ["Introvert"],
        "In groups and discussions": ["Extrovert"],
        "Based on the task": ["Ambivert"],
        "Quietly with close peers": ["Reserved"]}},
    10: {"question": "When making choices, you rely on:", "options": {
        "Facts and logic": ["Structured"],
        "Gut feeling": ["Spontaneous"],
        "Guidance from others": ["Dependent"],
        "A mix of both": ["Balanced"]}},

    # Learning Style Types
    11: {"question": "How do you best learn something new?", "options": {
        "By watching or seeing": ["Visual Learner"],
        "By doing or experiencing": ["Kinesthetic Learner"],
        "By listening": ["Auditory Learner"],
        "By reading": ["Reading/Writing Learner"]}},
    12: {"question": "How do you remember a concept best?", "options": {
        "By making mind maps": ["Visual Learner"],
        "By teaching someone else": ["Kinesthetic Learner"],
        "By repeating it aloud": ["Auditory Learner"],
        "By taking notes": ["Reading/Writing Learner"]}},
    13: {"question": "You understand better when:", "options": {
        "You draw it out": ["Visual Learner"],
        "You try it yourself": ["Kinesthetic Learner"],
        "You hear it explained": ["Auditory Learner"],
        "You read examples": ["Reading/Writing Learner"]}},
    14: {"question": "You revise best by:", "options": {
        "Making diagrams": ["Visual Learner"],
        "Practicing tasks": ["Kinesthetic Learner"],
        "Listening to recordings": ["Auditory Learner"],
        "Writing summaries": ["Reading/Writing Learner"]}},
    15: {"question": "You enjoy teachers who:", "options": {
        "Use visuals": ["Visual Learner"],
        "Make you do activities": ["Kinesthetic Learner"],
        "Explain out loud": ["Auditory Learner"],
        "Give notes and readings": ["Reading/Writing Learner"]}},
    16: {"question": "To recall something, you usually:", "options": {
        "Picture it in your mind": ["Visual Learner"],
        "Act it out or simulate": ["Kinesthetic Learner"],
        "Say it aloud": ["Auditory Learner"],
        "Write it down repeatedly": ["Reading/Writing Learner"]}},
    17: {"question": "What type of homework feels easiest?", "options": {
        "Drawing or mapping concepts": ["Visual Learner"],
        "Building or hands-on work": ["Kinesthetic Learner"],
        "Oral presentation": ["Auditory Learner"],
        "Essays or reports": ["Reading/Writing Learner"]}},
    18: {"question": "You enjoy content in the form of:", "options": {
        "Videos and diagrams": ["Visual Learner"],
        "Interactive games": ["Kinesthetic Learner"],
        "Podcasts or lectures": ["Auditory Learner"],
        "Articles and books": ["Reading/Writing Learner"]}},
    19: {"question": "You prefer revision that involves:", "options": {
        "Charts or mind maps": ["Visual Learner"],
        "Model making or practice": ["Kinesthetic Learner"],
        "Audio summaries": ["Auditory Learner"],
        "Written notes": ["Reading/Writing Learner"]}},
    20: {"question": "Which best describes how you study?", "options": {
        "I use color-coded notes": ["Visual Learner"],
        "I do sample exercises": ["Kinesthetic Learner"],
        "I listen to myself/others": ["Auditory Learner"],
        "I reread material often": ["Reading/Writing Learner"]}},

        # Behaviour Types (Q21–30)
    21: {"question": "In group projects, you usually:", "options": {
        "Take charge and lead": ["Leader"],
        "Do what you are assigned": ["Executor"],
        "Give ideas and feedback": ["Thinker"],
        "Help where needed": ["Supporter"]}},
    22: {"question": "You prefer instructions that are:", "options": {
        "Clear and step-by-step": ["Executor"],
        "Flexible with creativity": ["Thinker"],
        "Simple and quick": ["Supporter"],
        "Complete with big picture": ["Leader"]}},
    23: {"question": "In school events, you mostly:", "options": {
        "Manage or coordinate": ["Leader"],
        "Host or perform": ["Thinker"],
        "Do behind-the-scenes work": ["Executor"],
        "Assist friends or groups": ["Supporter"]}},
    24: {"question": "Your decision-making style is:", "options": {
        "Quick and confident": ["Leader"],
        "Balanced and open": ["Thinker"],
        "Based on given rules": ["Executor"],
        "With input from others": ["Supporter"]}},
    25: {"question": "Your classmates rely on you for:", "options": {
        "Leadership": ["Leader"],
        "Creative ideas": ["Thinker"],
        "Execution and details": ["Executor"],
        "Team spirit": ["Supporter"]}},
    26: {"question": "During competitions, you are:", "options": {
        "Focused and goal-oriented": ["Executor"],
        "Cheerful and motivating": ["Supporter"],
        "Strategic and planning": ["Leader"],
        "Innovative and fun": ["Thinker"]}},
    27: {"question": "When there's a problem, you:", "options": {
        "Try new ways to solve": ["Thinker"],
        "Get help from a group": ["Supporter"],
        "Take control to fix it": ["Leader"],
        "Follow a known process": ["Executor"]}},
    28: {"question": "You feel most valued when:", "options": {
        "You lead a task": ["Leader"],
        "You give good suggestions": ["Thinker"],
        "You do something well": ["Executor"],
        "You help someone succeed": ["Supporter"]}},
    29: {"question": "At school you often:", "options": {
        "Organise peers": ["Leader"],
        "Give ideas in class": ["Thinker"],
        "Do assignments carefully": ["Executor"],
        "Assist friends often": ["Supporter"]}},
    30: {"question": "If your friend needs help in a project:", "options": {
        "You take charge for them": ["Leader"],
        "You brainstorm ideas": ["Thinker"],
        "You complete parts for them": ["Executor"],
        "You guide and cheer them": ["Supporter"]}},

        # Emotional Types (Q31–40)
    31: {"question": "When you feel anxious, you:", "options": {
        "Talk it out": ["Expressive"],
        "Keep it to yourself": ["Internaliser"],
        "Get irritated": ["Reactive"],
        "Distract yourself": ["Avoidant"]}},
    32: {"question": "When you get bad marks:", "options": {
        "You feel down for a while": ["Internaliser"],
        "You talk to someone": ["Expressive"],
        "You blame the paper/system": ["Reactive"],
        "You ignore and move on": ["Avoidant"]}},
    33: {"question": "How do you react to criticism?", "options": {
        "Think quietly and change": ["Internaliser"],
        "Defend immediately": ["Reactive"],
        "Laugh or joke about it": ["Avoidant"],
        "Talk about it later": ["Expressive"]}},
    34: {"question": "When you’re angry:", "options": {
        "You raise your voice": ["Reactive"],
        "You cry or become silent": ["Internaliser"],
        "You walk away": ["Avoidant"],
        "You tell someone why": ["Expressive"]}},
    35: {"question": "When something great happens:", "options": {
        "You share it with everyone": ["Expressive"],
        "You smile to yourself": ["Internaliser"],
        "You act like it's no big deal": ["Avoidant"],
        "You celebrate loudly": ["Reactive"]}},
    36: {"question": "How do you handle pressure?", "options": {
        "Vent or share emotions": ["Expressive"],
        "Overthink silently": ["Internaliser"],
        "Get angry or short-tempered": ["Reactive"],
        "Escape into games/music": ["Avoidant"]}},
    37: {"question": "When people are upset with you:", "options": {
        "You cry or worry": ["Internaliser"],
        "You fight back": ["Reactive"],
        "You laugh it off": ["Avoidant"],
        "You try to talk it through": ["Expressive"]}},
    38: {"question": "What do you do when you're sad?", "options": {
        "Write or talk": ["Expressive"],
        "Stay quiet and hide it": ["Internaliser"],
        "Complain or shout": ["Reactive"],
        "Watch movies/play games": ["Avoidant"]}},
    39: {"question": "When nervous before exams:", "options": {
        "You talk to a parent or friend": ["Expressive"],
        "You worry silently": ["Internaliser"],
        "You get annoyed or restless": ["Reactive"],
        "You distract yourself": ["Avoidant"]}},
    40: {"question": "How do you deal with failure?", "options": {
        "Open up to someone": ["Expressive"],
        "Keep emotions to yourself": ["Internaliser"],
        "Blame others or get angry": ["Reactive"],
        "Avoid thinking about it": ["Avoidant"]}},

        # Interest Types (Q41–50)
    41: {"question": "In your free time, you prefer:", "options": {
        "Building something or solving problems": ["STEM"],
        "Writing, drawing, or performing": ["Creative"],
        "Learning about people or society": ["Humanities"],
        "Trading or money-related tasks": ["Business"]}},
    42: {"question": "You are most excited by:", "options": {
        "New technology and inventions": ["STEM"],
        "Beautiful designs and stories": ["Creative"],
        "Ideas that change society": ["Humanities"],
        "Business plans and brands": ["Business"]}},
    43: {"question": "Your ideal class activity would be:", "options": {
        "Science experiment or coding challenge": ["STEM"],
        "Drama or visual art": ["Creative"],
        "Debate or survey": ["Humanities"],
        "Case study or role play business": ["Business"]}},
    44: {"question": "When choosing a documentary, you’d pick:", "options": {
        "About space, physics or AI": ["STEM"],
        "About filmmakers, artists or musicians": ["Creative"],
        "About history or society": ["Humanities"],
        "About companies or finance": ["Business"]}},
    45: {"question": "You enjoy magazines or videos about:", "options": {
        "Science and discovery": ["STEM"],
        "Movies and storytelling": ["Creative"],
        "World events and change-makers": ["Humanities"],
        "Startups and money": ["Business"]}},
    46: {"question": "Your favourite school event is:", "options": {
        "Tech fair or quiz": ["STEM"],
        "Art or music fest": ["Creative"],
        "MUN or elocution": ["Humanities"],
        "Business bazaar": ["Business"]}},
    47: {"question": "What kind of club would you join?", "options": {
        "Coding or Robotics": ["STEM"],
        "Theatre or Design": ["Creative"],
        "Debating or Social Work": ["Humanities"],
        "Entrepreneurship or Commerce": ["Business"]}},
    48: {"question": "What excites you about the future?", "options": {
        "Tech innovation": ["STEM"],
        "Creative freedom": ["Creative"],
        "Changing the world": ["Humanities"],
        "Owning a company": ["Business"]}},
    49: {"question": "Which subject feels most natural to you?", "options": {
        "Math or Science": ["STEM"],
        "English or Art": ["Creative"],
        "Social Science": ["Humanities"],
        "Economics or Accounts": ["Business"]}},
    50: {"question": "Which of these do you admire most?", "options": {
        "Engineers or Scientists": ["STEM"],
        "Authors or Designers": ["Creative"],
        "Activists or Leaders": ["Humanities"],
        "CEOs or Investors": ["Business"]}},

    # Aptitude Types (Q51–60)
    51: {"question": "You are best at solving:", "options": {
        "Logic puzzles": ["Logical"],
        "Creative challenges": ["Creative"],
        "Word games": ["Verbal"],
        "Number patterns": ["Numerical"]}},
    52: {"question": "Your strongest subject area is:", "options": {
        "Physics, Math": ["Logical"],
        "Drawing, Art": ["Creative"],
        "English, Literature": ["Verbal"],
        "Accounts, Data": ["Numerical"]}},
    53: {"question": "You enjoy assignments that involve:", "options": {
        "Formulas and reasoning": ["Logical"],
        "Visuals and imagination": ["Creative"],
        "Writing and vocabulary": ["Verbal"],
        "Graphs and calculation": ["Numerical"]}},
    54: {"question": "In puzzles or games, you prefer:", "options": {
        "Sudoku or logic grid": ["Logical"],
        "Pictionary or design challenge": ["Creative"],
        "Crosswords or anagrams": ["Verbal"],
        "Math riddles": ["Numerical"]}},
    55: {"question": "When thinking fast, your brain picks:", "options": {
        "Facts and cause-effect": ["Logical"],
        "Images and colours": ["Creative"],
        "Words and sentences": ["Verbal"],
        "Quantities and patterns": ["Numerical"]}},
    56: {"question": "Your friends say you are good at:", "options": {
        "Solving tough problems": ["Logical"],
        "Making things beautiful": ["Creative"],
        "Explaining things well": ["Verbal"],
        "Handling budgets or scores": ["Numerical"]}},
    57: {"question": "You find it easy to:", "options": {
        "Understand scientific logic": ["Logical"],
        "Create something original": ["Creative"],
        "Learn new words": ["Verbal"],
        "Work with percentages": ["Numerical"]}},
    58: {"question": "You like tasks that involve:", "options": {
        "Cause-effect analysis": ["Logical"],
        "Drawing/sketching": ["Creative"],
        "Reading or storytelling": ["Verbal"],
        "Tabulation or computation": ["Numerical"]}},
    59: {"question": "You struggle the least with:", "options": {
        "Reasoning questions": ["Logical"],
        "Art/design prompts": ["Creative"],
        "Essay writing": ["Verbal"],
        "Math or data tables": ["Numerical"]}},
    60: {"question": "Which activity feels most rewarding?", "options": {
        "Solving a complex problem": ["Logical"],
        "Finishing a creative project": ["Creative"],
        "Delivering a speech/story": ["Verbal"],
        "Balancing or budgeting": ["Numerical"]}}
}

weights = {
    "Personality": 1.0,
    "Learning Style": 0.9,
    "Behaviour": 0.8,
    "Emotional": 0.8,
    "Interest": 1.0,
    "Aptitude": 1.2
}

dimension_map = {
    "Personality": list(range(1, 11)),
    "Learning Style": list(range(11, 21)),
    "Behaviour": list(range(21, 31)),
    "Emotional": list(range(31, 41)),
    "Interest": list(range(41, 51)),
    "Aptitude": list(range(51, 61))
}

career_domains = {
    "STEM": ["Engineer", "Data Analyst", "AI Researcher", "Biotech Scientist"],
    "Creative": ["UX Designer", "Animator", "Content Creator", "Filmmaker"],
    "Social": ["Psychologist", "Policy Researcher", "Teacher", "NGO Worker"],
    "Business": ["Entrepreneur", "Marketing Analyst", "Financial Consultant"]
}

university_domains = {
    "STEM": ["MIT", "Stanford", "ETH Zurich", "IIT Bombay"],
    "Creative": ["Parsons School of Design", "NID India", "SCAD", "RMIT"],
    "Social": ["Sciences Po", "TISS", "LSE", "UCLA"],
    "Business": ["Wharton", "INSEAD", "London Business School", "IIM Ahmedabad"]
}

def calculate_scores(responses):
    scores_by_dim = {}
    for dim, q_ids in dimension_map.items():
        dim_scores = {}
        for q_id in q_ids:
            selected = responses.get(q_id)
            tags = questions[q_id]['options'].get(selected, [])
            for tag in tags:
                dim_scores[tag] = dim_scores.get(tag, 0) + weights[dim]
        scores_by_dim[dim] = dim_scores
    return scores_by_dim

def recommend_domain(scores_by_dim):
    summary = {}
    interests = scores_by_dim.get("Interest", {})
    top_interest = max(interests, key=interests.get) if interests else "General"
    if top_interest in career_domains:
        summary["Careers"] = career_domains[top_interest]
        summary["Universities"] = university_domains[top_interest]
    return summary

def generate_split_radar_charts(scores_by_dim):
    charts = {}
    for dimension, scores in scores_by_dim.items():
        if not scores:
            continue

        labels = list(scores.keys())
        values = list(scores.values())
        angles = np.linspace(0, 2 * np.pi, len(labels), endpoint=False).tolist()
        values += values[:1]
        angles += angles[:1]

        fig, ax = plt.subplots(figsize=(7, 7), subplot_kw=dict(polar=True))
        ax.plot(angles, values, 'o-', linewidth=2)
        ax.fill(angles, values, alpha=0.25)
        ax.set_yticklabels([])
        ax.set_xticks(angles[:-1])
        ax.set_xticklabels(labels, fontsize=10)
        ax.set_title(dimension)
        fig.subplots_adjust(top=0.85, bottom=0.1)

        tmpfile = tempfile.NamedTemporaryFile(delete=False, suffix=".png")
        plt.savefig(tmpfile.name)
        charts[dimension] = tmpfile.name
        plt.close(fig)
    return charts

def generate_summary(scores_by_dim):
    summary = ""
    for dim, score_map in scores_by_dim.items():
        if score_map:
            top_area = max(score_map, key=score_map.get)
            summary += f"\n- {dim}: Dominant trait = {top_area}"
    return summary

def generate_pdf(student_name, scores_by_dim, chart_paths, recommendations):
    pdf = FPDF()
    pdf.add_page()
    pdf.set_font("Arial", size=12)
    pdf.cell(200, 10, txt=f"Career Report: {student_name}", ln=True, align='C')
    pdf.ln(5)
    pdf.multi_cell(0, 10, txt="Your psychometric analysis across 6 core dimensions shows the following dominant traits:")
    summary = generate_summary(scores_by_dim)
    for line in summary.strip().split('\n'):
        pdf.multi_cell(0, 8, txt=line)

    pdf.add_page()
    pdf.set_font("Arial", 'B', 14)
    pdf.cell(0, 10, "Suggested Career Tracks & Universities", ln=True, align='C')
    pdf.set_font("Arial", size=12)
    for section, items in recommendations.items():
        pdf.multi_cell(0, 8, f"\n{section} Suggestions:")
        for item in items:
            pdf.multi_cell(0, 8, f"- {item}")

    for dim in dimension_map.keys():
        if dim in chart_paths:
            pdf.add_page()
            pdf.set_font("Arial", 'B', 14)
            pdf.cell(0, 10, f"{dim} Profile", ln=True, align='C')
            pdf.image(chart_paths[dim], x=30, y=30, w=150)

    output_buffer = BytesIO()
    pdf_output = pdf.output(dest='S').encode('latin1')
    output_buffer.write(pdf_output)
    output_buffer.seek(0)
    return output_buffer

# Streamlit app
st.markdown("""
    <style>
    .stRadio > div > label {font-weight: 500; font-size: 16px;}
    .stButton > button {width: 100%;}
    </style>
""", unsafe_allow_html=True)

st.title("🧠 Career Guidance Psychometric Test")
st.markdown("Answer all 60 questions to generate your personalised career insight report.")

student_name = st.text_input("👤 Enter your full name:")

if 'page' not in st.session_state:
    st.session_state.page = 0
if 'responses' not in st.session_state:
    st.session_state.responses = {}

responses = st.session_state.responses

pages = [
    ("Personality", list(range(1, 11))),
    ("Learning Style", list(range(11, 21))),
    ("Behaviour", list(range(21, 31))),
    ("Emotional", list(range(31, 41))),
    ("Interest", list(range(41, 51))),
    ("Aptitude", list(range(51, 61)))
]

# Progress bar and tracker
if 0 <= st.session_state.page < len(pages):
    progress = (st.session_state.page + 1) / len(pages)
    st.progress(progress)
    st.markdown(f"### Section {st.session_state.page + 1} of {len(pages)}")

# Completion overview
completed = [
    all(q_id in responses and responses[q_id] is not None for q_id in q_ids)
    for _, q_ids in pages
]
st.markdown("**Progress Check:**")
st.markdown(" ".join([
    f"✅ {name}" if done else f"⬜️ {name}"
    for (name, _), done in zip(pages, completed)
]))

if st.session_state.page < len(pages):
    dim_name, q_ids = pages[st.session_state.page]
    st.subheader(f"{dim_name} Questions")

    incomplete = False
    for q_id in q_ids:
        q_data = questions.get(q_id)
        if q_data:
            options = list(q_data["options"].keys())
            selected = st.radio(
                f"Q{q_id}. {q_data['question']}",
                options,
                index=options.index(responses[q_id]) if q_id in responses and responses[q_id] in options else -1,
                key=f"q_{q_id}"
            )
            responses[q_id] = selected if selected else None

    col1, col2, col3 = st.columns([1, 1, 1])
    with col1:
        if st.button("⬅️ Back") and st.session_state.page > 0:
            st.session_state.page -= 1
            st.rerun()
    with col2:
        if st.button("🔄 Reset"):
            st.session_state.responses = {}
            st.session_state.page = 0
            st.rerun()
    with col3:
        if st.button("➡️ Next"):
            if any(responses.get(q_id) is None for q_id in q_ids):
                st.warning("Please answer all questions before proceeding.")
            else:
                st.session_state.page += 1
                st.rerun()

elif st.session_state.page == len(pages):
    st.header("🎯 Review Your Dominant Traits")
    scores_by_dim = calculate_scores(responses)
    summary_text = generate_summary(scores_by_dim)
    st.markdown("### Summary:")
    st.text(summary_text)

    if st.button("📄 Generate Career Report"):
        if student_name and all(responses.get(q_id) in questions[q_id]['options'] for q_id in range(1, 61)):
            chart_paths = generate_split_radar_charts(scores_by_dim)
            pdf_bytes = generate_pdf(student_name, scores_by_dim, chart_paths)
            st.download_button("⬇️ Download Your Career Report", pdf_bytes, file_name=f"{student_name.replace(' ', '_')}_Career_Report.pdf")
        else:
            st.warning("Please answer all questions and provide your name.")
