# src/exportacion.py
"""
Funciones para exportar datos de landmarks faciales.
"""

import json
import csv
from datetime import datetime


def landmarks_to_dict(landmarks, alto, ancho):
    """
    Convierte landmarks a formato diccionario para exportación.
    Soporta listas de objetos NormalizedLandmarkList de MediaPipe.

    Args:
        landmarks: Lista de objetos NormalizedLandmarkList de MediaPipe
        alto (int): Alto de la imagen
        ancho (int): Ancho de la imagen

    Returns:
        list: Lista de diccionarios con datos de cada landmark
    """
    data = []

    if not landmarks:
        return data

    # Procesar cada rostro detectado
    for rostro_idx, face_landmarks in enumerate(landmarks):
        # Procesar cada landmark del rostro
        for landmark_idx, landmark in enumerate(face_landmarks.landmark):
            data.append({
                "rostro_id": rostro_idx,
                "landmark_id": landmark_idx,
                "x": int(landmark.x * ancho),
                "y": int(landmark.y * alto),
                "z": landmark.z,
                "x_normalizado": landmark.x,
                "y_normalizado": landmark.y,
                "visibilidad": getattr(landmark, 'visibility', 1.0)
            })

    return data


def export_landmarks_json(landmarks, alto, ancho, filename=None):
    """
    Exporta landmarks a formato JSON.

    Args:
        landmarks: Objeto landmarks de MediaPipe
        alto (int): Alto de la imagen
        ancho (int): Ancho de la imagen
        filename (str, optional): Nombre del archivo. Si None, genera uno automático.

    Returns:
        tuple: (json_string, filename)
    """
    if filename is None:
        timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
        filename = f"landmarks_{timestamp}.json"

    data = landmarks_to_dict(landmarks, alto, ancho)

    # Agregar metadatos
    export_data = {
        "metadata": {
            "export_timestamp": datetime.now().isoformat(),
            "total_landmarks": len(data),
            "image_dimensions": {
                "width": ancho,
                "height": alto
            },
            "landmark_format": "MediaPipe Face Mesh 478 points"
        },
        "landmarks": data
    }

    json_string = json.dumps(export_data, indent=2, ensure_ascii=False)
    return json_string, filename


def export_landmarks_csv(landmarks, alto, ancho, filename=None):
    """
    Exporta landmarks a formato CSV.

    Args:
        landmarks: Objeto landmarks de MediaPipe
        alto (int): Alto de la imagen
        ancho (int): Ancho de la imagen
        filename (str, optional): Nombre del archivo. Si None, genera uno automático.

    Returns:
        tuple: (csv_string, filename)
    """
    if filename is None:
        timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
        filename = f"landmarks_{timestamp}.csv"

    data = landmarks_to_dict(landmarks, alto, ancho)

    # Crear CSV en memoria
    csv_lines = []
    csv_lines.append("rostro_id,landmark_id,x,y,z,x_normalizado,y_normalizado,visibilidad")

    for landmark in data:
        csv_lines.append(",".join([
            str(landmark["rostro_id"]),
            str(landmark["landmark_id"]),
            ".4f",
            ".4f",
            ".6f",
            ".6f",
            ".6f",
            ".3f"
        ]))

    csv_string = "\n".join(csv_lines)
    return csv_string, filename


def export_expressions_json(expression_data, filename=None):
    """
    Exporta datos de análisis de expresiones a JSON.

    Args:
        expression_data (dict): Datos de expresiones del analizador
        filename (str, optional): Nombre del archivo

    Returns:
        tuple: (json_string, filename)
    """
    if filename is None:
        timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
        filename = f"expressions_{timestamp}.json"

    export_data = {
        "metadata": {
            "export_timestamp": datetime.now().isoformat(),
            "analysis_type": "facial_expressions"
        },
        "expressions": expression_data
    }

    json_string = json.dumps(export_data, indent=2, ensure_ascii=False)
    return json_string, filename


def create_download_link(data, filename, mime_type, label):
    """
    Crea un botón de descarga para Streamlit.
    Versión corregida para evitar problemas de DOM en Streamlit Cloud.

    Args:
        data (str): Datos a descargar
        filename (str): Nombre del archivo
        mime_type (str): Tipo MIME del archivo
        label (str): Etiqueta del botón

    Returns:
        None: Renderiza directamente el botón
    """
    import streamlit as st

    # Crear clave única para evitar conflictos
    unique_key = f"download_{filename}_{hash(data) % 10000}"

    st.download_button(
        label=label,
        data=data,
        file_name=filename,
        mime=mime_type,
        key=unique_key
    )