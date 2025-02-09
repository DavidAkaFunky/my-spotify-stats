import spotipy, os, re
from dotenv import load_dotenv
from classes import Spotistats
import pandas as pd
import streamlit as st
import plotly.express as px

def plot_all(df):
    st.title("Music Track Analysis")
    columns = df.columns
    
    # Create Tabs dynamically
    tabs = st.tabs([col.capitalize() for col in columns])

    # Loop through each tab and display the histogram
    for i, col in enumerate(columns):
        with tabs[i]:
            fig = px.histogram(df, x=col, nbins=10, title=f"{col.capitalize()} Histogram")
            st.plotly_chart(fig, use_container_width=True)

if __name__ == "__main__":
    load_dotenv()
    sp = Spotistats(os.environ)
    pattern = r"\d{2}\/\d{4}"
    playlists = list(map(lambda x: x["id"], filter(lambda x: re.match(pattern, x["name"]), sp.get_personal_playlists())))
    first_tracks = sp.get_playlist_track_ids(playlists[-1])
    features = sp.get_tracks_audio_features(first_tracks)
    df = pd.DataFrame.from_dict(features)
    
    df["duration"] = df["duration_ms"] / 1000
    df = df.drop(columns=["id", "time_signature", "key", "mode", "duration_ms"])
    plot_all(df)