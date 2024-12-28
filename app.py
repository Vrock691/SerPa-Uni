import streamlit as st
import cv2
import numpy as np
from PIL import Image

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
    circleLocation = []

    # Séparer en 4 quarts l'image
    # Obtenir les dimensions de l'image
    height, width = roi_thresh.shape

    # Calculer les dimensions de chaque partie
    half_height = height // 2
    half_width = width // 2

    # Découper l'image en 4 parties
    top_left = roi_thresh[:half_height, :half_width].copy()
    top_right = roi_thresh[:half_height, half_width:].copy()
    bottom_left = roi_thresh[half_height:, :half_width].copy()
    bottom_right = roi_thresh[half_height:, half_width:].copy()
    quart = [top_left, top_right, bottom_left, bottom_right]

    # Scanner chaque coin pour y trouver les cercles
    circleLocation = []  # Liste pour stocker les cercles détectés

    for i in range(4):  # Boucle sur les 3 quarts de l'image
        quart[i] = cv2.GaussianBlur(quart[i], (3, 3), 2)

        HoughCircles = cv2.HoughCircles(
            quart[i],
            cv2.HOUGH_GRADIENT,
            dp=1,
            minDist=5,
            param1=50,
            param2=25,
        )

        if HoughCircles is not None:
            HoughCircles = np.round(HoughCircles[0, :]).astype("int")  # Convertir en entiers

            for j in HoughCircles:
                x, y, r = j  # Extraire les coordonnées et le rayon
                cv2.circle(quart[i], (x, y), r, (0, 0, 255), 2)  # Dessiner le cercle

            # Prendre le 1er rond trouvé
            x, y, r = HoughCircles[0]
            if i == 0:
                circleLocation.append(np.array([x-30, y-30]))
            elif i == 1:
                circleLocation.append(np.array([x+half_width+30, y-30]))
            elif i == 2:
                circleLocation.append(np.array([x-30, y+half_height+30]))
            elif i == 3:
                circleLocation.append(np.array([x+half_width+30, y+half_height+30]))

    # Applanir l'image
    if circleLocation is not None and len(circleLocation) == 4 :
        st.write("### Points d'angles détéctés, mise à plat de l'image")

        # Points de l'image source (par exemple, 4 coins d'un document)
        src_points = np.array(circleLocation, dtype=np.float32)

        # Points de destination (rectangle aplati)
        dst_points = np.array([[0, 0], [400, 0], [0, 400], [400, 400]], dtype=np.float32)

        # Matrice de transformation
        matrix = cv2.getPerspectiveTransform(src_points, dst_points)

        # Appliquer la transformation
        roi_thresh = cv2.warpPerspective(roi_thresh, matrix, (400, 400))

        st.image(roi_thresh, caption="Image applanie")

    # Reconnaissance de pattern
    st.write("### Détection de patterns dans la ROI :")

    # Création de l'objet SIFT
    sift = cv2.SIFT_create(nfeatures=1000, nOctaveLayers=1, contrastThreshold=0.3)

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