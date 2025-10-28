# Detector de Landmarks Faciales

Aplicación web para detectar 478 puntos clave en rostros humanos usando MediaPipe y Streamlit.

## Características

- Detección de 478 landmarks faciales
- Interfaz web interactiva
- Procesamiento en tiempo real
- Visualización antes/después
- Métricas de detección

## Tecnologías

- **MediaPipe**: Detección de landmarks
- **OpenCV**: Procesamiento de imágenes
- **Streamlit**: Framework web
- **Python 3.11+**

## Instalación Local

```bash
# Clonar repositorio
git clone https://github.com/tu-usuario/facial-landmarks-app.git
cd facial-landmarks-app

# Crear entorno virtual
python -m venv venv
venv\Scripts\activate  # Windows
source venv/bin/activate  # Linux/Mac

# Instalar dependencias
pip install -r requirements.txt

# Ejecutar aplicación
streamlit run app.py
```

## Deployment en Streamlit Community Cloud

1. Subir el código a GitHub
2. Ir a [https://share.streamlit.io](https://share.streamlit.io)
3. Conectar tu repositorio
4. Configurar el archivo principal como `app.py`
5. Deploy

Tu app estará disponible en: `https://tu-usuario-facial-landmarks-app.streamlit.app`

## Estructura del Proyecto

```
facial-landmarks-app/
├── src/
│   ├── __init__.py
│   ├── detector.py      # Lógica de detección
│   ├── utils.py         # Funciones auxiliares
│   └── config.py        # Configuración
├── app.py               # Aplicación Streamlit
├── requirements.txt     # Dependencias
├── .gitignore          # Archivos ignorados
└── README.md           # Documentación
```

## Documentación

- [MediaPipe Face Landmarker](https://ai.google.dev/edge/mediapipe/solutions/vision/face_landmarker)
- [Streamlit Docs](https://docs.streamlit.io)

## Autor

Desarrollado como parte del Laboratorio 2 - IFTS24
Materia: Procesamiento Digital de Imágenes

## Licencia

MIT License