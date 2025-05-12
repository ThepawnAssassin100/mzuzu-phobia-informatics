import streamlit as st
import pandas as pd
from datetime import datetime
from io import BytesIO

# Set Streamlit page configuration
st.set_page_config(page_title="Phobia Study - Mzuzu", page_icon="🧠", layout="centered")

# Title and Intro
st.title("🧠 Investigating the Prevalence of Phobias in Mzuzu City")
st.markdown("""
**Research Topic:** *Investigating the Prevalence of Phobias Across Different Demographics in Mzuzu City and the Role of Informatics in Promoting Mental Well-being*  
**Lead Researcher:** Henry Manda
""")

st.markdown("---")
st.header("📋 Participant Questionnaire")

# Initialize session data
if "responses" not in st.session_state:
    st.session_state.responses = pd.DataFrame(columns=[
        "Timestamp", "Name", "Age", "Gender", "Occupation", "Phobia Type", 
        "Severity (1-10)", "Known Duration (in years)", "Has Sought Help?", "Willingness to Receive Support"
    ])

# Questionnaire form
with st.form("phobia_form"):
    name = st.text_input("Full Name (Optional)")
    age = st.slider("Age", 10, 80)
    gender = st.selectbox("Gender", ["Male", "Female", "Other"])
    occupation = st.text_input("Occupation")
    phobia = st.selectbox("Phobia Type", [
        "Acrophobia (Fear of Heights)",
        "Arachnophobia (Fear of Spiders)",
        "Claustrophobia (Fear of Enclosed Spaces)",
        "Social Phobia", "Agoraphobia", "Other"
    ])
    severity = st.slider("Severity Level (1 = Mild, 10 = Extreme)", 1, 10)
    duration = st.number_input("How many years have you had this phobia?", min_value=0.0)
    sought_help = st.radio("Have you ever sought help for this phobia?", ["Yes", "No"])
    willing_support = st.radio("Would you like to receive information on how to manage phobias?", ["Yes", "No"])
    submitted = st.form_submit_button("✅ Submit Response")

if submitted:
    new_response = pd.DataFrame({
        "Timestamp": [datetime.now()],
        "Name": [name], "Age": [age], "Gender": [gender], "Occupation": [occupation],
        "Phobia Type": [phobia], "Severity (1-10)": [severity],
        "Known Duration (in years)": [duration],
        "Has Sought Help?": [sought_help],
        "Willingness to Receive Support": [willing_support]
    })
    st.session_state.responses = pd.concat([st.session_state.responses, new_response], ignore_index=True)
    st.success("Thank you! Your response has been recorded.")

# Show data
st.markdown("---")
st.header("📊 Survey Responses Summary")
if not st.session_state.responses.empty:
    st.dataframe(st.session_state.responses, use_container_width=True)

    # Basic Statistics
    st.markdown("### 🔍 Key Statistics")
    st.write("Total Responses:", len(st.session_state.responses))
    st.write("Most Common Phobia:", st.session_state.responses["Phobia Type"].mode()[0])
    st.write("Average Severity:", round(st.session_state.responses["Severity (1-10)"].mean(), 2))

    # Download CSV
    def convert_df(df):
        output = BytesIO()
        df.to_csv(output, index=False)
        return output.getvalue()

    st.download_button(
        label="📥 Download Data as CSV",
        data=convert_df(st.session_state.responses),
        file_name='mzuzu_phobia_survey.csv',
        mime='text/csv')
else:
    st.info("No responses yet. Fill the form above to begin collecting data.")

# Final note
st.markdown("---")
st.markdown("""
✅ This app was developed to demonstrate how **informatics tools** can be used to monitor and analyze **mental health trends** and improve **community well-being**.  
🔗 This project is maintained by Henry Manda and can be deployed through **GitHub and Streamlit Cloud**.
""")
