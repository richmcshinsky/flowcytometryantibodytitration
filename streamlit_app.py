import streamlit as st
import pandas as pd

# Page title
st.set_page_config(page_title='Flow Cytometry Antibody Titration Repositry')

#with st.expander('About this app'):
#  st.markdown('**What can this app do?**')
#  st.info('This app shows the use of Pandas for data wrangling, Altair for chart creation and editable dataframe for data interaction.')
#  st.markdown('**How to use the app?**')
#  st.warning('To engage with the app, 1. Select genres of your interest in the drop-down selection box and then 2. Select the year duration from the slider widget. As a result, this should generate an updated editable DataFrame and line plot.')
  


import streamlit as st
import pandas as pd
import streamlit_pandas as sp

@st.cache_data
def load_data():
    df = pd.read_excel(file)
    return df

file = "data/sample.xlsx"
df = load_data()

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

st.title("Demo")

st.header("Repository")
st.write(res)

st.header("Contribute")
uploaded_file = st.file_uploader("Upload a CSV file following instructions")
if uploaded_file is not None:
    df_new = pd.read_csv(uploaded_file)
    st.write(df_new)

