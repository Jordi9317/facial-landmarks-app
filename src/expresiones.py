# src/expresiones.py
"""
Cálculo de métricas y análisis de expresiones faciales.
"""

import math


class FacialExpressionAnalyzer:
    """
    Clase para analizar expresiones faciales basadas en landmarks.
    """

    def __init__(self):
        # Mapeo de landmarks básicos de OpenCV Haar Cascades
        self.LEFT_EYE = 'left_eye'
        self.RIGHT_EYE = 'right_eye'
        self.NOSE = 'nose'
        self.MOUTH = 'mouth'
        self.FACE_CENTER = 'face_center'

    def calcular_apertura_boca(self, face_landmarks, alto, ancho):
        """
        Calcula la apertura de la boca usando MediaPipe Face Mesh.

        Args:
            face_landmarks: Objeto NormalizedLandmarkList de MediaPipe
            alto (int): Alto de la imagen
            ancho (int): Ancho de la imagen

        Returns:
            float: Distancia normalizada entre labio superior e inferior
        """
        if not face_landmarks:
            return 0.0

        # Landmarks de la boca en MediaPipe Face Mesh
        # 13: labio superior, 14: labio inferior
        upper_lip = face_landmarks.landmark[13]
        lower_lip = face_landmarks.landmark[14]

        # Calcular distancia vertical normalizada
        apertura = abs(upper_lip.y - lower_lip.y)
        return apertura

    def calcular_apertura_ojos(self, face_landmarks, alto, ancho):
        """
        Calcula la apertura de ambos ojos usando MediaPipe Face Mesh.

        Args:
            face_landmarks: Objeto NormalizedLandmarkList de MediaPipe
            alto (int): Alto de la imagen
            ancho (int): Ancho de la imagen

        Returns:
            dict: {'izquierdo': float, 'derecho': float, 'promedio': float}
        """
        if not face_landmarks:
            return {'izquierdo': 0.0, 'derecho': 0.0, 'promedio': 0.0}

        # Landmarks de los ojos en MediaPipe Face Mesh
        # Ojo izquierdo: 159 (párpado superior), 145 (párpado inferior)
        # Ojo derecho: 386 (párpado superior), 374 (párpado inferior)

        left_eye_upper = face_landmarks.landmark[159]
        left_eye_lower = face_landmarks.landmark[145]
        right_eye_upper = face_landmarks.landmark[386]
        right_eye_lower = face_landmarks.landmark[374]

        # Calcular aperturas normalizadas
        left_apertura = abs(left_eye_upper.y - left_eye_lower.y)
        right_apertura = abs(right_eye_upper.y - right_eye_lower.y)
        promedio = (left_apertura + right_apertura) / 2

        return {
            'izquierdo': left_apertura,
            'derecho': right_apertura,
            'promedio': promedio
        }

    def calcular_inclinacion_cabeza(self, face_landmarks, alto, ancho):
        """
        Calcula la inclinación de la cabeza usando MediaPipe Face Mesh.

        Args:
            face_landmarks: Objeto NormalizedLandmarkList de MediaPipe
            alto (int): Alto de la imagen
            ancho (int): Ancho de la imagen

        Returns:
            float: Ángulo de inclinación en grados
        """
        if not face_landmarks:
            return 0.0

        # Usar landmarks de los ojos para calcular inclinación
        # Ojo izquierdo: 33, Ojo derecho: 263
        left_eye = face_landmarks.landmark[33]
        right_eye = face_landmarks.landmark[263]

        # Calcular ángulo usando la línea entre los ojos
        delta_y = right_eye.y - left_eye.y
        delta_x = right_eye.x - left_eye.x

        # Ángulo en radianes, convertir a grados
        angulo_radianes = math.atan2(delta_y, delta_x)
        angulo_grados = math.degrees(angulo_radianes)

        return angulo_grados

    def analizar_expresion_basica(self, face_landmarks, alto, ancho):
        """
        Análisis básico de expresión facial usando MediaPipe Face Mesh.

        Args:
            face_landmarks: Objeto NormalizedLandmarkList de MediaPipe
            alto (int): Alto de la imagen
            ancho (int): Ancho de la imagen

        Returns:
            dict: Diccionario con métricas de expresión
        """
        apertura_boca = self.calcular_apertura_boca(face_landmarks, alto, ancho)
        apertura_ojos = self.calcular_apertura_ojos(face_landmarks, alto, ancho)
        inclinacion_cabeza = self.calcular_inclinacion_cabeza(face_landmarks, alto, ancho)

        # Clasificación básica basada en métricas calculadas
        expresion = "neutral"

        if apertura_boca > 0.03:  # Umbral más alto para boca abierta
            expresion = "boca_abierta"
        elif apertura_ojos['promedio'] < 0.02:  # Umbral más bajo para ojos cerrados
            expresion = "ojos_cerrados"
        elif abs(inclinacion_cabeza) > 15:  # Umbral más alto para cabeza inclinada
            expresion = "cabeza_inclinada"

        return {
            'expresion_detectada': expresion,
            'apertura_boca': apertura_boca,
            'apertura_ojos': apertura_ojos,
            'inclinacion_cabeza': inclinacion_cabeza,
            'metricas': {
                'boca_abierta_umbral': 0.03,
                'ojos_cerrados_umbral': 0.02,
                'cabeza_inclinada_umbral': 15
            }
        }