import streamlit as st
from streamlit_gsheets import GSheetsConnection
from streamlit_dynamic_filters import DynamicFilters

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

def step_1():
    st.title("Step 1: Snowflake Credentials")
    username = st.text_input("Username")
    password = st.text_input("Password", type="password")
    account = st.text_input("Account")
    warehouse = st.text_input("Warehouse")
    
    return username, password, account, warehouse

def step_2():
    st.title("Step 2: Table Details")
    schema = st.text_input("Schema")
    table = st.text_input("Table Name")
    
    return schema, table

def step_3():
    st.title("Step 3: Upload CSV")
    csv_file = st.file_uploader("Choose a CSV file")

columns = ["Antigen", "Clone", "Conjugate", "Conjugate Type", "Test Tissue", "Test Cell Type", 
           "Test Preparation", "Test Cell Count", "Image", "Target Species", "Host Species", "Isotype",
           "Supplier", "Catalougue #", "RRID", "Concentration for this Lot#", 
           "Optimal Concentration for this Lot#", "Concentration for this Lot# (ng/µL)", 
           "Amount Tested (uL)", "Amount Tested (ng)", "Optimal Amount (µL/100 µL)", "Seperation Index", 
           "Samples/vial", "Cost/sample ($USD)", "Metal Conjugate", "Metal Source", "Metal Catalogue #",
           "Detector", "Staining", "Source", "Publisher", "Paper", "Journal", 
           "supplier link", "supplier size", "supplier price", "supplier Host Species",
           "Supplier Isotype", "supplier Catalougue Concentration", "supplier RRID"]

st.write("What protocol do you plan to run?")

current_step = st.selectbox("Step", ["Step 1", "Step 2", "Step 3"])
    
if current_step == "Step 1":
    username, password, account, warehouse = step_1()        

elif current_step == "Step 2":
    schema, table = step_2()
    
elif current_step == "Step 3":
    csv_file = step_3()
    next_step_button = st.sidebar.button("Submit")

"""df = load_data()

con_type, ants_choice, cons_choice, clos_choice = None, None, None, None
col1, col2 = st.columns(2, gap="small")
with col1:
    if st.button(label="Flow Cytometry", use_container_width=True):
        con_type = "Fluorescent"
        # move to next step on new page or something?
with col2:
    if st.button(label="Mass Cytometry", use_container_width=True):
        con_type = "Metal"
        # move to next step on new page or something?

# select antigen 
ants = df[df["Conjugate Type"] == con_type]['Antigen'].drop_duplicates()
ants_choice = st.selectbox("Select your target antigen", options=ants, index=None)

# select conjugate or clone
col1, col2 = st.columns(2, gap="small")
with col1:
    if st.button(label="Conjugate", use_container_width=True):
        cons = df[(df["Conjugate Type"] == con_type) & (df["Antigen"] == ants_choice)]['Conjugate'].drop_duplicates()
        cons_choice = st.selectbox("Select your target conjugate", options=cons, index=None)
        # move to next step on new page or something?
with col2:
    if st.button(label="Clone", use_container_width=True):
        clos = df[(df["Conjugate Type"] == con_type) & (df["Antigen"] == ants_choice)]['Clone'].drop_duplicates()
        clos_choice = st.selectbox("Select your target clone", options=clos, index=None)
            # move to next step on new page or something?

st.write(con_type)
st.write(ants_choice)
st.write(cons_choice)

if cons_choice:
    df = df[(df["Conjugate Type"] == con_type) & (df["Antigen"] == ants_choice) & (df["Conjugate"] == cons_choice)]
elif clos_choice:
    df = df[(df["Conjugate Type"] == con_type) & (df["Antigen"] == ants_choice) & (df["Clone"] == clos_choice)]
# show graph of cost/sample and graph of separation index by other (fluorophore or clone)​

# show data
st.divider()
st.write(df.head())"""
