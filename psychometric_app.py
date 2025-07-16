import streamlit as st
import pandas as pd

# --- DATA LOADING (Cached for performance) ---
@st.cache_data
def load_data():
    """Loads all necessary CSV files into dataframes."""
    try:
        df_questions = pd.read_csv("30-Questions_test.xlsx - questions_set.csv")
        df_weights = pd.read_csv("30-Questions_test.xlsx - weights_set.csv")
        df_stem = pd.read_csv("Career Guidance Test.xlsx - stem_set.csv")
        df_humanities = pd.read_csv("Career Guidance Test.xlsx - humanities_set.csv")
        df_arts = pd.read_csv("Career Guidance Test.xlsx - arts_set.csv")
        return df_questions, df_weights, df_stem, df_humanities, df_arts
    except FileNotFoundError as e:
        st.error(f"Error loading data files: {e}. Please make sure all CSV files are in the same folder as the app.py script.")
        return None, None, None, None, None

# --- HELPER FUNCTIONS ---
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
    # Note: The 'Art' category from the files is not used here as the subject list doesn't contain art subjects.
    # This can be expanded if more subjects are added.

def calculate_results():
    """Calculates the final results from MCQ answers."""
    df_questions, df_weights, _, _, _ = load_data()

    role_types = ['Creative', 'Specialist', 'Generalist', 'Administrative',
                  'Entrepreneurial', 'Customer Service', 'Technical',
                  'Human Resources', 'Sales/Marketing', 'Leadership', 'Other']
    career_lines = ['Linear', 'Non-linear', 'Diagonal', 'Horizontal']

    role_type_scores = {role: 0 for role in role_types}
    career_line_scores = {line: 0 for line in career_lines}

    # Retrieve answers from session state
    for i in range(len(df_questions)):
        answer = st.session_state[f'q_{i}']
        # The answer format from st.radio is "A. {Option Text}". We only need "A".
        answer_letter = answer.split('.')[0]

        weights_str = df_weights.loc[i, f'Option {answer_letter} Weights']
        if isinstance(weights_str, str):
            parts = weights_str.split(', ')
            for part in parts:
                key, value = part.split(' = ')
                if key in role_type_scores:
                    role_type_scores[key] += int(value)
                elif key in career_line_scores:
                    career_line_scores[key] += int(value)

    st.session_state.role_type = max(role_type_scores, key=role_type_scores.get)
    st.session_state.career_line = max(career_line_scores, key=career_line_scores.get)


# --- MAIN APP ---

# Load dataframes
df_questions, df_weights, df_stem, df_humanities, df_arts = load_data()

# Initialize session state to manage steps
if 'step' not in st.session_state:
    st.session_state.step = 1
    st.session_state.user_data = {}

st.title("Psychometric Career Guidance Test")

# --- STEP 1: Personal Info ---
if st.session_state.step == 1:
    st.header("Step 1: Personal Information")
    with st.form("personal_info_form"):
        name = st.text_input("Enter your full name", key="name")
        number = st.text_input("Enter your 10-digit mobile number", key="number", max_chars=10)
        submitted = st.form_submit_button("Next")
        if submitted:
            if name and number.isdigit() and len(number) == 10:
                st.session_state.user_data['name'] = name
                st.session_state.user_data['number'] = number
                st.session_state.step = 2
                st.experimental_rerun()
            else:
                st.error("Please enter a valid name and a 10-digit mobile number.")

# --- STEP 2: Academic Scores ---
if st.session_state.step == 2:
    st.header("Step 2: Academic Scores")
    st.write("Please select your top 5 subjects and enter your scores (out of 100).")
    subjects = ["Maths", "Physics", "Chemistry", "Biology", "History", "Civics",
                "Geography", "Economics", "Statistics", "Computer Science", "English"]
    with st.form("academic_scores_form"):
        selected_subjects_scores = {}
        cols = st.columns(2)
        for i in range(5):
            subject = cols[0].selectbox(f"Select Subject {i+1}", options=subjects, key=f"sub_{i}")
            score = cols[1].number_input(f"Score for Subject {i+1}", min_value=0, max_value=100, key=f"score_{i}")
            selected_subjects_scores[subject] = score

        submitted = st.form_submit_button("Next")
        if submitted:
            # Check for duplicate subjects
            if len(selected_subjects_scores) != 5:
                st.error("Please select 5 unique subjects.")
            else:
                st.session_state.user_data['academic_scores'] = selected_subjects_scores
                st.session_state.step = 3
                st.experimental_rerun()

# --- STEP 3: MCQ Test ---
if st.session_state.step == 3 and df_questions is not None:
    st.header("Step 3: Psychometric Test")
    st.write("Please answer the following questions honestly.")
    with st.form("mcq_form"):
        for index, row in df_questions.iterrows():
            st.subheader(f"Q{index+1}: {row['Question']}")
            options = [
                f"A. {row['Option A']}",
                f"B. {row['Option B']}",
                f"C. {row['Option C']}",
                f"D. {row['Option D']}"
            ]
            st.radio("Your choice:", options, key=f'q_{index}')
            st.markdown("---") # Visual separator

        submitted = st.form_submit_button("Calculate My Results")
        if submitted:
            calculate_results()
            st.session_state.step = 4
            st.experimental_rerun()

# --- STEP 4: Show Report ---
if st.session_state.step == 4:
    st.header("Your Personalized Career Guidance Report")
    st.balloons()

    # Retrieve results
    name = st.session_state.user_data.get('name', 'Student')
    role_type = st.session_state.get('role_type')
    career_line = st.session_state.get('career_line')
    academic_scores = st.session_state.user_data.get('academic_scores')

    if not all([role_type, career_line, academic_scores]):
        st.error("Something went wrong during calculation. Please try again.")
        st.button("Start Over", on_click=lambda: st.session_state.clear())
    else:
        subject_interest = determine_subject_interest(academic_scores)

        st.success(f"Hello {name}, based on your answers, here is your profile:")
        st.write(f"**Your Academic Interest Area:** {subject_interest}")
        st.write(f"**Your Dominant Role Type:** {role_type}")
        st.write(f"**Your Natural Career Line:** {career_line}")

        # Select correct dataframe
        if subject_interest == "STEM":
            df_guidance = df_stem
        elif subject_interest == "Humanities":
            df_guidance = df_humanities
        else:
            df_guidance = df_arts

        # Find the report
        report = df_guidance[
            (df_guidance['Role Type'] == role_type) &
            (df_guidance['Career Line'] == career_line)
        ]

        if not report.empty:
            report_data = report.iloc[0]
            st.info(f"**A message for you:** {report_data['Message']}")
            st.markdown("---")
            st.subheader("Career & Education Recommendations")
            st.markdown(f"**Example Career Options:** {report_data['Example Career Options']}")
            st.markdown(f"**Potential Companies to Aim For:** {report_data['Potential Companies to Aim For']}")
            st.markdown(f"**Possible Entry-Level Designations:** {report_data['Entry-Level Designations']}")
            st.markdown(f"**Top Universities in India:** {report_data['Top Universities India']}")
            st.markdown(f"**Top Universities Abroad:** {report_data['Top Universities  Globally']}") # Corrected column name
        else:
            st.warning("Could not find a specific career recommendation for your unique combination of results.")
            st.write("This may indicate a very special profile. We encourage you to explore interdisciplinary fields that blend your interests and strengths.")

        if st.button("Take the Test Again"):
            st.session_state.clear()
            st.experimental_rerun()
