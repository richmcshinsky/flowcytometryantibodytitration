import streamlit as st

def main():
    with st.sidebar:
        st.page_link('streamlit_app.py', label='Home')
        st.page_link('pages/01_Repository.py', label='Repository')
        st.page_link('pages/02_Contribute.py', label='Contribute')
        st.page_link('pages/03_Insights.py', label='Insights')
        st.page_link('pages/04_Contact.py', label='Contact')
        st.page_link('pages/05_Pricing.py', label='Pricing')
    st.write("Subscription benefits:")
    lst = ['access to the entire repository data', 
            'access to insights charts', 
            'tools to generate professional figures from your data']
    s = ''
    for i in lst:
        s += "- " + i + "\n"
    st.markdown(s)
    st.write("Pricing")
    lst = ["$xx/month for individual access", 
            "email about discounts for group and organizational level access",
            "free access for x months for contributing to repository"]
    s = ''
    for i in lst:
        s += "- " + i + "\n"
    st.markdown(s)

if __name__ == '__main__':
    main()