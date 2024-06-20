import streamlit as st

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

    st.write("Subscription benefits:")

if __name__ == '__main__':
    main()