import streamlit as st
import cv2
import numpy as np

from functions.findPatternsFunctions.findBestPatternSingleComparaison import findBestPatternSingleComparaison
from functions.getSiftMatches import getSiftMatches
from functions.warpImage import warpImage


def findBestPatternMultiComparaison(image):
    number = 0
    color = "black"

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

    rectangledetected = True
    quartNum = 0
    while rectangledetected == True and quartNum < 4:
        # Parcourir les patterns quart pour trouver des rectangles noirs
        contours, _ = cv2.findContours(
            quart[quartNum], cv2.RETR_EXTERNAL, cv2.CHAIN_APPROX_SIMPLE)

        # On prend le premier résultat
        contour = contours[0]

        # Approximation du contour pour simplifier la forme
        epsilon = 0.02 * cv2.arcLength(contour, True)
        approx = cv2.approxPolyDP(contour, epsilon, True)

        if len(approx) >= 4:
            if cv2.contourArea(approx) > 10:  # Filtrer les très petits objets
                # Dessiner le contour détecté
                cv2.drawContours(quart[quartNum], [approx], -1, (0, 255, 0), 3)

                if (len(approx) == 4): 
                    color = "white"
                else:
                    color = "black"

                st.image(quart[quartNum], "Couleur du rectangle : " + color)

                if quartNum == 0:
                    if len(approx) != 4: number += 1
                elif quartNum == 1:
                    if len(approx) != 4: number += 2
                elif quartNum == 2:
                    if len(approx) != 4: number += 4
                elif quartNum == 3:
                    if len(approx) != 4: number += 8

        else: # Si pas de carré trouvé on fait une vérification avec sift
            rectangledetected = False
            st.warning("Détection rectangle échouée")
            findBestPatternSingleComparaison(image=image)

        quartNum += 1

    if rectangledetected:
        st.write("### Nombre trouvé via la multidétection de rectangle : " + str(number))