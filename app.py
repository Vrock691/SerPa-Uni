import streamlit as st
import cv2
import numpy as np
from PIL import Image

from functions.findCircles import findCircles
from functions.findPatternsFunctions.findBestPatternMultiComparaison import findBestPatternMultiComparaison
from functions.findPatternsFunctions.findBestPatternSingleComparaison import findBestPatternSingleComparaison
from functions.warpImage import warpImage

st.title("SerPA - Reconnaissance de Pattern")

'''
L'application fonctionne avec :

    3-3 (Avec Resize)
    4-3 (Sans Resize)
    1-3 (Avec Resize)
    2-3 (Avec Resize)
    B-2-autre (Sans Resize)
    Patern2_MiseEnAbime (Sans Resize)
    Produit-1
    MEA-6-3G (Avec Resize)
    ---------------------------------
    Taux de réussite : 24.24% (Ne fonctionne pas avec le reste.)

'''

# Chargement de l'image
image = st.file_uploader("Veuillez téléchargez une image juse en dessous :", type=["jpg", "png"])

if image is not None:
    # Chargement de l'image avec PIL
    uploaded_image = Image.open(image)
    img_array = np.array(uploaded_image)
    h, w, _ = img_array.shape

    # Affichage de l'image originale
    st.write("Image uploadé avec succès !")

    # Sliders pour sélectionner la ROI
    st.write("### Sélectionnez la zone d'intérêt (ROI) :")
    x1 = st.slider("x1 (gauche)", min_value=0, max_value=w, value=0)
    y1 = st.slider("y1 (haut)", min_value=0, max_value=h, value=0)
    x2 = st.slider("x2 (droite)", min_value=0, max_value=w, value=w)
    y2 = st.slider("y2 (bas)", min_value=0, max_value=h, value=h)

    # Vérification si les sliders définissent une zone valide
    if x1 < x2 and y1 < y2:
        # Extraire la ROI
        roi = img_array[y1:y2, x1:x2]

        # Visualisation de la ROI
        preview = img_array.copy()
        cv2.rectangle(preview, (x1, y1), (x2, y2), (255, 0, 0), 2)
        st.image(preview, caption="Image avec ROI sélectionnée", use_container_width=True)

        # Afficher la ROI seule
        st.image(roi, caption="Zone d'intérêt sélectionnée (ROI)", use_container_width=True)
    else:
        st.error("La zone sélectionnée n'est pas valide. Vérifiez les valeurs des sliders.")
    
    # Conversion de la ROI en niveaux de gris
    roi_gray = cv2.cvtColor(roi, cv2.COLOR_BGR2GRAY)
    
    # Dilatation en cas d'image de petite taille avec gaussian blur
    if (x1 < 300 or x2 < 300 or y1 < 300 or y2 < 300):
        roi_gray = cv2.dilate(roi_gray, np.ones((1, 1), np.uint8))

    # Segmentation de l'image
    _, roi_thresh = cv2.threshold(roi_gray, 100, 255, cv2.THRESH_BINARY)

    # Détecter les cercles
    circleLocation = findCircles(roi_thresh)

    # Applanir l'image
    if circleLocation is not None and len(circleLocation) == 4 :
        st.write("### Points d'angles détéctés, mise à plat de l'image")
        roi_thresh = warpImage(circleLocation=circleLocation, image=roi_thresh)
        st.image(roi_thresh, caption="Image applanie")

    # Reconnaissance de pattern
    st.write("### Détection de patterns dans la ROI :")

    if (circleLocation is not None and circleLocation == 4):
        # Si les ronds ont été détécté, on applique l'algorithme poussé
        findBestPatternMultiComparaison(roi_thresh)
    else:
        # sinon on fait la comparaison sur toute l'image
        findBestPatternSingleComparaison(roi_thresh)