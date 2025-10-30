# app.py
"""
Aplicación Streamlit para detección de landmarks faciales.
"""

import streamlit as st
from PIL import Image
from src.detector import FaceLandmarkDetector
from src.visualizacion import FaceLandmarkVisualizer
from src.expresiones import FacialExpressionAnalyzer
from src.exportacion import (
    export_landmarks_json,
    export_landmarks_csv,
    export_expressions_json,
    create_download_link
)
from src.utils import pil_to_cv2, cv2_to_pil, resize_image
from src.config import TOTAL_LANDMARKS

# Configuración de la página
st.set_page_config(
    page_title="Detector de Landmarks Faciales",
    layout="wide"
)

# Título y descripción
st.title("Detector de Landmarks Faciales")
st.markdown("""
Esta aplicación detecta **478 puntos clave** en rostros humanos usando MediaPipe Face Mesh.
Subí una imagen con un rostro y mirá la magia de la visión por computadora.
""")

# Sidebar con información y controles
with st.sidebar:
    st.header("Información")
    st.markdown("""
    ### ¿Qué son los Landmarks?
    Son puntos de referencia que mapean:
    - 478 puntos precisos por rostro usando MediaPipe
    - Ojos, cejas, nariz, boca, contorno facial
    - Coordenadas 3D (x, y, z) normalizadas
    - Alta precisión para análisis facial detallado
    """)

    st.divider()

    # Controles de visualización
    st.header("🎨 Estilo de Visualización")
    visualization_style = st.selectbox(
        "Elegí el estilo de dibujo:",
        ["Puntos Simples", "Malla Conectada", "Contornos Principales", "Heatmap"],
        help="Diferentes formas de mostrar los landmarks detectados"
    )

    st.header("📊 Análisis de Expresiones")
    analyze_expressions = st.checkbox(
        "Analizar expresiones faciales",
        help="Calcula métricas como apertura de boca, ojos y inclinación de cabeza"
    )

    st.header("💾 Exportación de Datos")
    export_format = st.selectbox(
        "Formato de exportación:",
        ["JSON", "CSV"],
        help="Formato para descargar las coordenadas de landmarks"
    )

    st.divider()
    st.caption("Desarrollado en el Laboratorio 2 - IFTS24")

# Uploader de imagen
uploaded_file = st.file_uploader(
    "📤 Subí una imagen con un rostro",
    type=["jpg", "jpeg", "png"],
    help="Formatos aceptados: JPG, JPEG, PNG"
)

