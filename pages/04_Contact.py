import streamlit as st
import smtplib
from email.mime.text import MIMEText

st.set_page_config(page_title='Flow Cytometry Antibody Titration Repository', layout="wide")


with st.sidebar:
    st.page_link('streamlit_app.py', label='Home')
    st.page_link('pages/01_Repository.py', label='Repository')
    st.page_link('pages/02_Contribute.py', label='Contribute')
    st.page_link('pages/03_Insights.py', label='Insights')
    st.page_link('pages/04_Contact.py', label='Contact')
    st.page_link('pages/05_Pricing.py', label='Pricing')
    st.page_link('pages/06_Guided.py', label='Guided')

st.markdown("<h1 style='text-align: center; color: black;'>Metrdy</h1>", unsafe_allow_html=True)
st.divider()

import os
u = os.getenv("U")
secret = os.getenv("SECRET")
recipient = os.getenv("RECIPIENT")

st.write("submitting this form doesn't do anything yet FYI")    
with st.form("form2", clear_on_submit=True):
    name = st.text_input("Enter name")
    email_sender = st.text_input("Enter email")
    body = st.text_area("Enter message")
    password = ""
    email_receiver = "fcat.repository@gmail.com"
    if st.form_submit_button("Send Email"):
        try:
            msg = MIMEText(body)
            msg['From'] = email_sender
            msg['To'] = email_receiver
            msg['Subject'] = name

            server = smtplib.SMTP('smtp.gmail.com', 587)
            server.starttls()
            server.login(u, secret)
            server.sendmail(email_sender, email_receiver, msg.as_string())
            server.quit()
            st.success('Email sent successfully!')
        except:
            st.error("Email failed to send")
st.write("Or send email to: fcat.repository@gmail.com (can add file attachments this way)")

