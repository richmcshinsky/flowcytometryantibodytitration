import streamlit as st

st.write("Subscription benefits:")
lst = ['access to the entire repository data', 
        'access to insights charts', 
        'tools to generate professional figures from your data']
s = ''
for i in lst:
    s += "- " + i + "\n"
st.markdown(s)
st.write("Pricing")
lst = ["$xx/month for individual access", 
        "email about discounts for group and organizational level access",
        "free access for x months for contributing to repository"]
s = ''
for i in lst:
    s += "- " + i + "\n"
st.markdown(s)