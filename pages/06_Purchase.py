import streamlit as st
from streamlit_gsheets import GSheetsConnection
import streamlit_pandas as sp

st.set_page_config(page_title='Flow Cytometry Antibody Titration Repository', layout="wide")

def main():
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

    st.write("""By typing in the Catalougue # from the repository in the filter on the left navigation,
             this will filter this table to links of interest. You can 
             compare between values on the multiselect. These links will 
             redirect you to the supplier purchase page. Note that not all
             suppliers have link and not all links may be working. This is 
             purely for convience from looking up the supplier information
             by yourself.""")
    
    conn = st.connection("gsheets", type=GSheetsConnection)
    df = conn.read(worksheet="purchase", ttl="30m")
    columns = ["Supplier","Catalougue #", "Link"]
    create_data = {}
    for c in columns:
        create_data[c] = "multiselect"
    # Add filters
    df = df[columns]
    all_widgets = sp.create_widgets(df, create_data)
    res = sp.filter_df(df, all_widgets)
    st.dataframe(res.drop_duplicates().reset_index(drop=True), 
                 column_config={"Link": st.column_config.LinkColumn(display_text="Link")})


if __name__ == '__main__':
    main()