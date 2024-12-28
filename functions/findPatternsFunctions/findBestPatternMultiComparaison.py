import streamlit as st
import cv2

from functions.getSiftMatches import getSiftMatches

def findBestPatternMultiComparaison(image):
    patterns_votes = []

    # Découpage de l'image originale en 4 coins
    height, width = image.shape

    # Calculer les dimensions de chaque partie
    half_height = height // 2
    half_width = width // 2

    # Découper l'image en 4 parties
    top_left = image[:half_height, :half_width].copy()
    top_right = image[:half_height, half_width:].copy()
    bottom_left = image[half_height:, :half_width].copy()
    bottom_right = image[half_height:, half_width:].copy()
    quart = [top_left, top_right, bottom_left, bottom_right]

    for quartNum in range(4):
        # Parcourir les patterns
        for i in range(16):
            pattern_path = f"../patterns/Paterne{i+1}.png"
            st.write(f"Traitement du pattern : {pattern_path}")

            # Charger le pattern
            current_pattern = cv2.imread(pattern_path, cv2.IMREAD_COLOR)
            if current_pattern is None:
                st.warning(f"Le fichier {pattern_path} n'a pas pu être chargé.")
                continue

            good_matches, keypoints1, keypoints2, descriptors1, descriptors2 = getSiftMatches(imageGrey=image, imageName="Ref", patternImage=current_pattern, patternImageName=pattern_path)

            matches_results.append((pattern_path, len(good_matches), good_matches, keypoints2))

    # Identifier le meilleur pattern
    if matches_results:
        best_pattern = max(matches_results, key=lambda x: x[1])
        best_pattern_path, num_matches, good_matches, keypoints2 = best_pattern

        st.success(f"Meilleur pattern détecté : {best_pattern_path} avec {num_matches} correspondances.")

        # Affichage des correspondances
        best_pattern_image = cv2.imread(best_pattern_path, cv2.IMREAD_COLOR)
        matched_image = cv2.drawMatches(
            image, keypoints1, best_pattern_image, keypoints2,
            good_matches, None, flags=cv2.DrawMatchesFlags_NOT_DRAW_SINGLE_POINTS
        )
        st.image(matched_image, caption=f"Correspondances avec {best_pattern_path}", use_container_width=True)
    else:
        st.error("Aucun pattern détecté.")