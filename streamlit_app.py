import streamlit as st
# from streamlit_keycloak import login # https://github.com/bleumink/streamlit-keycloak

# TODO: add page for purchase options (maybe affiliate link income?)
# TODO: add styling/theming
# TODO: contact form
# TODO: finish adding images 
# TODO: review data with Tony
# TODO: update contribute to only have essential columns as options

# TODO: I think we need a generic search box so someone can enter whatever is on their mind and see what we have to offer.
# TODO: In time, we will need a reference for any published data, DOI and/or PMCID may be sufficient.
st.set_page_config(
        page_title='Flow Cytometry Antibody Titration Repository',
        layout="wide",
        #initial_sidebar_state="expanded"
    )

def main():
    # builds the sidebar menu
    with st.sidebar:
        st.page_link('streamlit_app.py', label='Home')
        st.page_link('pages/01_Repository.py', label='Repository')
        st.page_link('pages/02_Contribute.py', label='Contribute')
        st.page_link('pages/03_Insights.py', label='Insights')
        st.page_link('pages/04_Contact.py', label='Contact')
        st.page_link('pages/05_Pricing.py', label='Pricing')
        st.page_link('pages/06_Purchase.py', label='Purchase')

    st.markdown("<h1 style='text-align: center; color: black;'>Metrdy</h1>", unsafe_allow_html=True)

    #st.title("Streamlit Keycloak example")
    #keycloak = login(
    #    url="http://localhost:8080",
    #    realm="myrealm",
    #    client_id="myclient",
    #) 
    # def main():
    st.subheader("Welcome")
    st.write("""This is a database of flow cytometry antibody titration data.
                You can look up titration data for planning experiments and making 
                informed purchasing decisions. Data is collected from various publications
                and through user contributions. """)
    # st.divider()
    st.subheader("What brings you here today?")
    #if st.button("Repository"):
    #    st.switch_page("pages/01_Repository.py")
    #if st.button("Contribute"):
    #    st.switch_page("pages/02_Contribute.py")
    #if st.button("Insights"):
    #    st.switch_page("pages/03_Insights.py")
    #if st.button("Contact"):
    #    st.switch_page("pages/04_Contact.py")
    #if st.button("Pricing"):
    #    st.switch_page("pages/05_Pricing.py")
    #if st.button("Purchase"):
    #    st.switch_page("pages/06_Purchase.py")
    # if keycloak.authenticated:
    #     main()
    
    col1, col2 = st.columns(2, gap="small")
    with col1:
        st.button(label="Repository", use_container_width=True, help="""Click here to go explore the repository data. 
                  Filters will appear in the same navigation tab on the left.""")
    with col2:
        st.button(label="Contribute", use_container_width=True, help="""Add to the repository usign your own data. 
                  Free subscriptions are offered for accepted contributions!""")
    with col1:
        st.button(label="Insights", use_container_width=True, help="See visualizations and summaries about repository data.")
    with col2:
        st.button(label="Contact", use_container_width=True, help="Form to send an email.")
    with col1:
        st.button(label="Pricing", use_container_width=True, help="Explanations on subscription pricing and benefits")
    with col2:
        st.button(label="Purchase", use_container_width=True, help="Use identifier to link directly to supplier purchase page.")

if __name__ == '__main__':
    main()