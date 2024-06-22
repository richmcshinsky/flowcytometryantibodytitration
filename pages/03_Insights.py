import streamlit as st
import plotly.express as px
import streamlit_pandas as sp
from streamlit_gsheets import GSheetsConnection
from st_paywall import add_auth


st.set_page_config(page_title='Flow Cytometry Antibody Titration Repository', layout="wide")

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

st.write("Plot data from " + str(len(res["Source"].unique())) + " unique data sources.")
fig = px.bar(res["Antigen"].value_counts()[:20])
st.plotly_chart(fig, use_container_width=True)

add_auth(required=True)

fig = px.bar(res["Conjugate"].value_counts()[:20])
st.plotly_chart(fig, use_container_width=True)
fig = px.bar(res["Clone"].value_counts()[:20])
st.plotly_chart(fig, use_container_width=True)
fig = px.bar(res["Supplier"].value_counts()[:20])
st.plotly_chart(fig, use_container_width=True)
fig = px.bar(res["Concentration"].value_counts()[:20])
st.plotly_chart(fig, use_container_width=True)

# if __name__ == '__main__':
#     main()
