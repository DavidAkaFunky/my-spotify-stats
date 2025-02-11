import os
import pandas as pd
import streamlit as st
import plotly.express as px
from classes import Spotistats

def plot_all(df):
    columns = df.columns
    
    # Create Tabs dynamically
    tabs = st.tabs([col.capitalize() for col in columns])

    # Loop through each tab and display the histogram
    for i, col in enumerate(columns):
        with tabs[i]:
            fig = px.histogram(df, x=col, nbins=10, title=f"{col.capitalize()} Histogram")
            if col not in {"loudness", "tempo", "duration"}:
                fig.update_xaxes(range=[0, 1])
            st.plotly_chart(fig, use_container_width=True)

sp = Spotistats(os.environ)

st.title("Single Playlist Track Analysis")
with st.form("my_form"):
    url = st.text_input("Playlist URL")
    st.form_submit_button("Check it out!")
    
if url:
    tracks = sp.get_playlist_track_ids(url)
    features = sp.get_tracks_audio_features(tracks)
    df = pd.DataFrame.from_dict(features)
    df["duration"] = df["duration_ms"] / 1000
    df = df.drop(columns=["id", "time_signature", "key", "mode", "duration_ms"])
    plot_all(df)