import streamlit as st
from streamlit_gsheets import GSheetsConnection
import pandas as pd
import plotly.express as px

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
    return df[["Antigen", "Clone", "Conjugate", "Conjugate Type", "Supplier", "Amount Tested (uL)", 
               "Amount Tested (ng)", "Optimal Amount (µL/100 µL)", "Seperation Index", "Samples/vial", 
               "Cost/sample ($USD)", "supplier size", "supplier price"]]

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

def step_1():
    st.write("Step 1: What protocol do you plan to run?")
    con_type = None
    col1, col2 = st.columns(2, gap="small")
    with col1:
        if st.button(label="Flow Cytometry", use_container_width=True):
            con_type = "Fluorescent"
            # move to next step on new page or something?
    with col2:
        if st.button(label="Mass Cytometry", use_container_width=True):
            con_type = "Metal"
            # move to next step on new page or something?
    
    return con_type

def step_2(con_type):
    st.write("Step 2: Select target antigen")
    ants = df[df["Conjugate Type"] == con_type]['Antigen'].drop_duplicates()
    ants_choice = st.selectbox("Select your target antigen", options=ants, index=None)
    
    return ants_choice

def step_3():
    st.write("Step 3: Fluorophore or Clone?")
    choice = None
    col1, col2 = st.columns(2, gap="small")
    with col1:
        if st.button(label="Fluorophore", use_container_width=True):
            choice = "Conjugate"
            # move to next step on new page or something?
    with col2:
        if st.button(label="Clone", use_container_width=True):
            choice = "Clone"
    
    return choice

def step_4(con_type, ants_choice, choice):
    res = None
    if choice == "Conjugate":
        st.write("Step 4: Select target Fluorophore")
        cons = df[(df["Conjugate Type"] == con_type) & (df["Antigen"] == ants_choice)]['Conjugate'].drop_duplicates()
        res = st.selectbox("Select your target fluorophore", options=cons, index=None)
        return res
    elif choice == "Clone":
        st.write("Step 4: Select target Clone")
        clos = df[(df["Conjugate Type"] == con_type) & (df["Antigen"] == ants_choice)]['Clone'].drop_duplicates()
        res = st.selectbox("Select your target clone", options=clos, index=None)
        return res
    

df = load_data()

st.session_state["step"] = st.selectbox("Step", ["Step 1", "Step 2", "Step 3", "Step 4", "Step 5"])

if st.session_state["step"] == "Step 1":
    st.session_state["con_type"] = step_1()   

elif st.session_state["step"] == "Step 2":
    st.session_state["ants_choice"] = step_2(st.session_state["con_type"])

elif st.session_state["step"] == "Step 3":
    st.session_state["type"] = step_3()

elif st.session_state["step"] == "Step 4":
    st.session_state["choice"] = step_4(st.session_state["con_type"], st.session_state["ants_choice"], st.session_state["type"])

elif st.session_state["step"] == "Step 5":
    if st.session_state["type"] == "Conjugate":
        df_g = df[(df["Conjugate Type"] == st.session_state["con_type"]) & 
                    (df["Antigen"] == st.session_state["ants_choice"]) & 
                    (df["Conjugate"] == st.session_state["choice"])]
    elif st.session_state["type"] == "Clone":
        df_g = df[(df["Conjugate Type"] == st.session_state["con_type"]) & 
                    (df["Antigen"] == st.session_state["ants_choice"]) & 
                    (df["Clone"] == st.session_state["choice"])]
    
    # show graph of cost/sample and graph of separation index by other (fluorophore or clone)
    st.write("Price comparison between suppliers")
    res_p = df_g[["Source", "Antigen", "Supplier", "supplier price"]].dropna().drop_duplicates()
    res_p = res_p[res_p["supplier price"] != "nan"]
    res_p["supplier price"] = [float(x.replace("€", "")) * 1.29 if "€" in x else x for x in res_p["supplier price"]]
    res_p['supplier size'] = res_p['supplier size'].str.extract('(\d+)', expand=False)
    res_p["supplier price/size"] = res_p["supplier price"]/res_p["supplier size"]# supplier size

    fig = px.strip(res_p, x="Supplier", y="supplier price/size")
    st.plotly_chart(fig, use_container_width=True)

    st.write(res_p)

