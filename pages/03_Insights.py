import streamlit as st
import plotly.express as px
from streamlit_gsheets import GSheetsConnection
from st_paywall import add_auth
from streamlit_dynamic_filters import DynamicFilters
import pandas as pd


st.set_page_config(page_title='Flow Cytometry Antibody Titration Repository', layout="wide")

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

@st.cache_data(show_spinner=False)
def load_data():
    conn = st.connection("gsheets", type=GSheetsConnection)
    df = conn.read(worksheet="testing", ttl="30m")
    df["Supplier"] = df["Supplier"].replace(["Biolegend", "BL"], "BioLegend")
    df["Supplier"] = df["Supplier"].replace(["BD Horizon", "BD pharmingen", "BD Biosciences", "BD Pharm",
                                                    "BD Pharmingen", "BD Special order reagent", "BD OptiBuild",
                                                    "BD", "BD custom antibody"], "BD Bioscience")
    df["Supplier"] = df["Supplier"].replace(["eBiosciences", "ebioscience", "eBioscinece"], "eBioscience")
    df["Supplier"] = df["Supplier"].replace(["Thermo Fisher Scientific", "ThermoFisher", "Thermo",
                                                    "ThermoFisher Scientific", "Thermofisher"], "Thermo Fisher")
    df["Supplier"] = df["Supplier"].replace(["Miltenyi Biotec", "BL"], "Miltenyi")
    df = normalize_antigens(df)
    return df #[columns]

def normalize_antigens(df):
    df_terms = pd.read_excel("data/CD alternative names.xlsx", names=["cd", "alternate"]).fillna("NULL")
    df_terms["alternate"] = ["NULL" if x == "-" else x for x in df_terms["alternate"]]
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


columns_simple = ["Antigen", "Clone", "Conjugate", "Conjugate Type", "Test Tissue", "Test Cell Type",
                  "Test Preparation", "Target Species", "Isotype", "Supplier",
                  "Concentration for this Lot# (ng/µL)", "Amount Tested (uL)",
                  "Optimal Amount (µL/100 µL)", "Seperation Index", "Samples/vial",
                  "Cost/sample ($USD)", "Metal Conjugate", "Staining", "Source"]

df = load_data()
df_filtered = DynamicFilters(df.astype(str).fillna(""), filters=columns_simple)
df_filtered.display_filters(location='columns', num_columns=3, gap='large')
res = df_filtered.filter_df()

st.write("Plot data from " + str(len(res["Source"].unique())) + " unique data sources.")

# # of tests at optimal dilution       for antigens
# price/test at optimal uL.            antigens
# reorder frequency at 10 tests/week (years) 

# fig = px.bar(res["Antigen"].value_counts(normalize=True)[:20])
# st.plotly_chart(fig, use_container_width=True)

st.write("Number of tests at optimal dilution comparison between suppliers")
res_p = res[["Source", "supplier link", "Antigen", "Supplier", "# of tests at optimal dilution", 
             "price/test at optimal uL", "reorder frequency at 10 tests/week (years)"]].dropna().drop_duplicates()
res_p = res_p[res_p["price/test at optimal uL"] != "nan"]
res_p = res_p[res_p["price/test at optimal uL"] != 0]
fig = px.strip(res_p, x="Supplier", y="# of tests at optimal dilution", color="Antigen")
st.plotly_chart(fig, use_container_width=True)

st.write("price/test at optimal uL comparison between suppliers")
fig = px.strip(res_p, x="Supplier", y="price/test at optimal uL")
st.plotly_chart(fig, use_container_width=True)

st.write("reorder frequency at 10 tests/week (years) comparison between suppliers")
fig = px.strip(res_p, x="Supplier", y="reorder frequency at 10 tests/week (years)")
st.plotly_chart(fig, use_container_width=True)

st.write(res_p)

add_auth(required=True)

