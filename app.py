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
    import streamlit as st
    import cv2
    import numpy as np
    from PIL import Image

image = None

st.write("""
# SerPA   
Uploadez une image ici :
""")

image = st.file_uploader("Image", type=['png', 'jpg'], accept_multiple_files=False, label_visibility="visible")

if image is not None:
    st.write("### Votre image :")
    # Charger l'image uploadée
    uploaded_image = Image.open(image)
    st.image(uploaded_image, caption="Image uploadée", use_column_width=True)

    # Enregistrement temporaire et lecture avec OpenCV
    uploaded_image.save('img.png')
    img = cv2.imread('img.png', cv2.IMREAD_COLOR)
    
    # Conversion en niveaux de gris
    img_gray = cv2.cvtColor(img, cv2.COLOR_BGR2GRAY)

    # Segmentation de l'image
    _, img_thresh = cv2.threshold(img_gray, 100, 255, cv2.THRESH_BINARY)

    # Création de l’objet ORB
    orb = cv2.ORB_create()

    # Points et descripteurs de l'image uploadée
    keypoints1, descriptors1 = orb.detectAndCompute(img_thresh, None)

    if descriptors1 is None:
        st.error("Aucun point clé détecté dans l'image uploadée. Essayez une autre image.")
    else:
        # Liste pour stocker les correspondances des patterns
        matches_results = []

        # Parcourir les 16 patterns
        for i in range(16):
            pattern_path = f"./patterns/Paterne{i + 1}.png"
            st.write(f"Traitement du pattern : {pattern_path}")

            # Charger le pattern
            current_pattern = cv2.imread(pattern_path, cv2.IMREAD_COLOR)
            if current_pattern is None:
                st.warning(f"Le fichier {pattern_path} n'a pas pu être chargé.")
                continue

            # Conversion du pattern en niveaux de gris
            pattern_gray = cv2.cvtColor(current_pattern, cv2.COLOR_BGR2GRAY)

            # Points et descripteurs du pattern
            keypoints2, descriptors2 = orb.detectAndCompute(pattern_gray, None)
            if descriptors2 is None:
                st.warning(f"Aucun point clé détecté dans le pattern {pattern_path}.")
                continue

            # Appariement des descripteurs
            bf = cv2.BFMatcher(cv2.NORM_HAMMING, crossCheck=False)
            matches = bf.knnMatch(descriptors1, descriptors2, k=2)

            # Filtrage des bonnes correspondances avec le ratio test
            good_matches = []
            for m, n in matches:
                if m.distance < 0.75 * n.distance:
                    good_matches.append(m)

            # Stocker le résultat pour ce pattern
            matches_results.append((pattern_path, len(good_matches), good_matches, keypoints2))

        # Identifier le meilleur pattern en fonction du nombre de correspondances
        if matches_results:
            best_pattern = max(matches_results, key=lambda x: x[1])
            best_pattern_path, num_matches, good_matches, keypoints2 = best_pattern

            st.success(f"Meilleur pattern détecté : {best_pattern_path} avec {num_matches} correspondances.")

            # Affichage des correspondances avec le meilleur pattern
            best_pattern_image = cv2.imread(best_pattern_path, cv2.IMREAD_COLOR)
            best_pattern_gray = cv2.cvtColor(best_pattern_image, cv2.COLOR_BGR2GRAY)
            matched_image = cv2.drawMatches(
                img_thresh, keypoints1, best_pattern_gray, keypoints2,
                good_matches, None, flags=cv2.DrawMatchesFlags_NOT_DRAW_SINGLE_POINTS
            )
            st.image(matched_image, caption=f"Correspondances avec {best_pattern_path}", use_column_width=True)
        else:
            st.error("Aucun pattern détecté.")

    # Affichage de l'image prétraitée
    st.write("### Image prétraitée :")
    st.image(img_thresh, caption="Image en niveaux de gris et seuillée", use_column_width=True)

    '''