if uploaded_file is not None:
    # Cargar imagen
    imagen_original = Image.open(uploaded_file)

    # Convertir a formato OpenCV
    imagen_cv2 = pil_to_cv2(imagen_original)

    # Redimensionar si es muy grande
    imagen_cv2 = resize_image(imagen_cv2, max_width=800)

    # Columnas para mostrar antes/después
    col1, col2 = st.columns(2)

    with col1:
        st.subheader("🖼️ Imagen Original")
        st.image(cv2_to_pil(imagen_cv2), use_column_width=True)

    # Detectar landmarks
    with st.spinner("🔍 Detectando landmarks faciales..."):
        detector = FaceLandmarkDetector()
        imagen_procesada, landmarks, info = detector.detect(imagen_cv2)
        detector.close()

    # Aplicar estilo de visualización seleccionado
    if info["deteccion_exitosa"] and landmarks:
        visualizer = FaceLandmarkVisualizer()

        # Tomar el primer rostro para visualización
        primer_rostro = landmarks[0] if isinstance(landmarks, list) else landmarks

        if visualization_style == "Puntos Simples":
            imagen_visualizada = visualizer.draw_points_only(imagen_cv2, primer_rostro)
        elif visualization_style == "Malla Conectada":
            imagen_visualizada = visualizer.draw_mesh_tesselation(imagen_cv2, primer_rostro)
        elif visualization_style == "Contornos Principales":
            imagen_visualizada = visualizer.draw_contours_only(imagen_cv2, primer_rostro)
        elif visualization_style == "Heatmap":
            imagen_visualizada = visualizer.create_heatmap_overlay(imagen_cv2, primer_rostro)
        else:
            imagen_visualizada = imagen_procesada  # Fallback
    else:
        imagen_visualizada = imagen_procesada

    with col2:
        st.subheader(f"🎨 Landmarks - {visualization_style}")
        st.image(cv2_to_pil(imagen_visualizada), use_column_width=True)

    # Mostrar información de detección
    st.divider()

    if info["deteccion_exitosa"]:
        st.success("✅ Detección exitosa")

        # Métricas principales
        metric_col1, metric_col2, metric_col3 = st.columns(3)

        with metric_col1:
            st.metric("👤 Rostros detectados", info["rostros_detectados"])

        with metric_col2:
            st.metric("📍 Landmarks detectados", f"{info['total_landmarks']}/{TOTAL_LANDMARKS}")

        with metric_col3:
            porcentaje = (info['total_landmarks'] / TOTAL_LANDMARKS) * 100
            st.metric("🎯 Precisión", f"{porcentaje:.1f}%")

        # Análisis de expresiones (si está habilitado)
        if analyze_expressions and landmarks:
            st.header("😊 Análisis de Expresiones")

            analyzer = FacialExpressionAnalyzer()
            # Tomar el primer rostro para análisis de expresiones
            primer_rostro = landmarks[0] if isinstance(landmarks, list) and landmarks else None
            if primer_rostro:
                expresion_data = analyzer.analizar_expresion_basica(primer_rostro, imagen_cv2.shape[0], imagen_cv2.shape[1])

            # Mostrar métricas de expresión
            exp_col1, exp_col2, exp_col3 = st.columns(3)

            with exp_col1:
                st.metric("👄 Apertura Boca", f"{expresion_data['apertura_boca']:.3f}")

            with exp_col2:
                st.metric("👁️ Apertura Ojos", f"{expresion_data['apertura_ojos']['promedio']:.3f}")

            with exp_col3:
                st.metric("📐 Inclinación Cabeza", f"{expresion_data['inclinacion_cabeza']:.3f}°")

            # Clasificación de expresión
            st.info(f"**Expresión detectada:** {expresion_data['expresion_detectada'].replace('_', ' ').title()}")

            # Exportar datos de expresiones
            expressions_json, expr_filename = export_expressions_json(expresion_data)
            st.download_button(
                label="📊 Descargar Análisis de Expresiones (JSON)",
                data=expressions_json,
                file_name=expr_filename,
                mime="application/json",
                key="download_expressions"
            )

        # Exportación de landmarks
        st.header("💾 Exportar Datos")

        if export_format == "JSON":
            landmarks_data, filename = export_landmarks_json(landmarks, imagen_cv2.shape[0], imagen_cv2.shape[1])
            mime_type = "application/json"
        else:  # CSV
            landmarks_data, filename = export_landmarks_csv(landmarks, imagen_cv2.shape[0], imagen_cv2.shape[1])
            mime_type = "text/csv"

        st.download_button(
            label=f"📍 Descargar Landmarks ({export_format})",
            data=landmarks_data,
            file_name=filename,
            mime=mime_type,
            key=f"download_landmarks_{export_format.lower()}"
        )

    else:
        st.error("❌ No se detectó ningún rostro en la imagen")
        st.info("""
        **💡 Consejos para mejorar la detección:**
        - Asegurate de que el rostro esté bien iluminado
        - El rostro debe estar mirando hacia la cámara
        - Probá con una imagen de mayor calidad
        - Evitá ángulos extremos o rostros parcialmente ocultos
        """)

else:
    # Mensaje de bienvenida
    st.info("📤 Subí una imagen para comenzar la detección")

    # Información sobre estilos de visualización
    st.header("🎨 Estilos de Visualización Disponibles")

    viz_col1, viz_col2 = st.columns(2)

    with viz_col1:
        st.subheader("Puntos Simples")
        st.write("Visualización básica con puntos verdes")
        st.subheader("Malla Conectada")
        st.write("Puntos conectados formando una malla 3D")

    with viz_col2:
        st.subheader("Contornos Principales")
        st.write("Solo ojos, boca y contorno facial")
        st.subheader("Heatmap")
        st.write("Mapa de calor de densidad de puntos")

    # Información sobre funcionalidades
    st.markdown("### 🎯 Funcionalidades Disponibles")

    col_demo1, col_demo2 = st.columns(2)

    with col_demo1:
        st.markdown("**🔍 Detección Avanzada**")
        st.write("• Hasta 5 rostros simultáneamente")
        st.write("• 478 landmarks por rostro")
        st.write("• Precisión MediaPipe Face Mesh")

        st.markdown("**🎨 Visualización Múltiple**")
        st.write("• Puntos simples")
        st.write("• Malla conectada")
        st.write("• Contornos principales")
        st.write("• Mapa de calor")

    with col_demo2:
        st.markdown("**😊 Análisis de Expresiones**")
        st.write("• Apertura de boca")
        st.write("• Apertura de ojos")
        st.write("• Inclinación de cabeza")

        st.markdown("**💾 Exportación de Datos**")
        st.write("• Formato JSON completo")
        st.write("• CSV tabular")
        st.write("• Metadatos incluidos")