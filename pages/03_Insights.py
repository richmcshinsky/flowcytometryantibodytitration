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
    # st.page_link('pages/06_Purchase.py', label='Purchase')

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
    return df[columns]

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

columns = ["Antigen", "Clone", "Conjugate", "Conjugate Type", "Test Tissue", "Test Cell Type", 
           "Test Preparation", "Test Cell Count", "Image", "Target Species", "Host Species", "Isotype",
           "Supplier", "Catalougue #", "RRID", "Concentration for this Lot#", 
           "Optimal Concentration for this Lot#", "Concentration for this Lot# (ng/µL)", 
           "Amount Tested (uL)", "Amount Tested (ng)", "Optimal Amount (µL/100 µL)", "Seperation Index", 
           "Samples/vial", "Cost/sample ($USD)", "Metal Conjugate", "Metal Source", "Metal Catalogue #",
           "Detector", "Staining", "Source", "Publisher", "Paper", "Journal", 
           "supplier link", "supplier size", "supplier price", "supplier Host Species",
           "Supplier Isotype", "supplier Catalougue Concentration", "supplier RRID"]

columns_simple = ["Antigen", "Clone", "Conjugate", "Conjugate Type", "Test Tissue", "Test Cell Type",
                  "Test Preparation", "Target Species", "Isotype", "Supplier",
                  "Concentration for this Lot# (ng/µL)", "Amount Tested (uL)",
                  "Optimal Amount (µL/100 µL)", "Seperation Index", "Samples/vial",
                  "Cost/sample ($USD)", "Metal Conjugate", "Detector", "Staining", "Source"]

df = load_data()
df_filtered = DynamicFilters(df.astype(str).fillna(""), filters=columns_simple)
df_filtered.display_filters(location='columns', num_columns=3, gap='large')
res = df_filtered.filter_df()
st.write("Visualizations about repository data: Subsribe to see all insights!")

st.write("Plot data from " + str(len(res["Source"].unique())) + " unique data sources.")
fig = px.bar(res["Antigen"].value_counts(normalize=True)[:20])
st.plotly_chart(fig, use_container_width=True)

st.write("Price comparison between suppliers")
res_p = res[["Source", "Antigen", "Supplier", "supplier price"]].dropna().drop_duplicates()
res_p = res_p[res_p["supplier price"] != "nan"]
res_p["supplier price"] = [float(x.replace("€", "")) * 1.29 if "€" in x else x for x in res_p["supplier price"]]
fig = px.box(res_p, x="Supplier", y="supplier price")
st.plotly_chart(fig, use_container_width=True)
fig = px.scatter(res_p, x="Supplier", y="supplier price")
st.plotly_chart(fig, use_container_width=True)
fig = px.strip(res_p, x="Supplier", y="supplier price")
st.plotly_chart(fig, use_container_width=True)

add_auth(required=True)

# fig = px.bar(res["Conjugate"].value_counts(normalize=True)[:20])
# st.plotly_chart(fig, use_container_width=True)
# fig = px.bar(res["Clone"].value_counts(normalize=True)[:20])
# st.plotly_chart(fig, use_container_width=True)
# fig = px.bar(res["Supplier"].value_counts(normalize=True)[:20])
# st.plotly_chart(fig, use_container_width=True)
# fig = px.bar(res["Amount Tested (uL)"].value_counts(normalize=True))#[:20])
# st.plotly_chart(fig, use_container_width=True)

# if __name__ == '__main__':
#     main()
