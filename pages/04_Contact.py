import streamlit as st

def main():
    with st.sidebar:
        st.page_link('streamlit_app.py', label='Home')
        st.page_link('pages/01_Repository.py', label='Repository')
        st.page_link('pages/02_Contribute.py', label='Contribute')
        st.page_link('pages/03_Insights.py', label='Insights')
        st.page_link('pages/04_Contact.py', label='Contact')
        st.page_link('pages/05_Pricing.py', label='Pricing')

    st.write("submitting this form doesn't do anything yet FYI")    
    with st.form("form2", clear_on_submit=True):
        name = st.text_input("Enter name")
        email = st.text_input("Enter email")
        message = st.text_area("Enter message")
        submit = st.form_submit_button("Submit")
    st.write("Or send email to: fcat.repository@gmail.com (can add file attachments this way)")

if __name__ == '__main__':
    main()
