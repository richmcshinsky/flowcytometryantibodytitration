import streamlit as st
import plotly.express as px

if st.session_state['res']:
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
