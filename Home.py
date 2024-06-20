import streamlit as st
import streamlit_pandas as sp
from streamlit_gsheets import GSheetsConnection
# from streamlit_keycloak import login # https://github.com/bleumink/streamlit-keycloak

# TODO: add styling/theming
# TODO: contact form
# TODO: finish adding images 
# TODO: review data with Tony
# TODO: update contribute to only have essential columns as options

# TODO: I think we need a generic search box so someone can enter whatever is on their mind and see what we have to offer.
# TODO: In time, we will need a reference for any published data, DOI and/or PMCID may be sufficient.

# set up config for page
st.set_page_config(
    page_title='Flow Cytometry Antibody Titration Repository',
    layout="wide",
    #initial_sidebar_state="expanded"
)

conn = st.connection("gsheets", type=GSheetsConnection)
df = conn.read(worksheet="reviewed", ttl="30m")

columns = ["Antigen", "Clone", "Conjugate", "Test Tissue",
           "Test Cell Type", "Test Preparation", "Test Amount",
           "Image", "Target Species", "Host Species", "Isotype",
           "Supplier", "Catalougue #", "RRID", "Concentration",
           "Concentration (ug/mL)", "Titeration (ug/mL)",
           "Amount Tested (uL)", "Seperation Index", "Samples/vial",
           "Cost/sample", "Metal", "Metal Source", "Metal Catalogue #",
           "Detector", "Staining", "Source", "Publisher", "Paper",
           "Journal"]

create_data = {}
for c in columns:
    create_data[c] = "multiselect"

# Add filters
df = df[columns]
all_widgets = sp.create_widgets(df, create_data)
res = sp.filter_df(df, all_widgets)
if 'res' not in st.session_state:
    st.session_state['res'] = res
if 'columns' not in st.session_state:
    st.session_state['columns'] = columns

st.markdown("<h1 style='text-align: center; color: black;'>Metrdy</h1>", unsafe_allow_html=True)

# Removes download button on tables
st.markdown("""<style> [data-testid="stElementToolbar"] {display: none;} </style>""", unsafe_allow_html=True)

#st.title("Streamlit Keycloak example")
#keycloak = login(
#    url="http://localhost:8080",
#    realm="myrealm",
#    client_id="myclient",
#) 
# def main():
st.subheader("Welcome")
st.write("""This is a database of flow cytometry antibody titration data.
            You can look up titration data for planning experiments and making 
            informed purchasing decisions. Data is collected from various publications
            and through user contributions. """)
# st.divider()
st.subheader("What brings you here today?")
if st.button("Home"):
    st.switch_page("Home.py")
if st.button("Repository"):
    st.switch_page("pages/01_Repository.py")
if st.button("Contribute"):
    st.switch_page("pages/02_Contribute.py")
if st.button("Insights"):
    st.switch_page("pages/03_Insights.py")
if st.button("Contact"):
    st.switch_page("pages/04_Contact.py")
if st.button("Pricing"):
    st.switch_page("pages/05_Pricing.py")
# if keycloak.authenticated:
#     main()