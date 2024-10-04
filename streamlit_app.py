import streamlit as st
from st_paywall import add_auth
# from streamlit_keycloak import login # https://github.com/bleumink/streamlit-keycloak
  
# TODO: data: validation second pass
# TODO: make repository sample a hard coded file saved in project to save hits to google sheets connection


st.set_page_config(page_title='Flow Cytometry Antibody Titration Repository', layout="wide")

# builds the sidebar menu
with st.sidebar:
    st.page_link('streamlit_app.py', label='Home')
    st.page_link('pages/01_Repository.py', label='Repository')
    st.page_link('pages/02_Contribute.py', label='Contribute')
    st.page_link('pages/03_Insights.py', label='Insights')
    st.page_link('pages/04_Contact.py', label='Contact')
    st.page_link('pages/05_Pricing.py', label='Pricing')
    st.page_link('pages/06_Guided.py', label='Guided')
    #st.page_link('pages/07_Tools.py', label='Tools')
    #st.page_link('pages/08_FAQ.py', label='FAQ')
    # References
    # Search
    # Maybe cahnge purchase into tools?

col1,col2 = st.columns(2)
with col1:
    st.markdown("<h1 style='text-align: center; color: black;'>Metrdy</h1> ", unsafe_allow_html=True)
with col2:
    st.markdown("<a href=https://www.merriam-webster.com/dictionary/ma%C3%AEtre%20d%27><img src=./app/static/soundicon.png></a>")
    # st.markdown("[![Click me](./app/static/soundicon.png)](https://www.merriam-webster.com/dictionary/ma%C3%AEtre%20d%27)")
st.divider()

st.subheader("Welcome")
st.write("""This is a database of flow cytometry antibody titration data.
            You can look up titration data for planning experiments and for making 
            informed purchasing decisions. Data is collected from various publications
            and through user contributions. """)

st.subheader("What brings you here today?")

col1, col2 = st.columns(2, gap="small")
with col1:
    if st.button(label="Repository", use_container_width=True, help="""Click here to go explore the repository data. 
                Filters will appear in the same navigation tab on the left."""):
        st.switch_page("pages/01_Repository.py")
with col2:
    if st.button(label="Contribute", use_container_width=True, help="""Add to the repository using your own data. 
                Free subscriptions are offered for accepted contributions!"""):
        st.switch_page("pages/02_Contribute.py")
with col1:
    if st.button(label="Insights", use_container_width=True, help="See visualizations and summaries about repository data."):
        st.switch_page("pages/03_Insights.py")
with col2:
    if st.button(label="Contact", use_container_width=True, help="Form to send an email."):
        st.switch_page("pages/04_Contact.py")
with col1:
    if st.button(label="Pricing", use_container_width=True, help="Explanations on subscription pricing and benefits"):
        st.switch_page("pages/05_Pricing.py")
with col2:
    if st.button(type="primary", label="Not sure where to start?", use_container_width=True, help="Guided walkthrough for easy navigation."):
        st.switch_page("pages/06_Guided.py")

st.subheader("Watch our short demo video to see what you can do!")

st.write("To test login use https://docs.stripe.com/testing#cards")
add_auth(required=True)
st.write("Login successful!")
