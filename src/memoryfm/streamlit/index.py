import streamlit as st
from memoryfm.streamlit.pages.manage_imports import new_imports, delete_import
from memoryfm.streamlit.pages.overview import overview

new_imports_pg = st.Page(new_imports, title="New Import")
delete_import_pg = st.Page(delete_import, title="Delete Import")
overview_pg = st.Page(overview, title="Dashboard")
