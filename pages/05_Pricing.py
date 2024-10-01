import streamlit as st

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

with st.container():
    st.markdown("<h2 style='text-align: center; color: black;'>Repository benefits</h2>", unsafe_allow_html=True)
    st.image("data/repo benifits.png")

with st.container():
    total_diff_per_test = 54.61
    st.markdown("<h2 style='text-align: center; color: black;'>Example 1</h2>", unsafe_allow_html=True)
    st.write("""Using https://onlinelibrary.wiley.com/doi/10.1002/cyto.a.24545 as an example, there were 
             33 commercially purchased antibodies tested, 21 included in the final. 
             For the 21 in the final, summing the difference between supplier
             recommended and optimal dilution pricing per test, the total is :blue[$54.61/test].
             Note that this is the raw price difference on amounts and doesn't take into account
             other miscellanous expenses. """)
    
with st.container():
    total_diff_per_test = 54.61
    st.markdown("<h2 style='text-align: center; color: black;'>Example 2</h2>", unsafe_allow_html=True)
    st.write("""For common cases, ordering appopriate amounts antibodies can draw from personal
             experience. But for uncommon situations, this can make a significant difference. For example,
             antigen CD56 with conjugate BUV737, at optimal dilution, the savings on the difference
             is :blue[$8.20/test].""")
    st.write("""Or for one CD3 FITC, the sulpier recommended tests is 100, or 0.5 mL, but at the optimal
             dilution of 0.03, would result in over :blue[16,000] tests for the single vial, or $0.0096/test""")

with st.container():
    st.markdown("<h2 style='text-align: center; color: black;'>Subscription benefits</h2>", unsafe_allow_html=True)
    st.image("data/sub benifits.png")

with st.container():
    st.markdown("<h2 style='text-align: center; color: black;'>Pricing</h2>", unsafe_allow_html=True)
    st.image("data/pricing.png")
