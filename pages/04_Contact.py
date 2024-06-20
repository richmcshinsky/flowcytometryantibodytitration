import streamlit as st

st.write("submitting this form doesn't do anything yet FYI")    
with st.form("form2", clear_on_submit=True):
    name = st.text_input("Enter name")
    email = st.text_input("Enter email")
    message = st.text_area("Enter message")
    submit = st.form_submit_button("Submit")
st.write("Or send email to: fcat.repository@gmail.com (can add file attachments this way)")