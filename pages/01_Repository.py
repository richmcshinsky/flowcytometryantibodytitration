import streamlit as st
# import streamlit_pandas as sp
import pandas as pd
from streamlit_gsheets import GSheetsConnection
from st_paywall import add_auth
from streamlit_dynamic_filters import DynamicFilters

st.set_page_config(page_title='Flow Cytometry Antibody Titration Repository', layout="wide")

@st.cache_data(show_spinner=False)
def split_frame(input_df, rows):
    df = [input_df.loc[i:i+rows-1,:] for i in range(0, len(input_df), rows)]
    return df

@st.cache_data(show_spinner=False)
def load_data():
    conn = st.connection("gsheets", type=GSheetsConnection)
    df = conn.read(worksheet="testing", ttl="30m")
    df = normalize_antigens(df)
    return df

def normalize_antigens(df):
    rename = []
    for a in df["Antigen"].fillna(""):
        new_a = a
        for cd, alts in zip(df_terms["cd"], df_terms["alternate"]):
            for alt in alts.split(","):
                if alt in a:
                    new_a = cd
                    break
            if new_a != a:
                break
        rename.append(new_a)
    df["Antigen"] = rename
    return df


st.markdown("""<style> [data-testid="stElementToolbar"] {display: none;} </style>""", unsafe_allow_html=True)
with st.sidebar:
        st.page_link('streamlit_app.py', label='Home')
        st.page_link('pages/01_Repository.py', label='Repository')
        st.page_link('pages/02_Contribute.py', label='Contribute')
        st.page_link('pages/03_Insights.py', label='Insights')
        st.page_link('pages/04_Contact.py', label='Contact')
        st.page_link('pages/05_Pricing.py', label='Pricing')
        st.page_link('pages/06_Guided.py', label='Guided')

st.markdown("<h1 style='text-align: center; color: black;'>Metrdy</h1>", unsafe_allow_html=True)
st.divider()
st.write("This repository data has several filtering and search options:")
lst = ['Select filters of interest below', 
       'Filters can be text searched by typing in the box',
       'You can click on a column name to sort values']
s = ''
for i in lst:
    s += "- " + i + "\n"
st.markdown(s)
st.write("Note: If you are on mobile, you may need to press and hold on links to allow popups.")

df_terms = pd.read_excel("data/CD alternative names.xlsx", names=["cd", "alternate"]).fillna("NULL")
df_terms["alternate"] = ["NULL" if x == "-" else x for x in df_terms["alternate"]]

columns_simple = ["Antigen", "Clone", "Conjugate", "Conjugate Type", "Test Tissue", "Test Cell Type",
                  "Test Preparation", "Target Species", "Isotype", "Supplier",
                  "Concentration for this Lot# (ng/µL)", "Amount Tested (uL)",
                  "Optimal Amount (µL/100 µL)", "Seperation Index", "Samples/vial",
                  "Cost/sample ($USD)", "Metal Conjugate", "Staining", "Source"]

with st.expander("Shows example 10 rows from Repository: Subscribe to see full repository! (These rows wont filter FYI)"):
    df = load_data()
    st.dataframe(df.head(10), column_config={"Image": st.column_config.LinkColumn(display_text="Image here"),
                                    "Source": st.column_config.LinkColumn(display_text="Source")},
                    height=300, column_order=columns_simple)

add_auth(required=True)

with st.expander("If you aren't able to find your target antigen, try an alternative name! Or add alternate names to your filter for more data."):
    search_target = st.text_input("Type in target antigen name for alternative names")
    if search_target:
        st.dataframe(df_terms[df_terms["cd"].str.contains(search_target, case=False) | df_terms["alternate"].str.contains(search_target, case=False)])

df = load_data()
df_filtered = DynamicFilters(df.astype(str).fillna(""), filters=columns_simple)
df_filtered.display_filters(location='columns', num_columns=3, gap='large')

pagination = st.container()
bottom_menu = st.columns((4, 1, 1))
with bottom_menu[2]:
    batch_size = st.selectbox("Page Size", options=[25, 50, 100])
with bottom_menu[1]:
    total_pages = (int(len(df_filtered.filter_df()) / batch_size) if int(len(df_filtered.filter_df()) / batch_size) > 0 else 1)
    current_page = st.number_input("Page", min_value=1, max_value=total_pages, step=1)
with bottom_menu[0]:
    st.markdown(f"Page **{current_page}** of **{total_pages}** ")

pages = split_frame(df_filtered.filter_df(), batch_size)
pagination.dataframe(data=pages[current_page - 1], use_container_width=True, 
                     column_config={"Image": st.column_config.LinkColumn(display_text="Image here"),
                     "Source": st.column_config.LinkColumn(display_text="Source"), 
                     "supplier link": st.column_config.LinkColumn(display_text="Supplier Link")},
                     height=900, column_order=columns_simple)

#if __name__ == '__main__':
#   main()