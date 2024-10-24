import streamlit as st
from streamlit_gsheets import GSheetsConnection
import pandas as pd
import plotly.express as px
from st_paywall import add_auth

st.set_page_config(page_title='Metrdy', layout="wide")

with st.sidebar:
    st.page_link('streamlit_app.py', label='Home')
    st.page_link('pages/03_Discover.py', label='Discover')          # tool: see pricing comparisons and other figures
    st.page_link('pages/04_Create.py', label='Create')             # tool: to generate plots
    st.page_link('pages/05_Plan.py', label='Plan')                 # tool: guided walkthrough 
    st.page_link('pages/06_Pricing.py', label='Pricing')     
    st.page_link('pages/02_Contribute.py', label='Contribute') 

#st.markdown("<h1 style='text-align: center; color: black;'>Metrdy</h1>", unsafe_allow_html=True)
col1, col2, col3 = st.columns([2,3,2], gap="small")
with col2:
    st.image("data/logoex.png")
st.divider()


@st.cache_data(show_spinner=False)
def load_data():
    conn = st.connection("gsheets", type=GSheetsConnection)
    df = conn.read(worksheet="database", ttl="30m")
    df["Supplier"] = df["Supplier"].replace(["Biolegend", "BL"], "BioLegend")
    df["Supplier"] = df["Supplier"].replace(["BD Horizon", "BD pharmingen", "BD Biosciences", "BD Pharm",
                                                    "BD Pharmingen", "BD Special order reagent", "BD OptiBuild",
                                                    "BD", "BD custom antibody"], "BD Bioscience")
    df["Supplier"] = df["Supplier"].replace(["eBiosciences", "ebioscience", "eBioscinece"], "eBioscience")
    df["Supplier"] = df["Supplier"].replace(["Thermo Fisher Scientific", "ThermoFisher", "Thermo",
                                                    "ThermoFisher Scientific", "Thermofisher"], "Thermo Fisher")
    df["Supplier"] = df["Supplier"].replace(["Miltenyi Biotec", "BL"], "Miltenyi")
    df = normalize_antigens(df)
    return df[columns_simple]

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

columns_simple = ["Antigen", "Clone", "Conjugate", "Conjugate Type", "Supplier", "Amount Tested (uL)", 
               "Amount Tested (ng)", "Optimal Amount (µL/100 µL)", "Seperation Index", "Samples/vial", 
               "Cost/sample ($USD)", "supplier price", "Source", "supplier link", "supplier # tests",
               "# of tests at optimal dilution", "price/test at optimal uL", "reorder frequency at 10 tests/week"]

if "step" not in st.session_state:
    st.session_state["step"] = "Step 1"
    st.experimental_rerun()

elif st.session_state["step"] == "Step 1":
    st.write("Step 1: What protocol do you plan to run?")
    col1, col2 = st.columns(2, gap="small")
    with col1:
        if st.button(label="Flow Cytometry", use_container_width=True):
            st.session_state["con_type"] = "fluorescent"
            st.session_state["step"] = "Step 2"
            st.experimental_rerun()
    with col2:
        if st.button(label="Mass Cytometry", use_container_width=True):
            st.session_state["con_type"] = "Metal"
            st.session_state["step"] = "Step 2"
            st.experimental_rerun()

elif st.session_state["step"] == "Step 2":
    st.write("Step 2: Select target antigen")
    st.session_state["df"] = load_data()
    ants = st.session_state["df"][st.session_state["df"]["Conjugate Type"] == st.session_state["con_type"]]['Antigen'].drop_duplicates()
    ants_choice = st.selectbox("Select your target antigen", options=ants, index=None)

    if st.button(label="Next", type="primary"):
        st.session_state["ants_choice"] = ants_choice
        st.session_state["step"] = "Step 3"
        st.experimental_rerun()

    st.divider()
    col1, col2 = st.columns(2, gap="small")
    with col1:
        if st.button(label="Back", use_container_width=True):
                st.session_state["step"] = "Step 1"
                st.experimental_rerun()
    with col2:
        if st.button(label="Reset", use_container_width=True):
                st.session_state["step"] = "Step 1"
                st.experimental_rerun()

elif st.session_state["step"] == "Step 3":
    st.write("Step 3: Fluorophore (Conjugate) or Clone?")
    col1, col2 = st.columns(2, gap="small")
    with col1:
        if st.button(label="Fluorophore (Conjugate)", use_container_width=True):
            st.session_state["choice"] = "Conjugate"
            st.session_state["step"] = "Step 4"
            st.experimental_rerun()
    with col2:
        if st.button(label="Clone", use_container_width=True):
            st.session_state["choice"] = "Clone"
            st.session_state["step"] = "Step 4"
            st.experimental_rerun()
    
    st.divider()
    col1, col2 = st.columns(2, gap="small")
    with col1:
        if st.button(label="Back", use_container_width=True):
                st.session_state["step"] = "Step 2"
                st.experimental_rerun()
    with col2:
        if st.button(label="Reset", use_container_width=True):
                st.session_state["step"] = "Step 1"
                st.experimental_rerun()
    
