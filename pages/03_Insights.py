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
                  "Test Preparation", "Target Species"]

columns_df = ["Source", "supplier link", "Antigen", "Clone", "Conjugate", "Supplier", "# of tests at optimal dilution", 
             "price per test", "price/test at optimal uL", "reorder frequency at 10 tests/week (years)"]

st.write("""Welecome to the insights page! Figures are visable to everyone, but in order to see the underlying 
         data and links a valid subscription is needed.""")


df = load_data()
df_filtered = DynamicFilters(df.astype(str).fillna(""), filters=columns_simple)
df_filtered.display_filters(location='columns', num_columns=3, gap='large')
res = df_filtered.filter_df()

st.divider()

st.write("Plot data from " + str(len(res["Source"].unique())) + " unique data sources.")

# fig = px.bar(res["Antigen"].value_counts(normalize=True)[:20])
# st.plotly_chart(fig, use_container_width=True)

st.markdown("<h3 style='text-align: center; color: black;'>Number of tests at optimal dilution comparison between suppliers</h3>", unsafe_allow_html=True)
# st.write("Number of tests at optimal dilution comparison between suppliers")
res_p = res[columns_df].dropna().drop_duplicates()
res_p = res_p[res_p["price/test at optimal uL"] != "nan"]
res_p = res_p[res_p["price/test at optimal uL"] != 0]

fig = px.strip(res_p, x="Supplier", y="# of tests at optimal dilution", color="Antigen", 
               hover_data=["# of tests at optimal dilution", "price/test at optimal uL", "reorder frequency at 10 tests/week (years)"])
st.plotly_chart(fig, use_container_width=True)

avg_diff = (pd.to_numeric(res_p["price per test"]) - pd.to_numeric(res_p["price/test at optimal uL"])).mean()
st.write(pd.to_numeric(res_p["price per test"]) - pd.to_numeric(res_p["price/test at optimal uL"]))
st.write("""For the selected filters, on average the difference between the supplier recommended price per test 
         and the price per test at the optimal dilution is: $""" + str(avg_diff))

st.markdown("<h3 style='text-align: center; color: black;'>price/test at optimal uL comparison between suppliers</h3>", unsafe_allow_html=True)
fig = px.strip(res_p, x="Supplier", y="price/test at optimal uL", color="Clone")
st.plotly_chart(fig, use_container_width=True)

st.markdown("<h3 style='text-align: center; color: black;'>reorder frequency at 10 tests/week (years) comparison between suppliers</h3>", unsafe_allow_html=True)
fig = px.strip(res_p, x="Supplier", y="reorder frequency at 10 tests/week (years)", color="Conjugate")
st.plotly_chart(fig, use_container_width=True)

# st.dataframe(data=res_p, use_container_width=True, 
#             column_config={"Source": st.column_config.LinkColumn(display_text="Source"),
#                             "supplier link": st.column_config.LinkColumn(display_text="Supplier Link")})

add_auth(required=True)

@st.cache_data(show_spinner=False)
def split_frame(input_df, rows):
    df_temp = [input_df.iloc[i:i+rows-1,:] for i in range(0, len(input_df), rows)]
    return df_temp

pagination = st.container()
bottom_menu = st.columns((4, 1, 1))
with bottom_menu[2]:
    batch_size = st.selectbox("Page Size", options=[25, 50, 100])
with bottom_menu[1]:
    total_pages = (int(len(res) / batch_size) if int(len(res) / batch_size) > 0 else 1)
    current_page = st.number_input("Page", min_value=1, max_value=total_pages, step=1)
with bottom_menu[0]:
    st.markdown(f"Page **{current_page}** of **{total_pages}** ")

pages = split_frame(res, batch_size)
# st.write(res)
# pages = [res.loc[i:i+batch_size-1,:] for i in range(0, len(res), batch_size)]
# st.write(pages)
pagination.dataframe(data=pages[current_page - 1], use_container_width=True, 
                     column_config={"Image": st.column_config.LinkColumn(display_text="Image here"),
                     "Source": st.column_config.LinkColumn(display_text="Source"), 
                     "supplier link": st.column_config.LinkColumn(display_text="Supplier Link")},
                     height=900, column_order=columns_df)


