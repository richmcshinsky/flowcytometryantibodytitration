import streamlit as st
import pandas as pd
import streamlit_pandas as sp
from streamlit_gsheets import GSheetsConnection
# from streamlit_keycloak import login # https://github.com/bleumink/streamlit-keycloak

# TODO: make a google private sheet for CRUD operations
# TODO: make 2 sheets, one for data and one for review
# TODO: add styling/theming
# TODO: 

# set up config for page
st.set_page_config(
    page_title='Flow Cytometry Antibody Titration Repository',
    layout="wide",
    initial_sidebar_state="expanded"
)

tab1, tab2, tab3, tab4, tab5, tab6 = st.tabs(["Repository", "Contribute", "Insights", "FAQ", "Contact", "Pricing"])

# Removes download button on tables
st.markdown(
                """
                <style>
                [data-testid="stElementToolbar"] {
                    display: none;
                }
                </style>
                """,
                unsafe_allow_html=True
            )


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

# Add filters
create_data = { "Source":            "multiselect",
                "Target Species":    "multiselect",
                "Antigen":           "multiselect",
                "Clone":             "multiselect",
                "Conjugate":         "multiselect",
                "Host Species":      "multiselect",
                "Isotype":           "multiselect",
                "Supplier":          "multiselect",
                "Catalougue #":      "multiselect",
                "RRID":              "multiselect",
                "Concentration":     "multiselect",
                "Test Tissue":       "multiselect",
                "Test Cell Type":    "multiselect",
                "Test Amount":       "multiselect",
                "Test Preparation":  "multiselect",
                "Amount Tested (uL)":"text"}

all_widgets = sp.create_widgets(df, create_data)
res = sp.filter_df(df, all_widgets)

with tab1:
    # st.title("Demo")
    # st.header("Repository")
    st.write(res)

with tab2:
# adding new data
    # st.header("Contribute")
    def update_google_sheet():
        # update google sheet
        data=pd.DataFrame([[source, targetspecies, antigen, clone, con, hostspecies,
            isotype, supplier, cat, rrid, concentration, testtissue,
            testcelltype, testamount, testprep, amounttested]],
            columns=["Source", "Target Species", "Antigen", "Clone", 
                    "Conjugate", "Host Species", "Isotype", "Supplier", 
                    "Catalougue #", "RRID", "Concentration", 
                    "Test Tissue", "Test Cell Type", "Test Amount", 
                    "Test Preparation", "Amount Tested (uL)"])
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
            source = st.text_input("Source", key='label_input')
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
            st.form_submit_button('Add for review into Repository: for now this needs to be clicked twice to work', on_click=update_google_sheet)


    with st.expander("Option 3: Connect over email"):
        st.write("fcat.repository@gmail.com")

with tab3:
    st.bar_chart(res["Antigen"].value_counts())

with tab4:
    st.write("WIP")

with tab5:
    st.write("EMAIL: fcat.repository@gmail.com")

with tab6:
    st.write("WIP")


# if keycloak.authenticated:
#     main()