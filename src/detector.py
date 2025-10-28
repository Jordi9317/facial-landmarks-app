# src/detector.py
"""
Detector de landmarks faciales usando OpenCV Haar Cascades (compatible con Python 3.13+).
"""

import cv2
import numpy as np
from .config import LANDMARK_COLOR, LANDMARK_RADIUS, LANDMARK_THICKNESS


class FaceLandmarkDetector:
    """
    Clase para detectar y visualizar landmarks faciales usando OpenCV Haar Cascades.
    Implementa una solución simplificada con puntos de referencia básicos.
    """

    def __init__(self):
        """Inicializa el detector de OpenCV."""
        # Cargar clasificadores Haar para rostros y ojos
        cascade_path = cv2.data.haarcascades
        self.face_cascade = cv2.CascadeClassifier(
            cascade_path + 'haarcascade_frontalface_default.xml'
        )
        self.eye_cascade = cv2.CascadeClassifier(
            cascade_path + 'haarcascade_eye.xml'
        )

    def detect(self, image):
        """
        Detecta landmarks faciales básicos usando Haar Cascades.

        Args:
            image (numpy.ndarray): Imagen en formato BGR (OpenCV)

        Returns:
            tuple: (imagen_procesada, landmarks, info)
                - imagen_procesada: imagen con landmarks dibujados
                - landmarks: diccionario con coordenadas de landmarks
                - info: diccionario con información de detección
        """
        # Crear copia para dibujar
        imagen_con_puntos = image.copy()
        gray = cv2.cvtColor(image, cv2.COLOR_BGR2GRAY)

        # Detectar rostros
        faces = self.face_cascade.detectMultiScale(gray, 1.3, 5)

        info = {
            "rostros_detectados": len(faces),
            "total_landmarks": 0,
            "deteccion_exitosa": len(faces) > 0
        }

        landmarks = {}

        # Si se detectaron rostros
        if len(faces) > 0:
            # Tomar el primer rostro
            (x, y, w, h) = faces[0]

            # Región de interés para los ojos (mitad superior del rostro)
            roi_gray = gray[y:y+h//2, x:x+w]
            roi_color = imagen_con_puntos[y:y+h//2, x:x+w]

            # Detectar ojos en la región de interés
            eyes = self.eye_cascade.detectMultiScale(roi_gray, 1.1, 3)

            # Crear landmarks básicos
            landmarks = {
                'face_center': (x + w//2, y + h//2),
                'face_top': (x + w//2, y),
                'face_bottom': (x + w//2, y + h),
                'face_left': (x, y + h//2),
                'face_right': (x + w, y + h//2),
                'eyes': []
            }

            # Agregar ojos detectados
            for (ex, ey, ew, eh) in eyes[:2]:  # Máximo 2 ojos
                eye_center = (x + ex + ew//2, y + ey + eh//2)
                landmarks['eyes'].append(eye_center)

            # Calcular landmarks adicionales basados en proporciones faciales
            face_height = h
            face_width = w

            # Nariz (aproximadamente en el centro horizontal, 2/3 desde arriba)
            nose_y = y + int(face_height * 0.6)
            nose_x = x + face_width // 2
            landmarks['nose'] = (nose_x, nose_y)

            # Boca (aproximadamente en el centro horizontal, 4/5 desde arriba)
            mouth_y = y + int(face_height * 0.8)
            mouth_x = x + face_width // 2
            landmarks['mouth'] = (mouth_x, mouth_y)

            # Contar landmarks
            total_landmarks = len([item for sublist in landmarks.values()
                                 if isinstance(sublist, list) for item in sublist]) + \
                             len([item for item in landmarks.values()
                                 if not isinstance(item, list)])
            info["total_landmarks"] = total_landmarks

            # Dibujar landmarks
            for key, value in landmarks.items():
                if isinstance(value, list):
                    for point in value:
                        cv2.circle(imagen_con_puntos, point, LANDMARK_RADIUS,
                                 LANDMARK_COLOR, LANDMARK_THICKNESS)
                else:
                    cv2.circle(imagen_con_puntos, value, LANDMARK_RADIUS,
                             LANDMARK_COLOR, LANDMARK_THICKNESS)

        return imagen_con_puntos, landmarks, info

    def close(self):
        """Libera recursos del detector."""
        pass