import streamlit as st


st.markdown("<h1 style='text-align: center; color: black;'>Metrdy</h1>", unsafe_allow_html=True)

st.dataframe(st.session_state['res'], column_config={"Image": st.column_config.LinkColumn(display_text="Image here"),
                                     "Source": st.column_config.LinkColumn(display_text="Source")},
                    height=1000, column_order=st.session_state['columns'])