import streamlit as st
from st_paywall import add_auth
# from streamlit_keycloak import login # https://github.com/bleumink/streamlit-keycloak

st.set_page_config(page_title='Flow Cytometry Antibody Titration Repository', layout="wide")

# builds the sidebar menu
with st.sidebar:
    st.page_link('streamlit_app.py', label='Home')
    st.page_link('pages/03_Discover.py', label='Discover')          # tool: see pricing comparisons and other figures
    st.page_link('pages/04_Create.py', label='Create')             # tool: to generate plots
    st.page_link('pages/05_Plan.py', label='Plan')                 # tool: guided walkthrough 
    st.page_link('pages/06_Pricing.py', label='Pricing')     
    st.page_link('pages/02_Contribute.py', label='Contribute') 
    


st.markdown("<h1 style='text-align: center; color: black;'>Metrdy</h1> ", unsafe_allow_html=True)
# st.html("""<a href="https://www.merriam-webster.com/dictionary/ma%C3%AEtre%20d%27"><img src="https://drive.google.com/file/d/1j4VZ_kqPD3r1DpsmHOiLVZyVF3zGRsEZ/view?usp=sharing" width="200" /></a>""")
# st.markdown("[![Click me](./app/static/soundicon.png)](https://www.merriam-webster.com/dictionary/ma%C3%AEtre%20d%27)")
st.divider()

st.markdown("<h3 style='text-align: center; color: black;'>Welcome</h3>", unsafe_allow_html=True)

st.write("""Our aim is to democratize flow cytometry antibody data and give you the necessary tools to significantly 
         save your money and time. You will be able to look up curated data from publications and user contributions to 
         easily make informed purchasing decisions between suppliers, with optimal concentrations from validated research. 
         Another prime example of the potential use of our tools is the ability to painlessly generate publication quality figures 
         from your own data. Anyone is welcome to contribute to expanding the Metrdy repository.""")

st.markdown("<h3 style='text-align: center; color: black;'>How can we serve you today?</h3>", unsafe_allow_html=True)

col1, col2, col3 = st.columns(3, gap="small")
with col1:
    if st.button(type="primary", label="Discover", use_container_width=True, help="See visualizations and insights to compare pricing between suppliers and other data"):
        st.switch_page("pages/03_Discover.py")
    st.image("data/ex1.png")
with col2:
    if st.button(label="Create", use_container_width=True, help="All in one tool to generate advanced figures"):
        st.switch_page("pages/04_Create.py")
    st.image("data/ex2.png")
with col3:
    if st.button(label="Plan", use_container_width=True, help="Guided walkthrough tool for painless results"):
        st.switch_page("pages/05_Plan.py")
    st.image("data/ex3.1.png")
    st.image("data/ex3.2.png")
    st.image("data/ex3.3.png")
    st.image("data/ex3.4.png")

st.markdown("<h3 style='text-align: center; color: black;'>Watch our short demo video to see what you can do!</h3>", unsafe_allow_html=True)

st.write("To test login use https://docs.stripe.com/testing#cards")
add_auth(required=True)
st.write("Login successful!")


html_content = """<div style="display: flex; align-items: center; justify-content: center; gap: 10px;"><a href="https://www.merriam-webster.com/dictionary/ma%C3%AEtre%20d%27" target="_blank"><svg xmlns="http://www.w3.org/2000/svg" viewBox="0 0 512 512" width="25" height="25" fill="{color}"><!--!Font Awesome Free 6.5.1 by @fontawesome - https://fontawesome.com License - https://fontawesome.com/license/free Copyright 2024 Fonticons, Inc.--><path d="M512 256C512 114.6 397.4 0 256 0S0 114.6 0 256C0 376 82.7 476.8 194.2 504.5V334.2H141.4V256h52.8V222.3c0-87.1 39.4-127.5 125-127.5c16.2 0 44.2 3.2 55.7 6.4V172c-6-.6-16.5-1-29.6-1c-42 0-58.2 15.9-58.2 57.2V256h83.6l-14.4 78.2H287V510.1C413.8 494.8 512 386.9 512 256h0z"/></svg></a></div>"""
st.markdown(html_content, unsafe_allow_html=True)


