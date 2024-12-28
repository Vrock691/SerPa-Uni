import cv2
import numpy as np


def warpImage(circleLocation, image):
    # Points de l'image source (par exemple, 4 coins d'un document)
    src_points = np.array(circleLocation, dtype=np.float32)

    # Points de destination (rectangle aplati)
    dst_points = np.array([[0, 0], [400, 0], [0, 400], [400, 400]], dtype=np.float32)

    # Matrice de transformation
    matrix = cv2.getPerspectiveTransform(src_points, dst_points)

    # Appliquer la transformation
    image = cv2.warpPerspective(image, matrix, (400, 400))

    return image