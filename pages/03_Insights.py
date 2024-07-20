import streamlit as st
import plotly.express as px
import streamlit_pandas as sp
from streamlit_gsheets import GSheetsConnection
from st_paywall import add_auth
from streamlit_dynamic_filters import DynamicFilters


st.set_page_config(page_title='Flow Cytometry Antibody Titration Repository', layout="wide")

with st.sidebar:
    st.page_link('streamlit_app.py', label='Home')
    st.page_link('pages/01_Repository.py', label='Repository')
    st.page_link('pages/02_Contribute.py', label='Contribute')
    st.page_link('pages/03_Insights.py', label='Insights')
    st.page_link('pages/04_Contact.py', label='Contact')
    st.page_link('pages/05_Pricing.py', label='Pricing')
    # st.page_link('pages/06_Purchase.py', label='Purchase')

st.markdown("<h1 style='text-align: center; color: black;'>Metrdy</h1>", unsafe_allow_html=True)
st.divider()

# @st.cache_data(show_spinner=False)
def load_data():
    conn = st.connection("gsheets", type=GSheetsConnection)
    df = conn.read(worksheet="testing", ttl="30m")
    return df[columns]

columns = ["Antigen", "Clone", "Conjugate", "Conjugate Type", "Test Tissue", "Test Cell Type", 
           "Test Preparation", "Test Cell Count", "Image", "Target Species", "Host Species", "Isotype",
           "Supplier", "Catalougue #", "RRID", "Concentration for this Lot#", 
           "Optimal Concentration for this Lot#", "Concentration for this Lot# (ng/µL)", 
           "Amount Tested (uL)", "Amount Tested (ng)", "Optimal Amount (µL/100 µL)", "Seperation Index", 
           "Samples/vial", "Cost/sample ($USD)", "Metal Conjugate", "Metal Source", "Metal Catalogue #",
           "Detector", "Staining", "Source", "Publisher", "Paper", "Journal", 
           "supplier link", "supplier size", "supplier price", "supplier Host Species",
           "Supplier Isotype", "supplier Catalougue Concentration", "supplier RRID"]


df = load_data()
df_filtered = DynamicFilters(df.astype(str).fillna(""), filters=columns)
df_filtered.display_filters(location='columns', num_columns=3, gap='large')
res = df_filtered.filter_df()
st.write("Visualizations about repository data: Subsribe to see all insights!")

st.write("Plot data from " + str(len(res["Source"].unique())) + " unique data sources.")
fig = px.bar(res["Antigen"].value_counts(normalize=True)[:20])
st.plotly_chart(fig, use_container_width=True)

st.write("Price comparison between suppliers")
fig = px.bar(res["supplier price"].value_counts(normalize=True)[:20]) #, color="Supplier")
st.plotly_chart(fig, use_container_width=True)

add_auth(required=True)

fig = px.bar(res["Conjugate"].value_counts(normalize=True)[:20])
st.plotly_chart(fig, use_container_width=True)
fig = px.bar(res["Clone"].value_counts(normalize=True)[:20])
st.plotly_chart(fig, use_container_width=True)
fig = px.bar(res["Supplier"].value_counts(normalize=True)[:20])
st.plotly_chart(fig, use_container_width=True)
fig = px.bar(res["Amount Tested (uL)"].value_counts(normalize=True))#[:20])
st.plotly_chart(fig, use_container_width=True)

# if __name__ == '__main__':
#     main()
