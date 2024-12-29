import cv2
import numpy as np


def findCircles(image):
    circleLocation = []

    # Séparer en 4 quarts l'image
    # Obtenir les dimensions de l'image
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

    return circleLocation