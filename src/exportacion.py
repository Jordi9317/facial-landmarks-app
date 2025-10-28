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
    Soporta múltiples rostros.

    Args:
        landmarks: Lista de objetos landmarks de MediaPipe o objeto único
        alto (int): Alto de la imagen
        ancho (int): Ancho de la imagen

    Returns:
        list: Lista de diccionarios con datos de cada landmark
    """
    data = []

    # Si es una lista de rostros (múltiples), procesar todos
    if isinstance(landmarks, list):
        rostros = landmarks
    else:
        # Si es un solo rostro, convertirlo en lista
        rostros = [landmarks] if landmarks else []

    for rostro_idx, rostro in enumerate(rostros):
        for idx, punto in enumerate(rostro.landmark):
            data.append({
                "rostro_id": rostro_idx,
                "landmark_id": idx,
                "x": punto.x * ancho,
                "y": punto.y * alto,
                "z": punto.z,
                "x_normalizado": punto.x,
                "y_normalizado": punto.y,
                "visibilidad": getattr(punto, 'visibility', 1.0)  # Algunos modelos tienen visibilidad
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
    Crea un enlace de descarga para Streamlit.

    Args:
        data (str): Datos a descargar
        filename (str): Nombre del archivo
        mime_type (str): Tipo MIME del archivo
        label (str): Etiqueta del botón

    Returns:
        streamlit download_button
    """
    import streamlit as st

    return st.download_button(
        label=label,
        data=data,
        file_name=filename,
        mime=mime_type,
        key=f"download_{filename}_{datetime.now().timestamp()}"
    )