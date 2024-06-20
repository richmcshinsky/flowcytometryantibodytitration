import streamlit as st
import plotly.express as px
import pandas as pd

def main():
    with st.sidebar:
        st.page_link('streamlit_app.py', label='Home')
        st.page_link('pages/01_Repository.py', label='Repository')
        st.page_link('pages/02_Contribute.py', label='Contribute')
        st.page_link('pages/03_Insights.py', label='Insights')
        st.page_link('pages/04_Contact.py', label='Contact')
        st.page_link('pages/05_Pricing.py', label='Pricing')

    if isinstance(st.session_state['res'], pd.DataFrame):
        st.write("Plot data comming from " + str(len(st.session_state['res']["Source"].unique())) + " data sources.")
        fig = px.bar(st.session_state['res']["Antigen"].value_counts()[:20])
        st.plotly_chart(fig, use_container_width=True)
        fig = px.bar(st.session_state['res']["Conjugate"].value_counts()[:20])
        st.plotly_chart(fig, use_container_width=True)
        fig = px.bar(st.session_state['res']["Clone"].value_counts()[:20])
        st.plotly_chart(fig, use_container_width=True)
        fig = px.bar(st.session_state['res']["Supplier"].value_counts()[:20])
        st.plotly_chart(fig, use_container_width=True)
        fig = px.bar(st.session_state['res']["Concentration"].value_counts()[:20])
        st.plotly_chart(fig, use_container_width=True)

if __name__ == '__main__':
    main()
