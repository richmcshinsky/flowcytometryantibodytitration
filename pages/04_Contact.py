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


#########################################################################
#                   STREAMLIT CONTACT FORM TEMPLATE                     #
# Version: 0.2.0                                                        #
# License: MIT License (https://opensource.org/license/mit/)            #
# Author: João L. Neto (https://github.com/jlnetosci/)                  #
# Release date: 2023-11-07                                              #
# Documentation: https://github.com/jlnetosci/streamlit-contact-form    #
# Credit is not mandatory, but it is kindly appreciated.                #
# For a subtle link to github you may just uncomment the last line.     #
#########################################################################

import streamlit as st
import smtplib
import os

from email_validator import validate_email, EmailNotValidError
from email.mime.text import MIMEText
from email.mime.multipart import MIMEMultipart

## Page configuration options
st.set_page_config(layout="wide") # column widths set below are dependent on the layout being set to wide

## Load secrets.toml variables
server = os.getenv("SERVER")
port = os.getenv("PORT")
u = os.getenv("U")
secret = os.getenv("SECRET")
recipient = os.getenv("RECIPIENT")

## Contact Form
st.header("Contact Form")

# col1, col2, col3, col4 =  st.columns([3, 0.25, 1, 0.25]) # column widths for a balanced distribution of elements in the page

## Contact form
# with col1: # left side of the layout
email = st.text_input("**Your email***", value=st.session_state.get('email', ''), key='email') # input widget for contact email
message = st.text_area("**Your message***", value=st.session_state.get('message', ''), key='message') # input widget for message

st.markdown('<p style="font-size: 13px;">*Required fields</p>', unsafe_allow_html=True) # indication to user that both fields must be filled

if st.button("Send", type="primary"):
    if not email or not message:
        st.error("Please fill out all required fields.") # error for any blank field
    else:
        try:
            # Robust email validation
            valid = validate_email(email, check_deliverability=True)

            # Email configuration - **IMPORTANT**: for security these details should be present in the "Secrets" section of Streamlit
            
            smtp_server = server
            smtp_port = port
            smtp_username = u
            smtp_password = secret
            recipient_email = recipient

            ## Create an SMTP connection
            server = smtplib.SMTP(smtp_server, smtp_port)
            server.starttls()
            server.login(smtp_username, smtp_password)

            ## Compose the email message
            subject = "Contact Form Submission" # subject of the email you will receive upon contact.
            body = f"Email: {email}\nMessage: {message}"
            msg = MIMEMultipart()
            msg['From'] = smtp_username
            msg['To'] = recipient_email
            msg['Subject'] = subject
            msg.attach(MIMEText(body, 'plain'))

            ## Send the email
            server.sendmail(smtp_username, recipient_email, msg.as_string())

            ## Send the confirmation email to the message sender # If you do not want to send a confirmation email leave this section commented
            #current_datetime = datetime.datetime.now()
            #formatted_datetime = current_datetime.strftime("%Y-%m-%d %H:%M:%S")
            #confirmation_subject = f"Confirmation of Contact Form Submission ({formatted_datetime})"
            #confirmation_body = f"Thank you for contacting us! Your message has been received.\n\nYour message: {message}"
            #confirmation_msg = MIMEMultipart()
            #confirmation_msg['From'] = smtp_username
            #confirmation_msg['To'] = email  # Use the sender's email address here
            #confirmation_msg['Subject'] = confirmation_subject
            #confirmation_msg.attach(MIMEText(confirmation_body, 'plain'))
            #server.sendmail(smtp_username, email, confirmation_msg.as_string())

            ## Close the SMTP server connection
            server.quit()

            st.success("Sent successfully!") # Success message to the user.
                    
        except EmailNotValidError as e:
            st.error(f"Invalid email address. {e}") # error in case any of the email validation checks have not passed








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
            server.login(email_sender, password)
            server.sendmail(email_sender, email_receiver, msg.as_string())
            server.quit()
            st.success('Email sent successfully!')
        except:
            st.error("Email failed to send")
st.write("Or send email to: fcat.repository@gmail.com (can add file attachments this way)")

