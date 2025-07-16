"import streamlit as st
import pandas as pd
import ast

# --- CONFIGURATION ---
st.set_page_config(
    page_title=""Career Guidance Psychometric Test"",
    page_icon=""🧠"",
    layout=""centered"",
)

# --- DATA LOADING ---
@st.cache_data
def load_questions_data():
    """"""
    Loads and preprocesses the questions from the CSV file.
    The @st.cache_data decorator ensures this function only runs once.
    """"""
    try:
        df = pd.read_csv('30-Question_Psychometric_Test_with_Themes.csv')
        # Convert string representations of dictionaries to actual dictionaries
        for col in ['Weights A', 'Weights B', 'Weights C', 'Weights D']:
            df[col] = df[col].apply(ast.literal_eval)
        return df
    except FileNotFoundError:
        st.error(""The question file '30-Question_Psychometric_Test_with_Themes.csv' was not found."")
        st.stop()
    except Exception as e:
        st.error(f""An error occurred while loading the questions: {e}"")
        st.stop()

# --- REPORT GENERATION ---
def generate_report(user_data, df):
    """"""
    Analyzes the user's answers and generates a detailed report.
    """"""
    scores = {
        'Career Lines': {},
        'Role Types': {}
    }

    # Define all possible categories to initialize scores
    career_lines = ['Linear', 'Horizontal', 'Diagonal', 'Non-linear']
    role_types = ['Specialist', 'Generalist', 'Creative', 'Entrepreneurial', 'Administrative',
                  'Technical', 'Human Resources', 'Sales/Marketing', 'Customer Service', 'Leadership', 'Other']

    for line in career_lines:
        scores['Career Lines'][line] = 0
    for r_type in role_types:
        scores['Role Types'][r_type] = 0

    # Calculate scores based on user answers
    for q_idx, answer_key in user_data[""answers""].items():
        if answer_key: # Ensure an answer was given
            # The answer_key is like 'Option A', 'Option B', etc.
            # We need to get the corresponding weights column, e.g., 'Weights A'
            weights_col = f""Weights {answer_key.split(' ')[-1]}""
            weights = df.loc[q_idx, weights_col]
            for key, value in weights.items():
                if key in scores['Career Lines']:
                    scores['Career Lines'][key] += value
                if key in scores['Role Types']:
                    scores['Role Types'][key] += value

    # Start building the report string
    report = f""Psychometric Test Report for: {user_data['name']}\n""
    report += ""=""*40 + ""\n\n""

    # Career Line Analysis
    report += ""I. CAREER LINE ANALYSIS (Progression Style):\n""
    sorted_career = sorted(scores['Career Lines'].items(), key=lambda item: item[1], reverse=True)
    for career, score in sorted_career:
        report += f""- {career}: {score} points\n""
    report += f""\nYour responses suggest a preference for a **{sorted_career[0][0]}** career progression. This path is characterized by...""
    # You can add descriptions for each career line here
    report += ""\n\n""

    # Role Type Analysis
    report += ""II. ROLE TYPE ANALYSIS (Preferred Work Environment):\n""
    sorted_roles = sorted(scores['Role Types'].items(), key=lambda item: item[1], reverse=True)
    for role, score in sorted_roles:
        report += f""- {role}: {score} points\n""
    report += f""\nYour dominant role type appears to be **{sorted_roles[0][0]}**. This indicates you might thrive in roles that are...""
    # You can add descriptions for each role type here
    report += ""\n\n""

    # Academic Performance
    report += ""III. ACADEMIC PERFORMANCE:\n""
    has_marks = False
    for i in range(5):
        subject = user_data['subjects'][i]
        mark = user_data['marks'][i]
        if subject and mark:
            report += f""- {subject}: {mark}\n""
            has_marks = True
    if not has_marks:
        report += ""No academic marks were provided.\n""

    report += ""\n\n--- END OF REPORT ---\n""
    return report

# --- UI RENDERING FUNCTIONS ---

def update_answer(q_idx, option_map):
    """"""Callback function to update the user's answer in session state.""""""
    widget_key = f""q_{q_idx}""
    answer_text = st.session_state[widget_key] # Get the selected value from the widget's state
    
    if answer_text:
        # Find which option key ('Option A', 'Option B', etc.) the answer text corresponds to
        selected_option_key = [k for k, v in option_map.items() if v == answer_text][0]
        # Store this key in our user_data dictionary
        st.session_state.user_data[""answers""][q_idx] = selected_option_key

