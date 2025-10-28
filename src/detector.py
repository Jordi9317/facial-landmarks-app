# src/detector.py
"""
Detector de landmarks faciales usando MediaPipe.
"""

import cv2
import mediapipe as mp
from .config import FACE_MESH_CONFIG, LANDMARK_COLOR, LANDMARK_RADIUS, LANDMARK_THICKNESS


class FaceLandmarkDetector:
    """
    Clase para detectar y visualizar landmarks faciales.
    """

    def __init__(self):
        """Inicializa el detector de MediaPipe."""
        self.face_mesh = mp.solutions.face_mesh.FaceMesh(**FACE_MESH_CONFIG)
        self.mp_drawing = mp.solutions.drawing_utils
        self.mp_drawing_styles = mp.solutions.drawing_styles

    def detect(self, image):
        """
        Detecta landmarks faciales en la imagen.
        Ahora soporta múltiples rostros.

        Args:
            image (numpy.ndarray): Imagen en formato BGR (OpenCV)

        Returns:
            tuple: (imagen_procesada, landmarks, info)
                - imagen_procesada: imagen con landmarks dibujados
                - landmarks: lista de objetos landmarks de MediaPipe (múltiples rostros)
                - info: diccionario con información de detección
        """
        # Convertir BGR a RGB para MediaPipe
        imagen_rgb = cv2.cvtColor(image, cv2.COLOR_BGR2RGB)

        # Procesar la imagen
        resultados = self.face_mesh.process(imagen_rgb)

        # Crear copia para dibujar
        imagen_con_puntos = image.copy()

        info = {
            "rostros_detectados": 0,
            "total_landmarks": 0,
            "deteccion_exitosa": False
        }

        # Si se detectaron rostros
        if resultados.multi_face_landmarks:
            info["rostros_detectados"] = len(resultados.multi_face_landmarks)
            info["deteccion_exitosa"] = True

            # Calcular total de landmarks de todos los rostros
            total_landmarks = sum(len(rostro.landmark) for rostro in resultados.multi_face_landmarks)
            info["total_landmarks"] = total_landmarks

            # Dibujar landmarks para todos los rostros detectados
            alto, ancho = image.shape[:2]

            for rostro in resultados.multi_face_landmarks:
                for punto in rostro.landmark:
                    coord_x_pixel = int(punto.x * ancho)
                    coord_y_pixel = int(punto.y * alto)

                    cv2.circle(
                        imagen_con_puntos,
                        (coord_x_pixel, coord_y_pixel),
                        LANDMARK_RADIUS,
                        LANDMARK_COLOR,
                        LANDMARK_THICKNESS
                    )

            # Retornar todos los rostros para visualización completa
            return imagen_con_puntos, resultados.multi_face_landmarks, info

        # No se detectó rostro
        return imagen_con_puntos, None, info

    def close(self):
        """Libera recursos del detector."""
        self.face_mesh.close()