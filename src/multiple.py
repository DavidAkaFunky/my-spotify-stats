import os, re
import pandas as pd
import streamlit as st
import plotly.express as px
from classes import Spotistats

def plot_all(df):
    columns = [x for x in df.columns if x != "month"]
    
    # Create Tabs dynamically
    tabs = st.tabs([col.capitalize() for col in columns])

    # Loop through each tab and display the histogram
    for i, col in enumerate(columns):
        with tabs[i]:
            fig = px.box(df, x="month", y=col, title=f"{col.capitalize()} Histogram")
            st.plotly_chart(fig, use_container_width=True)

st.title("Multiple Playlist Track Analysis")

sp = Spotistats(os.environ)
pattern = r"\d{2}\/\d{4}"
playlists = list(
    map(
        lambda x: [x["id"]] + x["name"].split("/"), 
        filter(lambda x: re.match(pattern, x["name"]), sp.get_personal_playlists())
    )
)

features = {}
for id, month, year in playlists:
    features[f"{year}/{month}"] = sp.get_tracks_audio_features(sp.get_playlist_track_ids(id))

# Convert to a DataFrame
df = pd.concat(
    [pd.DataFrame(rows).assign(month=idx) for idx, rows in features.items()], 
    ignore_index=True
).sort_values("month")

df["duration"] = df["duration_ms"] / 1000
df = df.drop(columns=["id", "time_signature", "key", "mode", "duration_ms"])
plot_all(df)