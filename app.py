import streamlit as st
import os

os.system('playwright install')
os.system('playwright install-deps')

st.set_page_config(layout="wide")

codebook = st.Page(
    "frontend/guide.py", title="Guide", icon=":material/book:"
)

pulsing = st.Page(
    "frontend/pulsing.py", title="Generate Output", icon=":material/experiment:", default=True
)

# dashboard = st.Page(
#     "frontend/dashboard_mongo.py", title="Dashboard", icon=":material/dashboard:"
# )
# summary = st.Page(
#     "frontend/summarisation.py", title="Summary", icon=":material/summarize:"
# )



pg = st.navigation([codebook, pulsing])


pg.run()