elif st.session_state["step"] == "Step 4":
    if st.session_state["choice"] == "Conjugate":
        st.write("Step 4: Select target Fluorophore")
        cons = st.session_state["df"][(st.session_state["df"]["Conjugate Type"] == st.session_state["con_type"]) & (st.session_state["df"]["Antigen"] == st.session_state["ants_choice"])]['Conjugate'].drop_duplicates()
        res = st.selectbox("Select your target fluorophore", options=cons, index=None)
        if st.button(label="Next", type="primary"):
            st.session_state["target"] = res
            st.session_state["step"] = "Step 5"
            st.experimental_rerun()
    elif st.session_state["choice"] == "Clone":
        st.write("Step 4: Select target Clone")
        clos = st.session_state["df"][(st.session_state["df"]["Conjugate Type"] == st.session_state["con_type"]) & (st.session_state["df"]["Antigen"] == st.session_state["ants_choice"])]['Clone'].drop_duplicates()
        res = st.selectbox("Select your target clone", options=clos, index=None)
        if st.button(label="Next", type="primary"):
            st.session_state["target"] = res
            st.session_state["step"] = "Step 5"
            st.experimental_rerun()
    
    st.divider()
    col1, col2 = st.columns(2, gap="small")
    with col1:
        if st.button(label="Back", use_container_width=True):
                st.session_state["step"] = "Step 3"
                st.experimental_rerun()
    with col2:
        if st.button(label="Reset", use_container_width=True):
                st.session_state["step"] = "Step 1"
                st.experimental_rerun()

elif st.session_state["step"] == "Step 5":
    df = st.session_state["df"]
    if st.session_state["choice"] == "Conjugate":
        df_g = df[(df["Conjugate Type"] == st.session_state["con_type"]) & 
                    (df["Antigen"] == st.session_state["ants_choice"]) & 
                    (df["Conjugate"] == st.session_state["target"])]
    elif st.session_state["choice"] == "Clone":
        df_g = df[(df["Conjugate Type"] == st.session_state["con_type"]) & 
                    (df["Antigen"] == st.session_state["ants_choice"]) & 
                    (df["Clone"] == st.session_state["target"])]
    
    # show graph of cost/sample and graph of separation index by other (fluorophore or clone)
    st.write("""If the plots are empty, it's becuase there wasn't good pricing data to show. Please see table at bottom for 
             data contained in the repository""")
    
    # add_auth(required=True)
    
    col1, col2, col3 = st.columns(3, gap="small")
    with col1:
        st.radio( "Plot dot size", ["S", "M", "L"], horizontal=True, key="size", index=1)
    with col2:
        st.radio( "Plot hover text size", ["S", "M", "L"], horizontal=True, key="hover", index=1)
    with col3:
        st.radio( "Plot legend choice", ["Antigen", "Clone", "Conjugate"], horizontal=True, key="legend", index=0)

    if "size" not in st.session_state:
        st.session_state.size = 10
    if st.session_state.size == "S":
        size = 5
    elif st.session_state.size == "M":
        size = 10
    elif st.session_state.size == "L":
        size = 15

    if "hover" not in st.session_state:
        st.session_state.hover = 18
    if st.session_state.hover == "S":
        hover = 12
    elif st.session_state.hover == "M":
        hover = 18
    elif st.session_state.hover == "L":
        hover = 24

    if "legend" not in st.session_state:
        st.session_state.legend = "Antigen"

    st.markdown("<h4 style='text-align: center; color: black;'>Number of tests at optimal dilution comparison between suppliers</h4>", unsafe_allow_html=True)
    fig1 = px.strip(df_g, x="Supplier", y="# of tests at optimal dilution", color=st.session_state.legend, 
                hover_data=["# of tests at optimal dilution", "price/test at optimal uL", "reorder frequency at 10 tests/week"])
    fig1.update_traces({'marker':{'size': size}}) 
    fig1.update_layout(hoverlabel=dict(font=dict(size=hover)))
    st.plotly_chart(fig1, use_container_width=True)

    st.markdown("<h4 style='text-align: center; color: black;'>price/test at optimal uL comparison between suppliers</h4>", unsafe_allow_html=True)
    fig = px.strip(df_g, x="Supplier", y="price/test at optimal uL", color=st.session_state.legend,
                hover_data=["# of tests at optimal dilution", "price/test at optimal uL", "reorder frequency at 10 tests/week"])
    fig.update_traces({'marker':{'size': size}})
    fig.update_layout(hoverlabel=dict(font=dict(size=hover)))
    st.plotly_chart(fig, use_container_width=True)

    st.markdown("<h4 style='text-align: center; color: black;'>reorder frequency at 10 tests/week comparison between suppliers</h4>", unsafe_allow_html=True)
    fig = px.strip(df_g, x="Supplier", y="reorder frequency at 10 tests/week", color=st.session_state.legend,
                hover_data=["# of tests at optimal dilution", "price/test at optimal uL", "reorder frequency at 10 tests/week"])
    fig.update_traces({'marker':{'size': size}})
    fig.update_layout(hoverlabel=dict(font=dict(size=hover)))
    st.plotly_chart(fig, use_container_width=True)

    st.dataframe(data=df_g[["Source", "supplier link", "Antigen", "Supplier", "# of tests at optimal dilution", 
                "price/test at optimal uL", "reorder frequency at 10 tests/week"]], use_container_width=True, 
                column_config={"Source": st.column_config.LinkColumn(display_text="Source"),
                                "supplier link": st.column_config.LinkColumn(display_text="Supplier Link")})
    
    st.divider()
    col1, col2 = st.columns(2, gap="small")
    with col1:
        if st.button(label="Back", use_container_width=True):
                st.session_state["step"] = "Step 4"
                st.experimental_rerun()
    with col2:
        if st.button(label="Reset", use_container_width=True):
                st.session_state["step"] = "Step 1"
                st.experimental_rerun()





