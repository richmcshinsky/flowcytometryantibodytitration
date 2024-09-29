import streamlit as st

# st.set_page_config(page_title='Flow Cytometry Antibody Titration Repository', layout="wide")

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

st.write("Repository benefits:")
st.image("data/repo benifits.png")
lst = ['Using optimal concentrations from repository data, see comparative pricing per test for same antibodies',
       'Order antibodies at optimal amounts, reducing waste from overordering and improving outcomes', 
       'No need to spend many hours looking through previous research papers and doing pricing calculations just for one antibody',
       'New researchers can take advantage of the wealth of experience and knowledge to avoid common errors',
       'See sourcing to validate results and images of titrations to explore alternative concentrations']
s = ''
for i in lst:
    s += "- " + i + "\n"
st.markdown(s)

st.write("Subscription benefits:")
lst = ['access to all repository data', 
       'access to insights charts for purchasing decision making']
s = ''
for i in lst:
    s += "- " + i + "\n"
st.markdown(s)

st.write("Pricing:")
lst = ["$xx/month for individual access", 
        "email about discounts for group and organizational level access",
        "free access for x months for contributing to repository",
        "freee access for x months for each bug/error found or recommendation to improve that gets implemented"]
s = ''
for i in lst:
    s += "- " + i + "\n"
st.markdown(s)


#if __name__ == '__main__':
#    main()