import streamlit as st
import pandas as pd
import streamlit_pandas as sp
from streamlit_gsheets import GSheetsConnection
import plotly.express as px
# from streamlit_keycloak import login # https://github.com/bleumink/streamlit-keycloak

# TODO: add styling/theming
# TODO: contact form
# TODO: finish adding images 
# TODO: review data with Tony
# TODO: update contribute to only have essential columns as options

# TODO: The links could be condensed to "Image here" links. 
# TODO: I think we need a generic search box so someone can enter whatever is on their mind and see what we have to offer.
# TODO: In time, we will need a reference for any published data, DOI and/or PMCID may be sufficient.
# TODO: I am visioning a home page that shows an intro/how to, something like "What brings you here today, button for add titration data, button for look up an antibody I already have, button for shop for antibodies based on price/test, etc."

# set up config for page
st.set_page_config(
    page_title='Flow Cytometry Antibody Titration Repository',
    layout="wide",
    initial_sidebar_state="expanded"
)

st.markdown("<h1 style='text-align: center; color: black;'>Metrdy</h1>", unsafe_allow_html=True)
# st.image(logo_url, width=100) 
# st.title("Metrdy")
#col1, mid, col2 = st.columns([1,1,20])
#with col1:
#    st.image('row_2_col_1.jpg') #, width=60)
#with col2:
#    st.header('A Name')


tab1, tab2, tab3, tab5, tab6 = st.tabs(["Repository", "Contribute", "Insights", "Contact", "Pricing"]) #  tab4, "FAQ"

# Removes download button on tables
st.markdown("""<style> [data-testid="stElementToolbar"] {display: none;} </style>""", unsafe_allow_html=True)

#st.title("Streamlit Keycloak example")
#keycloak = login(
#    url="http://localhost:8080",
#    realm="myrealm",
#    client_id="myclient",
#) 
# def main():

# Create a connection object.  https://docs.streamlit.io/develop/tutorials/databases/private-gsheet
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

import plotly.graph_objects as go
def create_link(url:str) -> str:
    return f'''<a href="{url}">🔗</a>'''

with tab1: # repository
    st.dataframe(res, column_config={"Image": st.column_config.LinkColumn(display_text="Image here"),
                                     "Source": st.column_config.LinkColumn(display_text="Source")},
                    height=1000, column_order=columns)

with tab2: # contribute
# adding new data
    # st.header("Contribute")
    def update_google_sheet():
        # update google sheet
        data=pd.DataFrame([[source, pub, pap, jour, targetspecies, antigen, clone, con, hostspecies,
                            isotype, supplier, cat, rrid, concentration, testtissue,
                            testcelltype, testamount, testprep, amounttested, sep, samp, cost, image]],
            columns=["Source", "Publisher", "Paper", "Journal", 
                     "Target Species", "Antigen", "Clone", 
                    "Conjugate", "Host Species", "Isotype", "Supplier", 
                    "Catalougue #", "RRID", "Concentration", 
                    "Test Tissue", "Test Cell Type", "Test Amount", 
                    "Test Preparation", "Amount Tested (uL)",
                    "Seperation Index", "Samples/vial", "Cost/sample", "Image"])
        df_old = conn.read(worksheet="to-review")
        df_old = pd.concat([df_old, data])
        d = conn.update(worksheet="to-review",data=df_old)
        st.cache_data.clear()

    with st.expander("Option 1: Upload a CSV file for review with matching column names"):
        uploaded_file = st.file_uploader("Once you upload a file it will be automatically sent for review")
        if uploaded_file is not None:
            df_new = pd.read_csv(uploaded_file)
            df_old = conn.read(worksheet="to-review")
            df_old = pd.concat([df_old, df_new])
            d = conn.update(worksheet="to-review",data=df_old)
            st.cache_data.clear()

    with st.expander("Option 2: Fill out Form for review"):
        with st.form('Form1'):
            source = st.text_input("Source")
            pub = st.text_input("Publisher")
            pap = st.text_input("Paper")
            jour = st.text_input("Journal")
            targetspecies = st.text_input("Target Species")
            antigen = st.text_input("Antigen")
            clone = st.text_input("Clone")
            con = st.text_input("Conjugate")
            hostspecies = st.text_input("Host Species")
            isotype = st.text_input("Isotype")
            supplier = st.text_input("Supplier")
            cat = st.text_input("Catalougue #")
            rrid = st.text_input("RRID")
            concentration = st.text_input("Concentration")
            testtissue = st.text_input("Test Tissue")
            testcelltype = st.text_input("Test Cell Type")
            testamount = st.text_input("Test Amount")
            testprep = st.text_input("Test Preparation")
            amounttested = st.text_input("Amount Tested (uL)")
            sep = st.text_input("Seperation Index")
            samp = st.text_input("Samples/vial")
            cost = st.text_input("Cost/sample")
            image = st.text_input("Image")
            st.form_submit_button('Add for review into Repository: for now this needs to be clicked twice to work', on_click=update_google_sheet)


    with st.expander("Option 3: Connect over email"):
        st.write("fcat.repository@gmail.com")

with tab3: # insights 
    # maybe plot comparison to overall data? In percentages?
    st.write("Plot data comming from " + str(len(res["Source"].unique())) + " data sources.")
    fig = px.bar(res["Antigen"].value_counts()[:20])
    st.plotly_chart(fig, use_container_width=True)
    fig = px.bar(res["Conjugate"].value_counts()[:20])
    st.plotly_chart(fig, use_container_width=True)
    fig = px.bar(res["Clone"].value_counts()[:20])
    st.plotly_chart(fig, use_container_width=True)
    fig = px.bar(res["Supplier"].value_counts()[:20])
    st.plotly_chart(fig, use_container_width=True)
    fig = px.bar(res["Concentration"].value_counts()[:20])
    st.plotly_chart(fig, use_container_width=True)

# with tab4: # FAQ
#     st.write("WIP")

with tab5: # Contact
    st.write("submitting this form doesn't do anything yet FYI")
    with st.form("form2", clear_on_submit=True):
        name = st.text_input("Enter name")
        email = st.text_input("Enter email")
        message = st.text_area("Enter message")
        submit = st.form_submit_button("Submit")
    st.write("Or send email to: fcat.repository@gmail.com (can add file attachments this way)")

with tab6: # Pricing
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


# if keycloak.authenticated:
#     main()