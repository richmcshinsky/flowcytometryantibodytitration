import streamlit as st
import pandas as pd
import matplotlib.pyplot as plt
from matplotlib.backends.backend_agg import RendererAgg

st.set_page_config(page_title='Flow Cytometry Antibody Titration Repository', layout="wide")

# builds the sidebar menu
with st.sidebar:
    st.page_link('streamlit_app.py', label='Home')
    st.page_link('pages/03_Discover.py', label='Discover')          # tool: see pricing comparisons and other figures
    st.page_link('pages/04_Create.py', label='Create')             # tool: to generate plots
    st.page_link('pages/05_Plan.py', label='Plan')                 # tool: guided walkthrough 
    st.page_link('pages/06_Pricing.py', label='Pricing')     
    st.page_link('pages/02_Contribute.py', label='Contribute') 
    
st.markdown("<h1 style='text-align: center; color: black;'>Metrdy</h1>", unsafe_allow_html=True)
st.divider()

import flowkit as fk
import numpy as np
from sklearn.mixture import GaussianMixture

def find_split_on_dist(m1,m2,std1,std2):
    a = 1/(2*std1**2) - 1/(2*std2**2)
    b = m2/(std2**2) - m1/(std1**2)
    c = m1**2 /(2*std1**2) - m2**2 / (2*std2**2) - np.log(std2/std1)
    sol = np.roots([a,b,c])
    if len(sol) == 1:
        return sol[0]
    elif len(sol) == 2:
        if (sol[0] > min([m1, m2])) and (sol[0] < max([m1, m2])):
            return sol[0]
        else:
            return sol[1]
        
def seperation_index(pos, neg):
    return (pos.median().values[0] - neg.median().values[0])/((neg.quantile(.84).values[0] - neg.median().values[0])/0.995)

def stain_index(pos, neg):
    return (pos.median().values[0] - neg.median().values[0])/(2 * neg.std().values[0])

def seperation_stain_index_gauss(df, channel="FSC-H"):
    # since the guassian in non deterministic, the n_init param is important to weed out unlucky cases for EM algorithm
    gmm = GaussianMixture(n_components=2, n_init=10)
    gmm.fit(df[channel])
    means = gmm.means_
    standard_deviations = gmm.covariances_**0.5
    split_point = find_split_on_dist(means[0][0], means[1][0], standard_deviations[0][0][0], standard_deviations[1][0][0])
    pos = df[df[channel] < split_point][channel]
    neg = df[df[channel] >= split_point][channel]
    sep_ind = seperation_index(pos, neg)
    sta_ind = stain_index(pos, neg)
    if sep_ind < 0:
        sep_ind = seperation_index(neg, pos)
        sta_ind = stain_index(neg, pos)
    return sep_ind, sta_ind

def calc_index(dfs, channel):
    sep_l, sta_l = [], []
    for df_events in dfs:
        sep, sta = seperation_stain_index_gauss(df_events, channel=channel)
        sep_l.append(sep)
        sta_l.append(sta)
    return sep_l, sta_l


col1, col2, col3 = st.columns([1, 5, 1])
with col2:
    uploaded_files = st.file_uploader("""Add single or multiple FCS files. Please note that the auto gating requires some heavyweight 
                                      statistical models than are non deterministic and requires several folds of fitting for the 
                                      best fit. Please wait a few moments for the process to finish. """, 
                                      accept_multiple_files=True, type='fcs')
    dfs, con_fs, df_events = [], [], pd.DataFrame()
    for uploaded_file in uploaded_files:
        con_fs.append(uploaded_file.name[:-4])
        df_events = fk.Sample(uploaded_file).as_dataframe(source='raw')
        dfs.append(df_events)
    if not df_events.empty:
        channel_choice = st.selectbox("Select your target channel", options=df_events.columns, index=None)
        if st.button(label="Submit", type="primary"):
            sep_l, sta_l = calc_index(dfs, channel=channel_choice[0])
            df = pd.DataFrame(np.array([con_fs, sep_l, sta_l]).T, columns=["Concentration", "Seperation Index", "Stain Index"]).astype(float).sort_values(by=["Concentration"])

            if not df.empty:
                _lock = RendererAgg.lock
                with _lock:
                    fig, ax = plt.subplots()
                    ax.plot([str(x) for x in df["Concentration"].to_list()], df["Seperation Index"],label="seperation index")
                    ax.plot([str(x) for x in df["Concentration"].to_list()], df["Stain Index"], label="stain index")
                    ax.set_xlabel("Index")
                    ax.set_ylabel("Concentration")
                    ax.set_title("Seperation and Stain Index for uploaded data")
                    st.pyplot(fig)

                st.line_chart(df, x="Concentration", y=["Seperation Index", "Stain Index"])

