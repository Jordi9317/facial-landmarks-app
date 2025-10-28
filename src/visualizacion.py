# src/visualizacion.py
"""
Funciones de visualización y estilos para landmarks faciales.
"""

import cv2
import mediapipe as mp
from .config import LANDMARK_COLOR, LANDMARK_RADIUS, LANDMARK_THICKNESS


class FaceLandmarkVisualizer:
    """
    Clase para visualizar landmarks faciales con diferentes estilos.
    """

    def __init__(self):
        self.mp_drawing = mp.solutions.drawing_utils
        self.mp_drawing_styles = mp.solutions.drawing_styles

    def draw_points_only(self, image, landmarks):
        """
        Dibuja solo los puntos de landmarks (estilo original).
        Soporta múltiples rostros.

        Args:
            image (numpy.ndarray): Imagen OpenCV
            landmarks: Lista de objetos landmarks de MediaPipe o objeto único

        Returns:
            numpy.ndarray: Imagen con puntos dibujados
        """
        image_copy = image.copy()
        alto, ancho = image.shape[:2]

        # Si es una lista de rostros (múltiples), iterar sobre cada uno
        if isinstance(landmarks, list):
            rostros = landmarks
        else:
            # Si es un solo rostro, convertirlo en lista
            rostros = [landmarks] if landmarks else []

        for rostro in rostros:
            for punto in rostro.landmark:
                coord_x_pixel = int(punto.x * ancho)
                coord_y_pixel = int(punto.y * alto)

                cv2.circle(
                    image_copy,
                    (coord_x_pixel, coord_y_pixel),
                    LANDMARK_RADIUS,
                    LANDMARK_COLOR,
                    LANDMARK_THICKNESS
                )

        return image_copy

    def draw_mesh_tesselation(self, image, landmarks):
        """
        Dibuja puntos + malla conectada (teselación).
        Soporta múltiples rostros.

        Args:
            image (numpy.ndarray): Imagen OpenCV
            landmarks: Lista de objetos landmarks de MediaPipe o objeto único

        Returns:
            numpy.ndarray: Imagen con malla dibujada
        """
        image_copy = image.copy()

        # Si es una lista de rostros (múltiples), iterar sobre cada uno
        if isinstance(landmarks, list):
            rostros = landmarks
        else:
            # Si es un solo rostro, convertirlo en lista
            rostros = [landmarks] if landmarks else []

        for rostro in rostros:
            self.mp_drawing.draw_landmarks(
                image=image_copy,
                landmark_list=rostro,
                connections=mp.solutions.face_mesh.FACEMESH_TESSELATION,
                landmark_drawing_spec=None,
                connection_drawing_spec=self.mp_drawing_styles.get_default_face_mesh_tesselation_style()
            )

        return image_copy

    def draw_contours_only(self, image, landmarks):
        """
        Dibuja solo los contornos principales (ojos, boca, rostro).
        Soporta múltiples rostros.

        Args:
            image (numpy.ndarray): Imagen OpenCV
            landmarks: Lista de objetos landmarks de MediaPipe o objeto único

        Returns:
            numpy.ndarray: Imagen con contornos dibujados
        """
        image_copy = image.copy()

        # Si es una lista de rostros (múltiples), iterar sobre cada uno
        if isinstance(landmarks, list):
            rostros = landmarks
        else:
            # Si es un solo rostro, convertirlo en lista
            rostros = [landmarks] if landmarks else []

        for rostro in rostros:
            # Dibujar contornos faciales principales
            self.mp_drawing.draw_landmarks(
                image=image_copy,
                landmark_list=rostro,
                connections=mp.solutions.face_mesh.FACEMESH_FACE_OVAL,
                landmark_drawing_spec=None,
                connection_drawing_spec=self.mp_drawing_styles.get_default_face_mesh_contours_style()
            )

            # Dibujar contornos de ojos
            self.mp_drawing.draw_landmarks(
                image=image_copy,
                landmark_list=rostro,
                connections=mp.solutions.face_mesh.FACEMESH_LEFT_EYE,
                landmark_drawing_spec=None,
                connection_drawing_spec=self.mp_drawing_styles.get_default_face_mesh_contours_style()
            )

            self.mp_drawing.draw_landmarks(
                image=image_copy,
                landmark_list=rostro,
                connections=mp.solutions.face_mesh.FACEMESH_RIGHT_EYE,
                landmark_drawing_spec=None,
                connection_drawing_spec=self.mp_drawing_styles.get_default_face_mesh_contours_style()
            )

            # Dibujar contornos de labios
            self.mp_drawing.draw_landmarks(
                image=image_copy,
                landmark_list=rostro,
                connections=mp.solutions.face_mesh.FACEMESH_LIPS,
                landmark_drawing_spec=None,
                connection_drawing_spec=self.mp_drawing_styles.get_default_face_mesh_contours_style()
            )

        return image_copy

    def create_heatmap_overlay(self, image, landmarks):
        """
        Crea una superposición de heatmap de densidad de puntos.
        Soporta múltiples rostros.

        Args:
            image (numpy.ndarray): Imagen OpenCV
            landmarks: Lista de objetos landmarks de MediaPipe o objeto único

        Returns:
            numpy.ndarray: Imagen con heatmap superpuesto
        """
        import numpy as np

        image_copy = image.copy()
        alto, ancho = image.shape[:2]

        # Crear mapa de calor vacío
        heatmap = np.zeros((alto, ancho), dtype=np.float32)

        # Si es una lista de rostros (múltiples), iterar sobre cada uno
        if isinstance(landmarks, list):
            rostros = landmarks
        else:
            # Si es un solo rostro, convertirlo en lista
            rostros = [landmarks] if landmarks else []

        # Agregar puntos al heatmap para todos los rostros
        for rostro in rostros:
            for punto in rostro.landmark:
                x = int(punto.x * ancho)
                y = int(punto.y * alto)
                if 0 <= x < ancho and 0 <= y < alto:
                    # Crear un área circular alrededor del punto
                    cv2.circle(heatmap, (x, y), 10, 1.0, -1)

        # Aplicar filtro gaussiano para suavizar
        heatmap = cv2.GaussianBlur(heatmap, (21, 21), 0)

        # Normalizar al rango 0-255
        heatmap = cv2.normalize(heatmap, None, 0, 255, cv2.NORM_MINMAX, cv2.CV_8U)

        # Aplicar mapa de colores (jet)
        heatmap_colored = cv2.applyColorMap(heatmap, cv2.COLORMAP_JET)

        # Superponer al 50% de opacidad
        overlay = cv2.addWeighted(image_copy, 0.7, heatmap_colored, 0.3, 0)

        return overlay