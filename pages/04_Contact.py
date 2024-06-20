import streamlit as st

st.set_page_config(page_title='Flow Cytometry Antibody Titration Repository', layout="wide")

def main():
    with st.sidebar:
        st.page_link('streamlit_app.py', label='Home')
        st.page_link('pages/01_Repository.py', label='Repository')
        st.page_link('pages/02_Contribute.py', label='Contribute')
        st.page_link('pages/03_Insights.py', label='Insights')
        st.page_link('pages/04_Contact.py', label='Contact')
        st.page_link('pages/05_Pricing.py', label='Pricing')
        st.page_link('pages/06_Purchase.py', label='Purchase')

    st.markdown("<h1 style='text-align: center; color: black;'>Metrdy</h1>", unsafe_allow_html=True)
    st.divider()

    st.write("submitting this form doesn't do anything yet FYI")    
    with st.form("form2", clear_on_submit=True):
        name = st.text_input("Enter name")
        email = st.text_input("Enter email")
        message = st.text_area("Enter message")
        submit = st.form_submit_button("Submit")
    st.write("Or send email to: fcat.repository@gmail.com (can add file attachments this way)")

if __name__ == '__main__':
    main()
