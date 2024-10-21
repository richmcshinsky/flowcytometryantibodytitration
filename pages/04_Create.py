import streamlit as st
import pandas as pd
import matplotlib.pyplot as plt
from matplotlib.backends.backend_agg import RendererAgg
import FlowCal
import plotly.express as px


st.set_page_config(page_title='Metrdy', layout="wide")

# builds the sidebar menu
with st.sidebar:
    st.page_link('streamlit_app.py', label='Home')
    st.page_link('pages/03_Discover.py', label='Discover')          # tool: see pricing comparisons and other figures
    st.page_link('pages/04_Create.py', label='Create')             # tool: to generate plots
    st.page_link('pages/05_Plan.py', label='Plan')                 # tool: guided walkthrough 
    st.page_link('pages/06_Pricing.py', label='Pricing')     
    st.page_link('pages/02_Contribute.py', label='Contribute') 
    
#st.markdown("<h1 style='text-align: center; color: black;'>Metrdy</h1>", unsafe_allow_html=True)
col1, col2, col3 = st.columns([2,3,2], gap="small")
with col2:
    st.image("data/logoex.png")
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

st.markdown("<h3 style='text-align: center; color: black;'>Upload your FCS files and auto generate a seperation and stain index chart</h3>", unsafe_allow_html=True)


# https://welcome.cytekbio.com/hubfs/DOC-00504-Rev.-A_Antibody-Titration-Protocol.pdf
# https://flowcal.readthedocs.io/en/latest/python_tutorial/gate.html
col1, col2, col3 = st.columns([1, 5, 1])
with col2:
    st.write("NOTE: name the files like 0.25.fcs, 0.5.fcs, 1.fcs, 2.fcs...! The name tells the plot what concentration to label the file as.")
    st.write("""NOTE: process starts by cleaning the base data by removing staurated events with a density gate, which typically have better 
             performance than ellipse gates and manual gates. Once the overall data has been filtered, then there is an auto split
             between the positive and negative groups using some heavyweight statistical moels that are non deterministic and 
             require several folds of fittiing for stable results. Please wait a few moments for the process to finish, clicking the
             submit button again will start the process from the beginning.""")
    
    with st.expander("Example: see examples of how the auto process works"):
        col1, col2 = st.columns(2)
        with col1:
            st.image("data/cleaningex1.png")
        with col2:
            st.image("data/cleaningex2.png")

    # get data into pandas df
    uploaded_files = st.file_uploader("""Add single or multiple FCS files.""", 
                                      accept_multiple_files=True, type='fcs')
    dfs, con_fs, df_events = [], [], pd.DataFrame()
    for uploaded_file in uploaded_files:
        con_fs.append(uploaded_file.name[:-4])
        df_events = fk.Sample(uploaded_file).as_dataframe(source='raw')
        cols = df_events.columns
        df_events = FlowCal.gate.high_low(df_events.to_numpy(), channels=[1, 3])
        df_events = FlowCal.gate.density2d(df_events, channels=[1, 3], gate_fraction=0.75)
        df_events = pd.DataFrame(df_events, columns=cols)
        dfs.append(df_events)
    if not df_events.empty:
        channel_choice = st.selectbox("Select your target channel", options=df_events.columns, index=None)
        if st.button(label="Submit", type="primary"):
            sep_l, sta_l = calc_index(dfs, channel=channel_choice[0])
            df = pd.DataFrame(np.array([con_fs, sep_l, sta_l]).T, columns=["Concentration", "Seperation Index", "Stain Index"]).astype(float).sort_values(by=["Concentration"])
            if not df.empty:
                # line plot of seperation and stain index values
                _lock = RendererAgg.lock
                with _lock:
                    fig, ax = plt.subplots()
                    ax.plot([str(x) for x in df["Concentration"].to_list()], df["Seperation Index"],label="seperation index")
                    ax.plot([str(x) for x in df["Concentration"].to_list()], df["Stain Index"], label="stain index")
                    ax.set_ylabel("Index")
                    ax.set_xlabel("Concentration")
                    ax.set_title("Seperation and Stain Index for uploaded data")
                    st.pyplot(fig)

                df_t = pd.DataFrame(columns=["fl", "con", "seperation", "stain"])
                fl, con_l, seper_l, stain_l = [], [], [], []
                for d,c,s1,s2 in zip(dfs, con_fs, sep_l, sta_l):
                    fl += d[channel_choice[0]][channel_choice[1]].to_list()
                    con_l += [c] * len(d)
                    stain_l += [str(round(s2,2))] * len(d)
                    seper_l += [str(round(s1,2))] * len(d)
                df_t["fl"] = fl
                df_t["con"] = con_l
                df_t["seperation"] = seper_l
                df_t["stain"] = stain_l
                
                # strip plot of data
                sample_size = 30000 if len(df_t) > 30000 else len(df_t)
                df_t = df_t.sample(sample_size)
                df_t = df_t[df_t["fl"].astype(float) < 500000]
                df_t = df_t.sort_values(by=["con"])
                df_t["axis"] = [str(x) + "<br>" + str(y) + "<br>" + str(z) for x,y, z in zip(df_t["con"], df_t["stain"], df_t["seperation"])]
                fig = px.strip(df_t, x="axis", y="fl")
                fig.update_traces(marker_size=3)
                fig.update_yaxes(type="log", exponentformat='power')
                fig.update_layout(yaxis_title=channel_choice[1], xaxis_title=None, xaxis={'side': 'top'}, showlegend=False)
                fig.add_annotation(dict(font=dict(color="black",size=12),x=-0.55,y=1.25,showarrow=False,xref="x",yref="paper",
                                            text='Microliters:<br>Stain Index:<br>Seperation Index:',textangle=0))
                st.plotly_chart(fig, use_container_width=True)

