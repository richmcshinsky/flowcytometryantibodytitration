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
    st.markdown("<h2 style='text-align: center; color: black;'>Examples</h2>", unsafe_allow_html=True)
    st.write("""Using https://onlinelibrary.wiley.com/doi/10.1002/cyto.a.24545 as an example, there were 
             33 commercially purchased antibodies tested, 21 included in the final. 
             For the 21 in the final, summing the difference between supplier
             recommended and optimal dilution pricing per test, the total savings would be :blue[$54.61/test].""")
    st.write(""""We aimed to test 192 samples per experiment, which translates to approximately \$42,000 of reagent costs 
             (average cost of ∼\$2.5/reagent/sample) for three 28-color panels." 
             (https://www.cell.com/cell-reports-methods/fulltext/S2667-2375(23)00283-7). 
             Although antibodies may seem cheap, they add up fast and can have a dramatic overall savings. Even a 20% reduction here would have 
             reduced costs by :blue[$8,400] for the one paper.""")
    st.write("""For common cases, ordering appopriate amounts antibodies can draw from personal
             experience. But for uncommon situations, this can make a significant difference. For example,
             antigen CD56 with conjugate BUV737, at optimal dilution, the savings on the difference
             is :blue[$8.20/test].""")
    st.write("""Or for one CD3 FITC, the sulpier recommended tests is 100, or 0.5 mL, but at the optimal
             dilution of 0.03, would result in over :blue[16,000] tests for the single vial, or $0.0096/test""")
    st.write("""Or for antigen IL-21R and conjugate BV421, the optimal concentration is 10. Given the 
             supplier number of tests at 25, the price difference from the supplier's recommened to 
             optimal dilution is $-8.6, demonstrating that ording the vial in what one would normally do
             would likely result in underording enough antigen, resulting in either :blue[delayed] experiments
             or :blue[poor quality] data.""")
    st.write("""A major savings in cost comes from employee time spent in optimizing or having to redo an expirement because
             and antibody failed due to a bad dilution. Traditionally, purchasing amounts have been done by a history kept at the lab,
             what someone did before that worked, or hours and hours of research. Assuming a lab manager salary of 
             \$90,000/year or \$45/hour, not including benefits, then for every 8 hours spent reading published papers, optimizing, 
             reording, or other complications would correlate to :blue[$360/day] not counting material cost as well. 
             Assuming that the employee knows where to look and knows what to do.""")

with st.container():
    st.markdown("<h2 style='text-align: center; color: black;'>Subscription benefits</h2>", unsafe_allow_html=True)
    st.image("data/sub benifits.png")

with st.container():
    st.markdown("<h2 style='text-align: center; color: black;'>Pricing</h2>", unsafe_allow_html=True)
    st.image("data/pricing.png")
