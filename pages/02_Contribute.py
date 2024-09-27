import streamlit as st
import pandas as pd
from streamlit_gsheets import GSheetsConnection

st.set_page_config(page_title='Flow Cytometry Antibody Titration Repository', layout="wide")

@st.cache_data
def convert_df(df):
    # IMPORTANT: Cache the conversion to prevent computation on every rerun
    return df.to_csv().encode("utf-8")

def main():
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
    st.write("""If you found this repository useful, it would greatly benefit everyone using it with any contirbutions you can make. 
             By adding a successful contribution to the repository, you will recieve a free subscription for x months.""")

    conn = st.connection("gsheets", type=GSheetsConnection)

    with st.expander("Option 1: Upload a CSV file for review with matching column names"):
        st.write("""Download template file below to have columns 
                 appropriately structured, otherwise upload with fail.
                 Essential columns will be in red, the others are nice to have.""")
        csv = convert_df(pd.read_csv("data/template.csv"))
        st.download_button(label="Download template as CSV", data=csv,
                           file_name="template.csv", mime="text/csv")
        uploaded_file = st.file_uploader("Once you upload a file it will be automatically sent for review")
        if uploaded_file is not None:
            try:
                df_new = pd.read_csv(uploaded_file)
                df_old = conn.read(worksheet="to-review")
                df_old = pd.concat([df_old, df_new])
                d = conn.update(worksheet="to-review",data=df_old)
                st.cache_data.clear()
            except:
                st.error("File failed to upload, try. again or send over email.")

    with st.expander("Option 2: Connect over email"):
        st.write("fcat.repository@gmail.com")

if __name__ == '__main__':
    main()
