import streamlit as st
import pandas as pd
import streamlit_pandas as sp
from streamlit_gsheets import GSheetsConnection

# Page title
st.set_page_config(page_title='Flow Cytometry Antibody Titration Repositry')

#with st.expander('About this app'):
#  st.markdown('**What can this app do?**')
#  st.info('This app shows the use of Pandas for data wrangling, Altair for chart creation and editable dataframe for data interaction.')
#  st.markdown('**How to use the app?**')
#  st.warning('To engage with the app, 1. Select genres of your interest in the drop-down selection box and then 2. Select the year duration from the slider widget. As a result, this should generate an updated editable DataFrame and line plot.')

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

# Create a connection object.
conn = st.connection("gsheets", type=GSheetsConnection)
df = conn.read(ttl="30m")

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

# Visual Page
st.title("Demo")

st.header("Repository")
st.write(res)

st.header("Contribute")

def update_google_sheet():
    # update google sheet
    a = 1

with st.expander("Option 1: Fill out Form for review"):
    with st.form('Form1'):
        st.text_input("Source")
        st.text_input("Target Species")
        st.text_input("Antigen")
        st.text_input("Clone")
        st.text_input("Conjugate")
        st.text_input("Host Species")
        st.text_input("Isotype")
        st.text_input("Supplier")
        st.text_input("Catalougue #")
        st.text_input("RRID")
        st.text_input("Concentration")
        st.text_input("Test Tissue")
        st.text_input("Test Cell Type")
        st.text_input("Test Amount")
        st.text_input("Test Preparation")
        st.text_input("Amount Tested (uL)")
        st.form_submit_button('Add for review into Repository', on_click=update_google_sheet)

with st.expander("Option 2: Upload a CSV file for review with matching column names"):
    uploaded_file = st.file_uploader("Once you upload a file it will be automatically sent for review")
    if uploaded_file is not None:
        df_new = pd.read_csv(uploaded_file)
        st.write(df_new)
        # TODO: instead of write have it update the google sheet?

