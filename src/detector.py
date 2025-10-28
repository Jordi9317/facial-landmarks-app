# src/detector.py
"""
Detector de landmarks faciales usando MediaPipe Face Mesh.
"""

import cv2
import mediapipe as mp
import numpy as np
from .config import LANDMARK_COLOR, LANDMARK_RADIUS, LANDMARK_THICKNESS


class FaceLandmarkDetector:
    """
    Clase para detectar landmarks faciales usando MediaPipe Face Mesh.
    Detecta 478 landmarks por rostro con alta precisión.
    """

    def __init__(self):
        """Inicializa el detector de MediaPipe."""
        self.mp_face_mesh = mp.solutions.face_mesh
        self.face_mesh = self.mp_face_mesh.FaceMesh(
            static_image_mode=True,
            max_num_faces=5,
            min_detection_confidence=0.5,
            min_tracking_confidence=0.5
        )

    def detect(self, image):
        """
        Detecta landmarks faciales usando MediaPipe Face Mesh.

        Args:
            image (numpy.ndarray): Imagen en formato BGR (OpenCV)

        Returns:
            tuple: (imagen_procesada, landmarks, info)
                - imagen_procesada: imagen con landmarks dibujados
                - landmarks: lista de objetos landmarks de MediaPipe
                - info: diccionario con información de detección
        """
        # Crear copia para dibujar
        imagen_con_puntos = image.copy()

        # Convertir a RGB para MediaPipe
        rgb_image = cv2.cvtColor(image, cv2.COLOR_BGR2RGB)

        # Procesar con MediaPipe
        results = self.face_mesh.process(rgb_image)

        info = {
            "rostros_detectados": 0,
            "total_landmarks": 0,
            "deteccion_exitosa": False
        }

        landmarks = []

        if results.multi_face_landmarks:
            info["rostros_detectados"] = len(results.multi_face_landmarks)
            info["deteccion_exitosa"] = True
            info["total_landmarks"] = len(results.multi_face_landmarks) * 478

            # Devolver los landmarks de MediaPipe directamente
            landmarks = results.multi_face_landmarks

            # Dibujar landmarks básicos para preview
            for face_landmarks in results.multi_face_landmarks:
                for landmark in face_landmarks.landmark:
                    x = int(landmark.x * image.shape[1])
                    y = int(landmark.y * image.shape[0])
                    cv2.circle(imagen_con_puntos, (x, y), LANDMARK_RADIUS,
                              LANDMARK_COLOR, LANDMARK_THICKNESS)

        return imagen_con_puntos, landmarks, info

    def close(self):
        """Libera recursos del detector."""
        self.face_mesh.close()