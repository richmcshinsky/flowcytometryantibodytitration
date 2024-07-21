import streamlit as st
from streamlit_gsheets import GSheetsConnection
import streamlit_pandas as sp

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

st.write("What protocol do you plan to run?")
col1, col2 = st.columns(2, gap="small")
with col1:
    if st.button(label="Flow Cytometry", use_container_width=True):
        protocol = "flow"
with col2:
    if st.button(label="Mass Cytometry", use_container_width=True):
        protocol = "mass"

