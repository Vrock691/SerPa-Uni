import streamlit as st
import pandas as pd
import cv2
import numpy as np
from PIL import Image

 
image = None 

st.write("""
# SerPA
         
Uploadez une image ici :
""")

image = st.file_uploader("Image", type=['png', 'jpg'] , accept_multiple_files=False, label_visibility="visible")

if image is not None:
    st.write("""
        Votre image
""")
    # Enregistrement de l'image en mémoire
    imageToSave = Image.open(image)
    imageToSave = imageToSave.save('img.png')

    # Conversion de l'image en niveau de gris
    img = cv2.imread('img.png', cv2.IMREAD_COLOR)
    img = cv2.cvtColor(img, cv2.COLOR_BGR2GRAY)

    # Filtre canny
    img = cv2.Canny(img, 50, 50)

    st.image(img)