def render_welcome_page():
    st.title(""Welcome to the Career Guidance Test"")
    st.write(""""""
    This test is designed to help understand your psychology and aspirations to correlate them with potential career paths.
    Please answer all questions thoughtfully.
    """""")
    st.markdown(""---"")
    col1, col2 = st.columns(2)
    with col1:
        if st.button(""I am a Student""):
            st.session_state.page = ""details""
            st.rerun()
    with col2:
        if st.button(""I am a Parent""):
            st.session_state.page = ""details""
            st.rerun()

def render_details_page():
    st.title(""Student Details"")
    with st.form(""details_form""):
        name = st.text_input(""Student's Name"", st.session_state.user_data.get('name', ''))
        contact = st.text_input(""Contact Number (Optional)"", st.session_state.user_data.get('contact', ''))
        submitted = st.form_submit_button(""Start Test"")
        if submitted:
            if not name:
                st.warning(""Please enter a name to proceed."")
            else:
                st.session_state.user_data['name'] = name
                st.session_state.user_data['contact'] = contact
                st.session_state.page = ""questions""
                st.rerun()
    if st.button(""Back""):
        st.session_state.page = ""welcome""
        st.rerun()


def render_question_pages(df):
    theme = st.session_state.themes[st.session_state.current_theme_index]
    st.title(f""Section {st.session_state.current_theme_index + 1}: {theme}"")

    questions_in_theme = df[df['Theme'] == theme]

    for idx, row in questions_in_theme.iterrows():
        st.markdown(f""**{row['Question']}**"")
        options = {f""Option {opt}"": row[f'Option {opt}'] for opt in ['A', 'B', 'C', 'D']}
        
        # Using on_change callback to update state safely
        st.radio(
            ""Select an option:"",
            options.values(),
            key=f""q_{idx}"",
            label_visibility=""collapsed"",
            on_change=update_answer,
            args=(idx, options) # Pass necessary arguments to the callback
        )

    st.markdown(""---"")
    col1, col2 = st.columns(2)
    with col1:
        if st.session_state.current_theme_index > 0:
            if st.button(""Back""):
                st.session_state.current_theme_index -= 1
                st.rerun()
    with col2:
        if st.session_state.current_theme_index < len(st.session_state.themes) - 1:
            if st.button(""Next""):
                st.session_state.current_theme_index += 1
                st.rerun()
        else:
            if st.button(""Proceed to Final Step""):
                st.session_state.page = ""marks""
                st.rerun()

def render_marks_page():
    st.title(""Final Step: Academic Performance"")
    st.write(""Please enter your top 5 subjects and the marks obtained (e.g., percentage, grade)."")

    with st.form(""marks_form""):
        for i in range(5):
            col1, col2 = st.columns(2)
            with col1:
                st.session_state.user_data['subjects'][i] = st.text_input(f""Subject {i+1}"", key=f""sub_{i}"")
            with col2:
                st.session_state.user_data['marks'][i] = st.text_input(f""Marks for Subject {i+1}"", key=f""mark_{i}"")
        
        submitted = st.form_submit_button(""Generate My Report"")
        if submitted:
            st.session_state.page = ""report""
            st.rerun()

    if st.button(""Back to Questions""):
        st.session_state.page = ""questions""
        st.rerun()

def render_report_page(df):
    st.title(""Your Personalized Career Report"")
    
    with st.spinner(""Analyzing your responses and generating your report...""):
        report_str = generate_report(st.session_state.user_data, df)
        st.session_state.report = report_str

    st.text_area(""Report"", st.session_state.report, height=400)
    
    st.download_button(
        label=""Download Report"",
        data=st.session_state.report,
        file_name=f""Career_Report_{st.session_state.user_data.get('name', 'student')}.txt"",
        mime=""text/plain""
    )

    if st.button(""Start Over""):
        # Reset session state completely
        for key in list(st.session_state.keys()):
            del st.session_state[key]
        st.rerun()


# --- MAIN APP LOGIC ---
def main():
    # Load data
    df = load_questions_data()

    # Initialize session state variables
    if 'page' not in st.session_state:
        st.session_state.page = ""welcome""
        st.session_state.themes = df['Theme'].unique().tolist()
        st.session_state.current_theme_index = 0
        st.session_state.user_data = {
            ""name"": """",
            ""contact"": """",
            ""answers"": {},
            ""subjects"": [""""] * 5,
            ""marks"": [""""] * 5
        }
        st.session_state.report = """"

    # Page routing
    if st.session_state.page == ""welcome"":
        render_welcome_page()
    elif st.session_state.page == ""details"":
        render_details_page()
    elif st.session_state.page == ""questions"":
        render_question_pages(df)
    elif st.session_state.page == ""marks"":
        render_marks_page()
    elif st.session_state.page == ""report"":
        render_report_page(df)

if __name__ == ""__main__"":
    main()"
