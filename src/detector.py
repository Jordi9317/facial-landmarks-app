# src/detector.py
"""
Detector de landmarks faciales usando face_recognition (compatible con Python 3.13+).
"""

import cv2
import face_recognition
import numpy as np
from .config import LANDMARK_COLOR, LANDMARK_RADIUS, LANDMARK_THICKNESS


class FaceLandmarkDetector:
    """
    Clase para detectar y visualizar landmarks faciales usando face_recognition.
    """

    def __init__(self):
        """Inicializa el detector de face_recognition."""
        # face_recognition usa modelos pre-entrenados automáticamente
        pass

    def detect(self, image):
        """
        Detecta landmarks faciales en la imagen usando face_recognition.

        Args:
            image (numpy.ndarray): Imagen en formato BGR (OpenCV)

        Returns:
            tuple: (imagen_procesada, landmarks, info)
                - imagen_procesada: imagen con landmarks dibujados
                - landmarks: lista de landmarks en formato face_recognition
                - info: diccionario con información de detección
        """
        # Convertir BGR a RGB para face_recognition
        imagen_rgb = cv2.cvtColor(image, cv2.COLOR_BGR2RGB)

        # Detectar rostros y landmarks
        face_locations = face_recognition.face_locations(imagen_rgb)
        face_landmarks_list = face_recognition.face_landmarks(imagen_rgb, face_locations)

        # Crear copia para dibujar
        imagen_con_puntos = image.copy()

        info = {
            "rostros_detectados": len(face_landmarks_list),
            "total_landmarks": 0,
            "deteccion_exitosa": len(face_landmarks_list) > 0
        }

        # Si se detectaron rostros
        if face_landmarks_list:
            # Tomar el primer rostro para compatibilidad
            landmarks = face_landmarks_list[0]

            # Contar total de landmarks
            total_points = sum(len(points) for points in landmarks.values())
            info["total_landmarks"] = total_points

            # Dibujar landmarks
            alto, ancho = image.shape[:2]

            # face_recognition landmarks están en formato (x, y)
            for feature_name, points in landmarks.items():
                for point in points:
                    coord_x_pixel = int(point[0])
                    coord_y_pixel = int(point[1])

                    cv2.circle(
                        imagen_con_puntos,
                        (coord_x_pixel, coord_y_pixel),
                        LANDMARK_RADIUS,
                        LANDMARK_COLOR,
                        LANDMARK_THICKNESS
                    )

            return imagen_con_puntos, landmarks, info

        # No se detectó rostro
        return imagen_con_puntos, None, info

    def close(self):
        """Libera recursos del detector (face_recognition no requiere limpieza explícita)."""
        pass