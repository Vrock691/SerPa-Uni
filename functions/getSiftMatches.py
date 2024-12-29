import cv2
import streamlit as st

# Création de l'objet SIFT
sift = cv2.SIFT_create(nfeatures=1000, nOctaveLayers=1, contrastThreshold=0.3)

def getSiftMatches(imageGrey, imageName, patternImage, patternImageName = "pattern"):
    # Points et descripteurs pour la ROI
    keypoints1, descriptors1 = sift.detectAndCompute(imageGrey, None)

    # Conversion du pattern en niveaux de gris
    pattern_gray = cv2.cvtColor(patternImage, cv2.COLOR_BGR2GRAY)

    # Points et descripteurs du pattern
    keypoints2, descriptors2 = sift.detectAndCompute(pattern_gray, None)
    if descriptors2 is None:
        st.warning(f"Aucun point clé détecté dans le pattern {imageName}.")

    # Appariement des descripteurs avec BFMatcher
    bf = cv2.BFMatcher(cv2.NORM_L2, crossCheck=False)
    matches = bf.knnMatch(descriptors1, descriptors2, k=2)

    # Filtrage des bonnes correspondances
    good_matches = []
    for m, n in matches:
        if m.distance < 0.75 * n.distance:
            good_matches.append(m)

    return good_matches, keypoints1, keypoints2, descriptors1, descriptors2