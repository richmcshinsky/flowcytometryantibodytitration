import streamlit as st
import pandas as pd
from streamlit_gsheets import GSheetsConnection

st.set_page_config(page_title='Flow Cytometry Antibody Titration Repository', layout="wide")

@st.cache_data
def convert_df(df):
    # IMPORTANT: Cache the conversion to prevent computation on every rerun
    return df.to_csv().encode("utf-8")


# builds the sidebar menu
with st.sidebar:
    st.page_link('streamlit_app.py', label='Home')
    st.page_link('pages/01_Learn.py', label='Learn')               # educational materials, each to learn about titrations and how to's. Easy to add links to this tab from other parts of site
    st.page_link('pages/02_Contribute.py', label='Contribute')     # add data to repository
    st.page_link('pages/03_Discover.py', label='Compare')          # tool: see pricing comparisons and other figures
    st.page_link('pages/04_Create.py', label='Create')             # tool: to generate plots
    st.page_link('pages/05_Plan.py', label='Plan')                 # tool: guided walkthrough 
    st.page_link('pages/06_Pricing.py', label='Product Info')      # pricing, faq, contact

st.markdown("<h1 style='text-align: center; color: black;'>Metrdy</h1>", unsafe_allow_html=True)
st.divider()
st.write("""If you found this repository useful, it would greatly benefit everyone using it with any contirbutions you can make. 
            By adding a successful contribution to the repository, you will recieve a free subscription for x months.""")

conn = st.connection("gsheets", type=GSheetsConnection)

with st.expander("Option 1: Upload a CSV file for review with matching column names"):
    st.write("""Download template file below to have columns 
                appropriately structured, otherwise upload with fail.
                Make sure to put your contact information such as email into the first column in
                order to recieve free subcription time. Fill out what you can, if there are 
                non-relevant columns, skip them. The repository contains a wide variety of
                information from a variety of sources.""")
    csv = convert_df(pd.read_csv("data/template.csv"))
    st.download_button(label="Download template as CSV", data=csv, file_name="template.csv", mime="text/csv")
    uploaded_file = st.file_uploader("Once you upload a file it will be automatically sent for review")
    if uploaded_file is not None:
        try:
            df_new = pd.read_csv(uploaded_file)
            df_old = conn.read(worksheet="to-review")
            df_old = pd.concat([df_old, df_new])
            d = conn.update(worksheet="to-review",data=df_old)
            st.cache_data.clear()

            import os
            import smtplib
            from email.mime.text import MIMEText
            secret = os.getenv("SECRET")
            msg = MIMEText("Success on contribution, review added data and reply")
            msg['From'] = "fcat.repository@gmail.com"
            msg['To'] = "fcat.repository@gmail.com"
            msg['Subject'] = "Successful Contribution Added"

            server = smtplib.SMTP('smtp.gmail.com', 587)
            server.starttls()
            server.login(u, secret)
            server.sendmail("fcat.repository@gmail.com", "fcat.repository@gmail.com", msg.as_string())
            server.quit()
        except:
            st.error("File failed to upload, try. again or send over email.")

with st.expander("Option 2: Connect over email"):
    st.write("fcat.repository@gmail.com")

