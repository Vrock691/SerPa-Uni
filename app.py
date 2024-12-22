'''

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
    st.write("""Votre image""")

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
        matched = cv2.drawMatchesKnn(img, pointsPath1, currentPattern, pointsPath2, Matches_tri[:25], None)
        st.image(matched)

    st.image(img)

    '''

'''
Algorithme utilisant SIFT + Recadrage manuel
Fonctionne avec :

    NON IDENTIFIE

Erreur avec :

    NON IDENTIFIE

*Les erreurs peuvent être un léger soucis d'identification de pattern ou une mauvaise reconnaissance.*

Ne fonctionne pas avec le reste.

'''

import streamlit as st
import cv2
import numpy as np
from PIL import Image

st.title("SerPA - Sélection de ROI et Reconnaissance de Pattern")

# Chargement de l'image
image = st.file_uploader("Téléchargez une image", type=["jpg", "png"])

if image is not None:
    # Chargement de l'image avec PIL
    uploaded_image = Image.open(image)
    img_array = np.array(uploaded_image)
    h, w, _ = img_array.shape

    # Affichage de l'image originale
    st.image(uploaded_image, caption="Image téléchargée", use_container_width=True)

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

    # Segmentation de l'image
    _, roi_thresh = cv2.threshold(roi_gray, 100, 255, cv2.THRESH_BINARY)

    # Reconnaissance de pattern
    st.write("### Détection de patterns dans la ROI :")

    # Création de l'objet SIFT
    sift = cv2.SIFT_create(nfeatures=800, nOctaveLayers=7, contrastThreshold=0.3)

    # Points et descripteurs pour la ROI
    keypoints1, descriptors1 = sift.detectAndCompute(roi_thresh, None)

    if descriptors1 is None:
        st.error("Aucun point clé détecté dans la ROI. Essayez une autre image ou une autre zone.")
    else:
        matches_results = []

        # Parcourir les patterns
        for i in range(16):
            pattern_path = f"./patterns/Paterne{i+1}.png"
            st.write(f"Traitement du pattern : {pattern_path}")

            # Charger le pattern
            current_pattern = cv2.imread(pattern_path, cv2.IMREAD_COLOR)
            if current_pattern is None:
                st.warning(f"Le fichier {pattern_path} n'a pas pu être chargé.")
                continue

            # Conversion du pattern en niveaux de gris
            pattern_gray = cv2.cvtColor(current_pattern, cv2.COLOR_BGR2GRAY)

            # Points et descripteurs du pattern
            keypoints2, descriptors2 = sift.detectAndCompute(pattern_gray, None)
            if descriptors2 is None:
                st.warning(f"Aucun point clé détecté dans le pattern {pattern_path}.")
                continue

            # Appariement des descripteurs avec BFMatcher
            bf = cv2.BFMatcher(cv2.NORM_L2, crossCheck=False)
            matches = bf.knnMatch(descriptors1, descriptors2, k=2)

            # Filtrage des bonnes correspondances
            good_matches = []
            for m, n in matches:
                if m.distance < 0.75 * n.distance:
                    good_matches.append(m)

            matches_results.append((pattern_path, len(good_matches), good_matches, keypoints2))

        # Identifier le meilleur pattern
        if matches_results:
            best_pattern = max(matches_results, key=lambda x: x[1])
            best_pattern_path, num_matches, good_matches, keypoints2 = best_pattern

            st.success(f"Meilleur pattern détecté : {best_pattern_path} avec {num_matches} correspondances.")

            # Affichage des correspondances
            best_pattern_image = cv2.imread(best_pattern_path, cv2.IMREAD_COLOR)
            matched_image = cv2.drawMatches(
                roi_thresh, keypoints1, best_pattern_image, keypoints2,
                good_matches, None, flags=cv2.DrawMatchesFlags_NOT_DRAW_SINGLE_POINTS
            )
            st.image(matched_image, caption=f"Correspondances avec {best_pattern_path}", use_container_width=True)
        else:
            st.error("Aucun pattern détecté.")

'''
Algorithme utilisant SIFT + Recadrage manuel
Fonctionne avec :

    3-3


Erreur avec :

    NON IDENTIFIE

*Les erreurs peuvent être un léger soucis d'identification de pattern ou une mauvaise reconnaissance.*

Ne fonctionne pas avec le reste.

'''