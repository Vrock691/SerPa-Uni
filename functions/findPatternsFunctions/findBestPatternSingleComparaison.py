import streamlit as st
import cv2

from functions.getSiftMatches import getSiftMatches


def findBestPatternSingleComparaison(image):
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

        good_matches, keypoints1, keypoints2, descriptors1, descriptors2 = getSiftMatches(
            imageGrey=image, imageName="Ref", patternImage=current_pattern, patternImageName=pattern_path)

        matches_results.append(
            (pattern_path, len(good_matches), good_matches, keypoints2))

    # Identifier le meilleur pattern
    if matches_results:
        best_pattern = max(matches_results, key=lambda x: x[1])
        best_pattern_path, num_matches, good_matches, keypoints2 = best_pattern

        st.success(
            f"Meilleur pattern détecté : {best_pattern_path} avec {num_matches} correspondances.")

        # Affichage des correspondances
        best_pattern_image = cv2.imread(best_pattern_path, cv2.IMREAD_COLOR)
        matched_image = cv2.drawMatches(
            image, keypoints1, best_pattern_image, keypoints2,
            good_matches, None, flags=cv2.DrawMatchesFlags_NOT_DRAW_SINGLE_POINTS
        )
        st.image(
            matched_image, caption=f"Correspondances avec {best_pattern_path}", use_container_width=True)

        associate_numbers = {
            "./patterns/Paterne1.png": 0,
            "./patterns/Paterne2.png": 2,
            "./patterns/Paterne3.png": 1,
            "./patterns/Paterne4.png": 4,
            "./patterns/Paterne5.png": 8,
            "./patterns/Paterne6.png": 3,
            "./patterns/Paterne7.png": 12,
            "./patterns/Paterne8.png": 5,
            "./patterns/Paterne9.png": 10,
            "./patterns/Paterne10.png": 9,
            "./patterns/Paterne11.png": 6,
            "./patterns/Paterne12.png": 13,
            "./patterns/Paterne13.png": 15,
            "./patterns/Paterne14.png": 14,
            "./patterns/Paterne15.png": 11,
            "./patterns/Paterne16.png": 7,
        }

        # Affichage du nombre correspondant au pattern
        st.write("### Nombre trouvé via la detection de pattern : " + str(associate_numbers[best_pattern_path]))
    else:
        st.error("Aucun pattern détecté.")
