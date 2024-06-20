import streamlit as st
import pandas as pd
from streamlit_gsheets import GSheetsConnection

def main():
    with st.sidebar:
            st.page_link('streamlit_app.py', label='Home')
            st.page_link('pages/01_Repository.py', label='Repository')
            st.page_link('pages/02_Contribute.py', label='Contribute')
            st.page_link('pages/03_Insights.py', label='Insights')
            st.page_link('pages/04_Contact.py', label='Contact')
            st.page_link('pages/05_Pricing.py', label='Pricing')
            st.page_link('pages/06_Purchase.py', label='Purchase')

    conn = st.connection("gsheets", type=GSheetsConnection)

    def update_google_sheet():
        # update google sheet
        data=pd.DataFrame([[source, pub, pap, jour, targetspecies, antigen, clone, con, hostspecies,
                            isotype, supplier, cat, rrid, concentration, testtissue,
                            testcelltype, testamount, testprep, amounttested, sep, samp, cost, image]],
            columns=["Source", "Publisher", "Paper", "Journal", 
                        "Target Species", "Antigen", "Clone", 
                    "Conjugate", "Host Species", "Isotype", "Supplier", 
                    "Catalougue #", "RRID", "Concentration", 
                    "Test Tissue", "Test Cell Type", "Test Amount", 
                    "Test Preparation", "Amount Tested (uL)",
                    "Seperation Index", "Samples/vial", "Cost/sample", "Image"])
        df_old = conn.read(worksheet="to-review")
        df_old = pd.concat([df_old, data])
        d = conn.update(worksheet="to-review",data=df_old)
        st.cache_data.clear()

    with st.expander("Option 1: Upload a CSV file for review with matching column names"):
        uploaded_file = st.file_uploader("Once you upload a file it will be automatically sent for review")
        if uploaded_file is not None:
            df_new = pd.read_csv(uploaded_file)
            df_old = conn.read(worksheet="to-review")
            df_old = pd.concat([df_old, df_new])
            d = conn.update(worksheet="to-review",data=df_old)
            st.cache_data.clear()

    with st.expander("Option 2: Fill out Form for review"):
        with st.form('Form1'):
            source = st.text_input("Source")
            pub = st.text_input("Publisher")
            pap = st.text_input("Paper")
            jour = st.text_input("Journal")
            targetspecies = st.text_input("Target Species")
            antigen = st.text_input("Antigen")
            clone = st.text_input("Clone")
            con = st.text_input("Conjugate")
            hostspecies = st.text_input("Host Species")
            isotype = st.text_input("Isotype")
            supplier = st.text_input("Supplier")
            cat = st.text_input("Catalougue #")
            rrid = st.text_input("RRID")
            concentration = st.text_input("Concentration")
            testtissue = st.text_input("Test Tissue")
            testcelltype = st.text_input("Test Cell Type")
            testamount = st.text_input("Test Amount")
            testprep = st.text_input("Test Preparation")
            amounttested = st.text_input("Amount Tested (uL)")
            sep = st.text_input("Seperation Index")
            samp = st.text_input("Samples/vial")
            cost = st.text_input("Cost/sample")
            image = st.text_input("Image")
            st.form_submit_button('Add for review into Repository: for now this needs to be clicked twice to work', on_click=update_google_sheet)


    with st.expander("Option 3: Connect over email"):
        st.write("fcat.repository@gmail.com")

if __name__ == '__main__':
    main()
