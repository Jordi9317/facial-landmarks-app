# src/visualizacion.py
"""
Módulo para visualización de landmarks faciales con diferentes estilos.
Compatible con MediaPipe Face Mesh.
"""

import cv2
import mediapipe as mp
from .config import LANDMARK_COLOR, LANDMARK_RADIUS, LANDMARK_THICKNESS


class FaceLandmarkVisualizer:
    """
    Clase para visualizar landmarks faciales con diferentes estilos.
    Compatible con MediaPipe Face Mesh.
    """

    def __init__(self):
        """Inicializa el visualizador."""
        self.mp_drawing = mp.solutions.drawing_utils
        self.mp_face_mesh = mp.solutions.face_mesh

    def draw_points_only(self, image, face_landmarks):
        """
        Dibuja solo los puntos de landmarks usando MediaPipe.

        Args:
            image (numpy.ndarray): Imagen donde dibujar
            face_landmarks: Objeto NormalizedLandmarkList de MediaPipe

        Returns:
            numpy.ndarray: Imagen con puntos dibujados
        """
        image_copy = image.copy()

        if face_landmarks:
            # Dibujar todos los landmarks como puntos simples
            for landmark in face_landmarks.landmark:
                x = int(landmark.x * image.shape[1])
                y = int(landmark.y * image.shape[0])
                cv2.circle(image_copy, (x, y), LANDMARK_RADIUS,
                          LANDMARK_COLOR, LANDMARK_THICKNESS)

        return image_copy

    def draw_mesh_tesselation(self, image, face_landmarks):
        """
        Dibuja la malla de teselación completa usando MediaPipe.

        Args:
            image (numpy.ndarray): Imagen donde dibujar
            face_landmarks: Objeto NormalizedLandmarkList de MediaPipe

        Returns:
            numpy.ndarray: Imagen con malla de teselación dibujada
        """
        image_copy = image.copy()

        if face_landmarks:
            # Dibujar la malla de teselación completa
            self.mp_drawing.draw_landmarks(
                image=image_copy,
                landmark_list=face_landmarks,
                connections=self.mp_face_mesh.FACEMESH_TESSELATION,
                landmark_drawing_spec=None,  # No dibujar puntos individuales
                connection_drawing_spec=self.mp_drawing.DrawingSpec(
                    color=LANDMARK_COLOR, thickness=1
                )
            )

        return image_copy

    def create_heatmap_overlay(self, image, face_landmarks):
        """
        Crea un mapa de calor superpuesto sobre la imagen basado en la densidad de landmarks.

        Args:
            image (numpy.ndarray): Imagen donde dibujar
            face_landmarks: Objeto NormalizedLandmarkList de MediaPipe

        Returns:
            numpy.ndarray: Imagen con mapa de calor superpuesto
        """
        import numpy as np

        image_copy = image.copy()
        height, width = image.shape[:2]

        # Crear mapa de calor vacío
        heatmap = np.zeros((height, width), dtype=np.float32)

        if face_landmarks:
            # Agregar puntos al mapa de calor con un radio de influencia
            for landmark in face_landmarks.landmark:
                x = int(landmark.x * width)
                y = int(landmark.y * height)
                if 0 <= x < width and 0 <= y < height:
                    # Crear un círculo de influencia alrededor de cada punto
                    cv2.circle(heatmap, (x, y), 20, 1.0, -1)  # Radio 20, valor 1.0

        # Normalizar el mapa de calor
        if heatmap.max() > 0:
            heatmap = heatmap / heatmap.max()

        # Aplicar colormap
        heatmap_colored = cv2.applyColorMap((heatmap * 255).astype(np.uint8), cv2.COLORMAP_JET)

        # Superponer el mapa de calor sobre la imagen original
        alpha = 0.5  # Transparencia
        image_copy = cv2.addWeighted(image_copy, 1 - alpha, heatmap_colored, alpha, 0)

        return image_copy

    def draw_contours_only(self, image, face_landmarks):
        """
        Dibuja solo los contornos principales usando MediaPipe.

        Args:
            image (numpy.ndarray): Imagen donde dibujar
            face_landmarks: Objeto NormalizedLandmarkList de MediaPipe

        Returns:
            numpy.ndarray: Imagen con contornos dibujados
        """
        image_copy = image.copy()

        if face_landmarks:
            # Dibujar solo los contornos principales (ojos, boca, contorno facial)
            self.mp_drawing.draw_landmarks(
                image=image_copy,
                landmark_list=face_landmarks,
                connections=self.mp_face_mesh.FACEMESH_CONTOURS,
                landmark_drawing_spec=None,  # No dibujar puntos individuales
                connection_drawing_spec=self.mp_drawing.DrawingSpec(
                    color=LANDMARK_COLOR, thickness=3
                )
            )

        return image_copy