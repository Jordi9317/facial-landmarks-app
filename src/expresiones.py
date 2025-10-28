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
        # Índices de landmarks importantes para expresiones
        self.LEFT_EYE_TOP = 159    # Párpado superior ojo izquierdo
        self.LEFT_EYE_BOTTOM = 145  # Párpado inferior ojo izquierdo
        self.RIGHT_EYE_TOP = 386   # Párpado superior ojo derecho
        self.RIGHT_EYE_BOTTOM = 374 # Párpado inferior ojo derecho

        self.UPPER_LIP = 13   # Labio superior
        self.LOWER_LIP = 14   # Labio inferior

        self.NOSE_TIP = 1     # Punta de la nariz
        self.FOREHEAD = 10    # Frente (aproximado)

    def calcular_apertura_boca(self, landmarks, alto, ancho):
        """
        Calcula la apertura de la boca (distancia entre labios).

        Args:
            landmarks: Objeto landmarks de MediaPipe
            alto (int): Alto de la imagen
            ancho (int): Ancho de la imagen

        Returns:
            float: Distancia en píxeles entre labio superior e inferior
        """
        punto_superior = landmarks.landmark[self.UPPER_LIP]
        punto_inferior = landmarks.landmark[self.LOWER_LIP]

        y_superior = punto_superior.y * alto
        y_inferior = punto_inferior.y * alto

        distancia = abs(y_inferior - y_superior)
        return distancia

    def calcular_apertura_ojos(self, landmarks, alto, ancho):
        """
        Calcula la apertura de ambos ojos.

        Args:
            landmarks: Objeto landmarks de MediaPipe
            alto (int): Alto de la imagen
            ancho (int): Ancho de la imagen

        Returns:
            dict: {'izquierdo': float, 'derecho': float, 'promedio': float}
        """
        # Ojo izquierdo
        left_top = landmarks.landmark[self.LEFT_EYE_TOP]
        left_bottom = landmarks.landmark[self.LEFT_EYE_BOTTOM]
        apertura_izquierdo = abs(left_bottom.y - left_top.y) * alto

        # Ojo derecho
        right_top = landmarks.landmark[self.RIGHT_EYE_TOP]
        right_bottom = landmarks.landmark[self.RIGHT_EYE_BOTTOM]
        apertura_derecho = abs(right_bottom.y - right_top.y) * alto

        promedio = (apertura_izquierdo + apertura_derecho) / 2

        return {
            'izquierdo': apertura_izquierdo,
            'derecho': apertura_derecho,
            'promedio': promedio
        }

    def calcular_inclinacion_cabeza(self, landmarks, alto, ancho):
        """
        Calcula la inclinación de la cabeza usando landmarks de la nariz y frente.

        Args:
            landmarks: Objeto landmarks de MediaPipe
            alto (int): Alto de la imagen
            ancho (int): Ancho de la imagen

        Returns:
            float: Ángulo de inclinación en grados (positivo = inclinado a la derecha)
        """
        # Usar puntos de la nariz y frente para calcular ángulo
        nose = landmarks.landmark[self.NOSE_TIP]
        forehead = landmarks.landmark[self.FOREHEAD]

        # Convertir a coordenadas de píxeles
        nose_x = nose.x * ancho
        nose_y = nose.y * alto
        forehead_x = forehead.x * ancho
        forehead_y = forehead.y * alto

        # Calcular ángulo usando atan2
        delta_x = forehead_x - nose_x
        delta_y = forehead_y - nose_y

        # Calcular ángulo en grados
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