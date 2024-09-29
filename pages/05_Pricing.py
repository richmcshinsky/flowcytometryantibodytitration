import streamlit as st

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

with st.container():
    st.markdown("<h2 style='text-align: center; color: black;'>Repository benefits</h2>", unsafe_allow_html=True)
    st.image("data/repo benifits.png")

with st.container():
    st.markdown("<h2 style='text-align: center; color: black;'>Subscription benefits</h2>", unsafe_allow_html=True)
    st.image("data/sub benifits.png")

with st.container():
    st.markdown("<h2 style='text-align: center; color: black;'>Pricing</h2>", unsafe_allow_html=True)
    st.image("data/pricing.png")
