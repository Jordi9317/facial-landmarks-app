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
        # Mapeo de features de face_recognition a índices para expresiones
        # face_recognition landmarks están organizados por features
        self.LEFT_EYE = 'left_eye'
        self.RIGHT_EYE = 'right_eye'
        self.TOP_LIP = 'top_lip'
        self.BOTTOM_LIP = 'bottom_lip'
        self.NOSE_BRIDGE = 'nose_bridge'

    def calcular_apertura_boca(self, landmarks, alto, ancho):
        """
        Calcula la apertura de la boca (distancia entre labios).
        Compatible con face_recognition landmarks.

        Args:
            landmarks: Diccionario de landmarks de face_recognition
            alto (int): Alto de la imagen
            ancho (int): Ancho de la imagen

        Returns:
            float: Distancia en píxeles entre labio superior e inferior
        """
        if self.TOP_LIP not in landmarks or self.BOTTOM_LIP not in landmarks:
            return 0.0

        # Calcular punto medio del labio superior
        top_lip_points = landmarks[self.TOP_LIP]
        top_y = sum(point[1] for point in top_lip_points) / len(top_lip_points)

        # Calcular punto medio del labio inferior
        bottom_lip_points = landmarks[self.BOTTOM_LIP]
        bottom_y = sum(point[1] for point in bottom_lip_points) / len(bottom_lip_points)

        distancia = abs(bottom_y - top_y)
        return distancia

    def calcular_apertura_ojos(self, landmarks, alto, ancho):
        """
        Calcula la apertura de ambos ojos.
        Compatible con face_recognition landmarks.

        Args:
            landmarks: Diccionario de landmarks de face_recognition
            alto (int): Alto de la imagen
            ancho (int): Ancho de la imagen

        Returns:
            dict: {'izquierdo': float, 'derecho': float, 'promedio': float}
        """
        apertura_izquierdo = 0.0
        apertura_derecho = 0.0

        # Calcular apertura del ojo izquierdo
        if self.LEFT_EYE in landmarks:
            left_eye_points = landmarks[self.LEFT_EYE]
            if len(left_eye_points) >= 2:
                # Distancia vertical entre puntos superior e inferior
                y_coords = [point[1] for point in left_eye_points]
                apertura_izquierdo = max(y_coords) - min(y_coords)

        # Calcular apertura del ojo derecho
        if self.RIGHT_EYE in landmarks:
            right_eye_points = landmarks[self.RIGHT_EYE]
            if len(right_eye_points) >= 2:
                # Distancia vertical entre puntos superior e inferior
                y_coords = [point[1] for point in right_eye_points]
                apertura_derecho = max(y_coords) - min(y_coords)

        promedio = (apertura_izquierdo + apertura_derecho) / 2

        return {
            'izquierdo': apertura_izquierdo,
            'derecho': apertura_derecho,
            'promedio': promedio
        }

    def calcular_inclinacion_cabeza(self, landmarks, alto, ancho):
        """
        Calcula la inclinación de la cabeza usando landmarks de la nariz.
        Compatible con face_recognition landmarks.

        Args:
            landmarks: Diccionario de landmarks de face_recognition
            alto (int): Alto de la imagen
            ancho (int): Ancho de la imagen

        Returns:
            float: Ángulo de inclinación en grados (aproximado)
        """
        if self.NOSE_BRIDGE not in landmarks:
            return 0.0

        nose_points = landmarks[self.NOSE_BRIDGE]
        if len(nose_points) < 2:
            return 0.0

        # Calcular ángulo usando los puntos del puente de la nariz
        # Punto superior e inferior del puente nasal
        top_point = nose_points[0]  # Punto superior
        bottom_point = nose_points[-1]  # Punto inferior

        delta_x = bottom_point[0] - top_point[0]
        delta_y = bottom_point[1] - top_point[1]

        # Calcular ángulo usando atan2
        angulo_radianes = math.atan2(delta_y, delta_x)
        angulo_grados = math.degrees(angulo_radianes)

        return angulo_grados

    def analizar_expresion_basica(self, landmarks, alto, ancho):
        """
        Análisis básico de expresión facial.

        Args:
            landmarks: Objeto landmarks de MediaPipe
            alto (int): Alto de la imagen
            ancho (int): Ancho de la imagen

        Returns:
            dict: Diccionario con métricas de expresión
        """
        apertura_boca = self.calcular_apertura_boca(landmarks, alto, ancho)
        apertura_ojos = self.calcular_apertura_ojos(landmarks, alto, ancho)
        inclinacion_cabeza = self.calcular_inclinacion_cabeza(landmarks, alto, ancho)

        # Clasificación básica (muy simplificada)
        expresion = "neutral"

        if apertura_boca > 20:  # Umbral arbitrario
            expresion = "boca_abierta"
        elif apertura_ojos['promedio'] < 5:  # Umbral arbitrario
            expresion = "ojos_cerrados"
        elif abs(inclinacion_cabeza) > 15:  # Umbral arbitrario
            expresion = "cabeza_inclinada"

        return {
            'expresion_detectada': expresion,
            'apertura_boca': apertura_boca,
            'apertura_ojos': apertura_ojos,
            'inclinacion_cabeza': inclinacion_cabeza,
            'metricas': {
                'boca_abierta_umbral': 20,
                'ojos_cerrados_umbral': 5,
                'cabeza_inclinada_umbral': 15
            }
        }