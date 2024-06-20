import streamlit as st

def main():
    with st.sidebar:
            st.page_link('streamlit_app.py', label='Home')
            st.page_link('pages/01_Repository.py', label='Repository')
            st.page_link('pages/02_Contribute.py', label='Contribute')
            st.page_link('pages/03_Insights.py', label='Insights')
            st.page_link('pages/04_Contact.py', label='Contact')
            st.page_link('pages/05_Pricing.py', label='Pricing')

    st.markdown("<h1 style='text-align: center; color: black;'>Metrdy</h1>", unsafe_allow_html=True)

    st.dataframe(st.session_state['res'], column_config={"Image": st.column_config.LinkColumn(display_text="Image here"),
                                        "Source": st.column_config.LinkColumn(display_text="Source")},
                        height=1000, column_order=st.session_state['columns'])
    
if __name__ == '__main__':
    main()