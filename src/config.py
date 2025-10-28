# src/config.py
"""
Configuración del detector de landmarks faciales.
"""

# Configuración de visualización (compatible con face_recognition)
LANDMARK_COLOR = (0, 255, 0)  # Verde en BGR
LANDMARK_RADIUS = 2
LANDMARK_THICKNESS = -1  # Relleno

# Cantidad aproximada de landmarks (face_recognition tiene ~68 puntos)
TOTAL_LANDMARKS = 68