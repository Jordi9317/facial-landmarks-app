# src/config.py
"""
Configuración del detector de landmarks faciales.
"""

# Configuración de visualización (compatible con face_recognition)
LANDMARK_COLOR = (0, 255, 0)  # Verde en BGR
LANDMARK_RADIUS = 2
LANDMARK_THICKNESS = -1  # Relleno

# Cantidad aproximada de landmarks (MediaPipe Face Mesh tiene 478 puntos)
TOTAL_LANDMARKS = 478