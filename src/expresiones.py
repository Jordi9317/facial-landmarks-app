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

    def calcular_apertura_boca(self, landmarks, alto, ancho):
        """
        Calcula la apertura de la boca usando landmarks básicos de OpenCV.

        Args:
            landmarks: Diccionario de landmarks de OpenCV Haar Cascades
            alto (int): Alto de la imagen
            ancho (int): Ancho de la imagen

        Returns:
            float: Distancia aproximada (siempre 0 ya que no tenemos landmarks de boca precisos)
        """
        # Con Haar Cascades no podemos calcular apertura de boca precisa
        # Retornamos 0 como indicador de que no está disponible
        return 0.0

    def calcular_apertura_ojos(self, landmarks, alto, ancho):
        """
        Calcula la apertura de ambos ojos usando Haar Cascades.
        Como no tenemos landmarks precisos de ojos, retornamos valores aproximados.

        Args:
            landmarks: Diccionario de landmarks de OpenCV Haar Cascades
            alto (int): Alto de la imagen
            ancho (int): Ancho de la imagen

        Returns:
            dict: {'izquierdo': float, 'derecho': float, 'promedio': float}
        """
        # Contar ojos detectados
        num_eyes = len(landmarks.get('eyes', []))

        # Valores aproximados basados en detección de ojos
        eye_apertura = 15.0 if num_eyes >= 2 else 10.0  # Valor aproximado en píxeles

        return {
            'izquierdo': eye_apertura if num_eyes >= 1 else 0.0,
            'derecho': eye_apertura if num_eyes >= 2 else 0.0,
            'promedio': eye_apertura if num_eyes >= 1 else 0.0
        }

    def calcular_inclinacion_cabeza(self, landmarks, alto, ancho):
        """
        Calcula la inclinación de la cabeza usando landmarks básicos de OpenCV.

        Args:
            landmarks: Diccionario de landmarks de OpenCV Haar Cascades
            alto (int): Alto de la imagen
            ancho (int): Ancho de la imagen

        Returns:
            float: Ángulo de inclinación en grados (siempre 0 ya que no podemos calcularlo con precisión)
        """
        # Con Haar Cascades no podemos calcular inclinación precisa
        return 0.0

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