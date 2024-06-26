import streamlit as st
import streamlit_pandas as sp
from streamlit_gsheets import GSheetsConnection
from st_paywall import add_auth

st.set_page_config(page_title='Flow Cytometry Antibody Titration Repository', layout="wide")


st.markdown("""<style> [data-testid="stElementToolbar"] {display: none;} </style>""", unsafe_allow_html=True)
with st.sidebar:
        st.page_link('streamlit_app.py', label='Home')
        st.page_link('pages/01_Repository.py', label='Repository')
        st.page_link('pages/02_Contribute.py', label='Contribute')
        st.page_link('pages/03_Insights.py', label='Insights')
        st.page_link('pages/04_Contact.py', label='Contact')
        st.page_link('pages/05_Pricing.py', label='Pricing')
        st.page_link('pages/06_Purchase.py', label='Purchase')

st.markdown("<h1 style='text-align: center; color: black;'>Metrdy</h1>", unsafe_allow_html=True)
st.divider()
st.write("This repository data has several filtering and search options:")
lst = ['click on a column name to sort values', 
        'filter using the menu on the left', 
        'search using keywords by typing in the filter box on the left menu']
s = ''
for i in lst:
    s += "- " + i + "\n"
st.markdown(s)
st.write("Note: If you are on mobile, you may need to press and hold on links to allow popups.")

conn = st.connection("gsheets", type=GSheetsConnection)
df = conn.read(worksheet="testing", ttl="30m")

columns = ["Antigen", "Clone", "Conjugate", "Test Tissue",
        "Test Cell Type", "Test Preparation", "Test Amount",
        "Image", "Target Species", "Host Species", "Isotype",
        "Supplier", "Catalougue #", "RRID", "Concentration for this Lot#",
        "Optimal Concentration for this Lot#", "Concentration for this Lot# (ng/µL)",
        "Amount Tested (uL)", "Amount Tested (ng)", "Optimal Amount (µL)", 
        "Seperation Index", "Samples/vial",
        "Cost/sample ($USD)", "Metal", "Metal Source", "Metal Catalogue #",
        "Detector", "Staining", "Source", "Publisher", "Paper",
        "Journal"]

create_data = {}
for c in columns:
    create_data[c] = "multiselect"

# Add filters
df = df[columns]
all_widgets = sp.create_widgets(df, create_data)
res = sp.filter_df(df, all_widgets)

with st.expander("Shows example 10 rows from Repository: Subscribe to see full repository! (These rows wont filter FYI)"):
    st.dataframe(df.head(10), column_config={"Image": st.column_config.LinkColumn(display_text="Image here"),
                                    "Source": st.column_config.LinkColumn(display_text="Source")},
                    height=300, column_order=columns)

add_auth(required=True)
st.dataframe(res, column_config={"Image": st.column_config.LinkColumn(display_text="Image here"),
                                    "Source": st.column_config.LinkColumn(display_text="Source")},
                    height=1000, column_order=columns)


# st.session_state['res'] = res
    
#if __name__ == '__main__':
#   main()