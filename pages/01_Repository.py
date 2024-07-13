import streamlit as st
# import streamlit_pandas as sp
import pandas as pd
from streamlit_gsheets import GSheetsConnection
from st_paywall import add_auth
from streamlit_dynamic_filters import DynamicFilters

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

# st.write("If you aren't able to find your target antigen, try an alternative name! Or add alternate names to your filter for more data.")
search_target = st.text_input("If you aren't able to find your target antigen, try an alternative name! Or add alternate names to your filter for more data.")
if search_target:
    df_terms = pd.read_excel("data/CD alternative names.xlsx", names=["cd", "alternate"])
    st.dataframe(df_terms[df_terms["cd"].str.contains(search_target, case=False) | df_terms["alternate"].str.contains(search_target, case=False)])

columns = ["Antigen", "Clone", "Fluorescent Conjugate", "Test Tissue",
        "Test Cell Type", "Test Preparation", "Test Cell Count",
        "Image", "Target Species", "Host Species", "Isotype",
        "Supplier", "Catalougue #", "RRID", "Concentration for this Lot#",
        "Optimal Concentration for this Lot#", "Concentration for this Lot# (ng/µL)",
        "Amount Tested (uL)", "Amount Tested (ng)", "Optimal Amount (µL/100 µL)", 
        "Seperation Index", "Samples/vial",
        "Cost/sample ($USD)", "Metal Conjugate", "Metal Source", "Metal Catalogue #",
        "Detector", "Staining", "Source", "Publisher", "Paper",
        "Journal"]

# create_data = {}
# for c in columns:
#     create_data[c] = "multiselect"

# Add filters
df = df[columns]
# all_widgets = sp.create_widgets(df, create_data)
# res = sp.filter_df(df, all_widgets)

with st.expander("Shows example 10 rows from Repository: Subscribe to see full repository! (These rows wont filter FYI)"):
    st.dataframe(df.head(10), column_config={"Image": st.column_config.LinkColumn(display_text="Image here"),
                                    "Source": st.column_config.LinkColumn(display_text="Source")},
                    height=300, column_order=columns)

add_auth(required=True)
# st.dataframe(res, column_config={"Image": st.column_config.LinkColumn(display_text="Image here"),
#                                     "Source": st.column_config.LinkColumn(display_text="Source")},
#                     height=1000, column_order=columns)

df_filtered = DynamicFilters(df.astype(str).fillna(""), filters=columns)
df_filtered.display_filters(location='columns', num_columns=3, gap='large')
st.write(df_filtered)
df_filtered.display_df()

# st.session_state['res'] = res
    
#if __name__ == '__main__':
#   main()