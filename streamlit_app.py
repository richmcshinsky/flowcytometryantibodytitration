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


# st.markdown("<h1 style='text-align: center; color: black;'>Metrdy</h1>", unsafe_allow_html=True)
#st.image("data/logoex.png")
col1, col2, col3, col4 = st.columns([2,3,1,1], gap="small")
with col2:
    st.image("data/logoex.png")
    st.markdown("""<h3 style='text-align: center; color: black;'>Cyto<u>metr</u>y Antibo<u>dy</u> Database</h3>""", unsafe_allow_html=True)
with col3:
    st.markdown('#')
    st.link_button("", "https://www.merriam-webster.com/dictionary/ma%C3%AEtre%20d%27", icon=":material/brand_awareness:")

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


