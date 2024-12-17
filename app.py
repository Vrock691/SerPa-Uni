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

    # Segmentation de l'image
    _, img = cv2.threshold(img, 100, 255, 0)

    # création de l’objet de la classe ORB
    orb = cv2.ORB_create()

    # points de l'image uploadé
    pointsPath1, descripteursImgPath1 = orb.detectAndCompute(img, None)

    # Tentative de trouver un pattern dans les 16 disponibles
    finds = []
    for i in range(16):
        print(img)

        path = "./patterns/Paterne" + str(i+1) + ".png"
        st.write(path)
        currentPattern = cv2.imread(path, cv2.IMREAD_COLOR)
        currentPattern = cv2.cvtColor(currentPattern, cv2.COLOR_BGR2GRAY)

        # descripteurs
        pointsPath2, descripteursImgPath2 = orb.detectAndCompute(currentPattern, None)

        algoBF = cv2.BFMatcher(cv2.NORM_HAMMING, crossCheck=False)
        paires_corresp = algoBF.knnMatch(descripteursImgPath1, descripteursImgPath2, k=5)

        # Tri par distance
        Matches_tri = sorted(paires_corresp, key=lambda x:x[0].distance)

        # Affichage
        matched = cv2.drawMatchesKnn(img, pointsPath1, currentPattern, pointsPath2, Matches_tri[:10], None)
        st.image(matched)

    st.image(img)