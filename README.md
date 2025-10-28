# Detector de Landmarks Faciales

Aplicación web para detectar 478 puntos clave en rostros humanos usando MediaPipe Face Mesh y Streamlit.

## Características

- ✅ Detección de 478 landmarks faciales con MediaPipe
- ✅ Interfaz web interactiva con Streamlit
- ✅ 4 estilos de visualización: Puntos simples, Malla conectada, Contornos principales, Heatmap
- ✅ Análisis de expresiones faciales (apertura boca, ojos, inclinación cabeza)
- ✅ Exportación de datos a JSON y CSV
- ✅ Procesamiento en tiempo real
- ✅ Compatible con Streamlit Cloud

## Tecnologías

- **MediaPipe Face Mesh**: Detección precisa de 478 landmarks
- **OpenCV**: Procesamiento de imágenes
- **Streamlit**: Framework web
- **Python 3.13.9** (compatible con Streamlit Cloud)

## 🚀 Instalación y Uso

### Opción 1: Ejecutar Localmente

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

### Opción 2: Streamlit Cloud (Recomendado)

1. **Subir código a GitHub**
   - Crear repositorio público en GitHub
   - Subir todos los archivos del proyecto

2. **Deploy en Streamlit Cloud**
   - Ir a [https://share.streamlit.io](https://share.streamlit.io)
   - Conectar tu repositorio de GitHub
   - Configurar `app.py` como archivo principal
   - Hacer clic en "Deploy"

3. **¡Listo!** Tu app estará disponible en una URL como:
   `https://tu-usuario-facial-landmarks-app.streamlit.app`

## 📁 Estructura del Proyecto

```
facial-landmarks-app/
├── src/
│   ├── __init__.py
│   ├── detector.py          # Detección con MediaPipe Face Mesh
│   ├── visualizacion.py     # 4 estilos de visualización
│   ├── expresiones.py       # Análisis de expresiones faciales
│   ├── exportacion.py       # Exportación JSON/CSV
│   ├── utils.py            # Funciones auxiliares
│   └── config.py           # Configuración
├── app.py                   # Aplicación Streamlit principal
├── requirements.txt         # Dependencias Python
├── README.md               # Esta documentación
└── .gitignore             # Archivos ignorados por Git
```

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

## 📖 Uso de la Aplicación

1. **Subir imagen**: Haz clic en "📤 Subí una imagen con un rostro" y selecciona una imagen JPG/PNG
2. **Seleccionar estilo**: Elige entre 4 opciones de visualización en el sidebar
3. **Ver resultados**: Observa la detección de 478 landmarks y métricas
4. **Analizar expresiones**: Activa el checkbox para ver análisis de boca, ojos y cabeza
5. **Exportar datos**: Descarga coordenadas en formato JSON o CSV

## 🔧 Dependencias

```txt
streamlit>=1.28.0
opencv-python-headless>=4.8.0
pillow>=10.0.0
numpy>=1.24.0
mediapipe>=0.10.0
```

## 📚 Documentación

- [MediaPipe Face Mesh](https://ai.google.dev/edge/mediapipe/solutions/vision/face_landmarker)
- [Streamlit Documentation](https://docs.streamlit.io)
- [OpenCV Documentation](https://docs.opencv.org/)

## 👨‍💻 Autor

**Proyecto desarrollado para el Laboratorio 2 - IFTS24**
- **Materia**: Procesamiento Digital de Imágenes
- **Tecnologías**: MediaPipe, Streamlit, OpenCV
- **Python**: 3.13.9 (compatible con Streamlit Cloud)

## 📄 Licencia

Este proyecto está bajo la Licencia MIT. Ver archivo `LICENSE` para más detalles.