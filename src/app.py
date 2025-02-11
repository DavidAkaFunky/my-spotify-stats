import streamlit as st
from dotenv import load_dotenv
from classes import Spotistats

load_dotenv()

single = st.Page("single.py", title="Single")
multiple = st.Page("multiple.py", title="Multiple")

pg = st.navigation([single, multiple])
st.set_page_config(page_title="My Spotify Stats", layout="wide")
pg.run()