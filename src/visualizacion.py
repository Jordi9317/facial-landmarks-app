# src/visualizacion.py
"""
Módulo para visualización de landmarks faciales con diferentes estilos.
Compatible con OpenCV Haar Cascades.
"""

import cv2
from .config import LANDMARK_COLOR, LANDMARK_RADIUS, LANDMARK_THICKNESS


class FaceLandmarkVisualizer:
    """
    Clase para visualizar landmarks faciales con diferentes estilos.
    Compatible con OpenCV Haar Cascades.
    """

    def __init__(self):
        """Inicializa el visualizador."""
        pass

    def draw_points_only(self, image, landmarks):
        """
        Dibuja solo los puntos de landmarks.

        Args:
            image (numpy.ndarray): Imagen donde dibujar
            landmarks: Diccionario de coordenadas de landmarks

        Returns:
            numpy.ndarray: Imagen con puntos dibujados
        """
        image_copy = image.copy()

        # Dibujar landmarks del diccionario
        for key, value in landmarks.items():
            if isinstance(value, list):
                for point in value:
                    cv2.circle(image_copy, point, LANDMARK_RADIUS,
                             LANDMARK_COLOR, LANDMARK_THICKNESS)
            else:
                cv2.circle(image_copy, value, LANDMARK_RADIUS,
                         LANDMARK_COLOR, LANDMARK_THICKNESS)

        return image_copy

    def draw_mesh_tesselation(self, image, landmarks):
        """
        Dibuja conexiones simples entre landmarks principales.

        Args:
            image (numpy.ndarray): Imagen donde dibujar
            landmarks: Diccionario de coordenadas de landmarks

        Returns:
            numpy.ndarray: Imagen con conexiones dibujadas
        """
        image_copy = image.copy()

        # Dibujar líneas conectando puntos principales
        if 'face_left' in landmarks and 'face_right' in landmarks:
            cv2.line(image_copy, landmarks['face_left'], landmarks['face_right'],
                    LANDMARK_COLOR, 2)

        if 'face_top' in landmarks and 'face_bottom' in landmarks:
            cv2.line(image_copy, landmarks['face_top'], landmarks['face_bottom'],
                    LANDMARK_COLOR, 2)

        # Conectar ojos si existen
        if 'eyes' in landmarks and len(landmarks['eyes']) >= 2:
            eye1, eye2 = landmarks['eyes'][:2]
            cv2.line(image_copy, eye1, eye2, LANDMARK_COLOR, 2)

        # Dibujar puntos también
        image_copy = self.draw_points_only(image_copy, landmarks)

        return image_copy

    def draw_contours_only(self, image, landmarks):
        """
        Dibuja solo el contorno facial básico.

        Args:
            image (numpy.ndarray): Imagen donde dibujar
            landmarks: Diccionario de coordenadas de landmarks

        Returns:
            numpy.ndarray: Imagen con contorno dibujado
        """
        image_copy = image.copy()

        # Dibujar solo los puntos del contorno facial
        contour_points = ['face_top', 'face_right', 'face_bottom', 'face_left']
        points_to_draw = {}

        for point_name in contour_points:
            if point_name in landmarks:
                points_to_draw[point_name] = landmarks[point_name]

        # Dibujar conexiones del contorno
        if len(points_to_draw) >= 4:
            # Crear lista ordenada de puntos para el contorno
            ordered_points = [
                points_to_draw['face_top'],
                points_to_draw['face_right'],
                points_to_draw['face_bottom'],
                points_to_draw['face_left']
            ]

            # Dibujar líneas conectando los puntos del contorno
            for i in range(len(ordered_points)):
                start_point = ordered_points[i]
                end_point = ordered_points[(i + 1) % len(ordered_points)]
                cv2.line(image_copy, start_point, end_point, LANDMARK_COLOR, 3)

        # Dibujar puntos del contorno
        for point in points_to_draw.values():
            cv2.circle(image_copy, point, LANDMARK_RADIUS + 2,
                     LANDMARK_COLOR, LANDMARK_THICKNESS)

        return image_copy