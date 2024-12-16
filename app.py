import streamlit as st
import pandas as pd
 
st.write("""
# SerPA
""")

def onImageUploaded():
    st.write('uploaded')

st.file_uploader("Image", type=['png', 'jpg'] , accept_multiple_files=False, label_visibility="visible", on_change=onImageUploaded())

