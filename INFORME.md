# Informe Técnico: Detector Avanzado de Landmarks Faciales

## Procesamiento Digital de Imágenes - Laboratorio 2

**Fecha**: Octubre 2025
**Institución**: IFTS24
**Desarrollador**: Jordi Galman

---

## 1. Introducción

### ¿Qué son los Landmarks Faciales?

Los **landmarks faciales** son puntos de referencia específicos que mapean las características clave de un rostro humano en una imagen digital. Representan coordenadas (x, y, z) de puntos anatómicos importantes como esquinas de ojos, punta de nariz, comisuras de labios, y contorno mandibular.

![MediaPipe Face Mesh](https://ai.google.dev/static/mediapipe/images/solutions/face_landmarker_keypoints.png?hl=es-419)

*Figura 1: MediaPipe detecta 478 landmarks faciales distribuidos en el rostro*

### Importancia en Visión por Computadora

Los landmarks faciales son fundamentales en aplicaciones modernas de visión por computadora porque:

- **Filtros AR**: Instagram y Snapchat usan landmarks para posicionar efectos virtuales
- **Reconocimiento Facial**: Face ID de Apple analiza geometría facial para autenticación
- **Animación**: Películas como Avatar usan landmarks para captura de movimiento
- **Análisis Médico**: Detección de parálisis facial y estudios genéticos
- **UX Research**: Análisis de expresiones para testing de interfaces

---

## 2. Arquitectura del Proyecto

### Estructura General

```
facial-landmarks-app/
├── src/                          # Módulos principales
│   ├── __init__.py              # Inicialización del paquete
│   ├── config.py                # Configuración del modelo
│   ├── detector.py              # Lógica de detección MediaPipe
│   ├── visualizacion.py         # Estilos de dibujo de landmarks
│   ├── expresiones.py           # Análisis de expresiones faciales
│   ├── exportacion.py           # Exportación de datos
│   └── utils.py                 # Funciones auxiliares
├── app.py                       # Interfaz principal Streamlit
├── requirements.txt             # Dependencias del proyecto
├── packages.txt                 # Paquetes sistema para deployment
├── .gitignore                   # Archivos ignorados por Git
├── README.md                    # Documentación de uso
└── INFORME.md                   # Este documento
```

### Diagrama de Arquitectura

```
┌─────────────────┐    ┌─────────────────┐    ┌─────────────────┐
│   Interfaz      │    │   Lógica de     │    │   Procesamiento │
│   Streamlit     │◄──►│   Negocio       │◄──►│   de Imágenes   │
│   (app.py)      │    │   (src/)        │    │   (OpenCV)      │
└─────────────────┘    └─────────────────┘    └─────────────────┘
         │                       │                       │
         ▼                       ▼                       ▼
┌─────────────────┐    ┌─────────────────┐    ┌─────────────────┐
│   Visualización │    │   Exportación   │    │   Detección     │
│   Múltiple      │    │   JSON/CSV      │    │   MediaPipe     │
└─────────────────┘    └─────────────────┘    └─────────────────┘
```

### Flujo de Datos

1. **Entrada**: Usuario sube imagen vía Streamlit
2. **Procesamiento**: OpenCV convierte formato y redimensiona
3. **Detección**: MediaPipe analiza landmarks faciales
4. **Análisis**: Cálculo de métricas de expresiones (opcional)
5. **Visualización**: Renderizado según estilo seleccionado
6. **Exportación**: Datos guardados en JSON/CSV (opcional)

---

## 3. Decisiones de Diseño

### Modularización del Código

La decisión de separar la funcionalidad en múltiples archivos responde a principios de **ingeniería de software**:

#### Separación de Responsabilidades

```python
# app.py - Interfaz de usuario
# Maneja únicamente la UI de Streamlit y coordinación

# src/detector.py - Lógica de detección
# Encapsula toda la interacción con MediaPipe

# src/visualizacion.py - Renderizado
# Gestiona diferentes estilos de dibujo

# src/expresiones.py - Análisis
# Calcula métricas faciales específicas

# src/exportacion.py - Persistencia
# Maneja formatos de exportación
```

#### Beneficios de la Modularización

- **Mantenibilidad**: Cambios en visualización no afectan detección
- **Reutilización**: Módulos pueden usarse en otros proyectos
- **Testabilidad**: Cada módulo se prueba independientemente
- **Legibilidad**: Código organizado por funcionalidad
- **Colaboración**: Múltiples desarrolladores pueden trabajar en paralelo

### Elección de Tecnologías

#### MediaPipe vs OpenCV puro

```python
# MediaPipe: Modelo pre-entrenado, alta precisión
mp_face_mesh = mp.solutions.face_mesh.FaceMesh(**FACE_MESH_CONFIG)

# vs OpenCV puro: Requiere entrenamiento personalizado
# Más complejo pero potencialmente más flexible
```

**Decisión**: MediaPipe por su facilidad de uso y precisión out-of-the-box.

#### Streamlit vs Gradio

```python
# Streamlit: Más maduro, mejor para dashboards complejos
st.sidebar.selectbox("Estilo:", ["Puntos", "Malla", "Contornos"])

# vs Gradio: Más simple pero menos personalizable
# gr.Interface(fn=detect, inputs="image", outputs="image")
```

**Decisión**: Streamlit por su flexibilidad en interfaces complejas.

---

## 4. Desafíos Técnicos y Soluciones

### Error Inicial: `ModuleNotFoundError: No module named 'cv2'`

**Problema**: OpenCV no estaba instalado en el entorno virtual.

**Solución**:
```bash
# Verificar instalación
python -c "import cv2; print('OpenCV OK')"

# Instalar si falta
pip install opencv-python
```

### Conflicto de Dependencias: Protobuf

**Problema**: TensorFlow 2.20.0 requería protobuf >= 5.28.0, pero MediaPipe necesitaba protobuf 3.20.3.

**Solución**:
```bash
# Desinstalar TensorFlow conflictivo
pip uninstall tensorflow -y

# Instalar versión compatible de protobuf
pip install protobuf==3.20.3
```

### Manejo de Múltiples Rostros

**Problema**: Código original solo manejaba un rostro, pero MediaPipe puede detectar múltiples.

**Solución**: Modificar funciones para aceptar listas de rostros:

```python
# Antes: Un solo rostro
def draw_points_only(self, image, landmarks):
    for punto in landmarks.landmark:  # Error si es lista

# Después: Múltiples rostros
def draw_points_only(self, image, landmarks):
    rostros = landmarks if isinstance(landmarks, list) else [landmarks]
    for rostro in rostros:
        for punto in rostro.landmark:
```

### Errores de Streamlit: `use_container_width`

**Problema**: Streamlit depreció `use_container_width` en favor de `width='stretch'`.

**Solución**:
```python
# Antes (deprecated)
st.image(image, use_container_width=True)

# Después (correcto)
st.image(image, use_container_width=True)  # Aún funciona
# o
st.image(image, width='stretch')  # Nueva sintaxis
```

### Conversión de Tipos en Exportación

**Problema**: `landmarks_to_dict()` cambió claves pero `export_landmarks_csv()` usaba nombres antiguos.

**Solución**: Actualizar referencias de claves:

```python
# Antes
landmark["id"]  # KeyError

# Después
landmark["rostro_id"]      # ID del rostro
landmark["landmark_id"]    # ID del landmark
```

---

## 5. Uso de Kilo Code como Agente de Desarrollo

### Configuración Inicial

Kilo Code Supernova 1M fue configurado como asistente principal:

```bash
# Configuración conceptual
kilo config --model code-supernova-1m
kilo auth login
```

### Casos de Uso Principales

#### 1. Modularización del Código

**Prompt usado**:
```
Necesito convertir este código de Jupyter a módulos Python separados:
- detector.py para MediaPipe
- visualizacion.py para estilos de dibujo
- expresiones.py para métricas faciales
- exportacion.py para JSON/CSV
```

**Resultado**: Kilo generó la estructura modular completa con docstrings en español.

#### 2. Debugging de Errores

**Prompt usado**:
```
Tengo este error: AttributeError: 'list' object has no attribute 'landmark'
El error ocurre en expresiones.py línea 39.
¿Puedes identificar el problema y sugerir la solución?
```

**Resultado**: Kilo identificó que estaba pasando una lista de rostros en lugar de un solo rostro.

#### 3. Optimización de Funciones

**Prompt usado**:
```
Esta función draw_points_only solo funciona con un rostro.
¿Puedes modificarla para que soporte múltiples rostros?
```

**Resultado**: Kilo agregó lógica condicional para manejar listas de rostros.

#### 4. Generación de Documentación

**Prompt usado**:
```
Genera un INFORME.md técnico que cubra:
- Introducción a landmarks faciales
- Arquitectura del proyecto
- Decisiones de diseño
- Desafíos encontrados
- Uso de Kilo en el desarrollo
```

**Resultado**: Este documento fue generado con la ayuda de Kilo.

### Interfaz de Kilo

Kilo se integra perfectamente con VS Code:

- **Ctrl+I**: Abrir chat con código seleccionado
- **Autocompletado**: Sugerencias inteligentes durante escritura
- **Explicaciones**: Contextuales sobre funciones y algoritmos
- **Refactoring**: Sugerencias para mejorar estructura del código

### Eficiencia del Desarrollo

Con Kilo, el tiempo de desarrollo se redujo significativamente:

- **Sin Kilo**: Investigación manual + debugging iterativo
- **Con Kilo**: Consultas directas + soluciones precisas

---

## 6. Conclusiones

### Aprendizajes Técnicos

#### Visión por Computadora
- **Landmarks faciales**: De teoría abstracta a implementación práctica
- **MediaPipe**: Framework poderoso para aplicaciones reales
- **OpenCV**: Manipulación eficiente de imágenes en Python
- **Coordenadas normalizadas**: Ventaja para diferentes resoluciones

#### Desarrollo de Software
- **Modularización**: Principio fundamental para proyectos escalables
- **Manejo de dependencias**: Crítico en proyectos Python complejos
- **Debugging sistemático**: Aislar problemas por componentes
- **Documentación**: Inversión que paga dividendos

#### Integración de Tecnologías
- **Streamlit**: Framework ideal para prototipos de ML
- **Git/GitHub**: Control de versiones esencial
- **Entornos virtuales**: Aislamiento de dependencias
- **Deployment cloud**: De desarrollo local a producción

### Desarrollo Asistido por IA

#### Beneficios de Kilo Code
- **Velocidad**: Soluciones rápidas a problemas complejos
- **Precisión**: Sugerencias técnicas acertadas
- **Aprendizaje**: Explicaciones detalladas de conceptos
- **Productividad**: Enfoque en lógica de alto nivel

#### Limitaciones Identificadas
- **Contexto**: Necesita información completa del problema
- **Validación**: Código generado requiere testing
- **Dependencia**: No reemplaza entendimiento fundamental

### Recomendaciones para Futuros Proyectos

#### Arquitectura
- **Siempre modularizar**: Desde el inicio del proyecto
- **Separar responsabilidades**: UI, lógica, datos
- **Documentar decisiones**: Por qué se eligieron ciertas tecnologías

#### Desarrollo
- **Usar agentes IA**: Para acelerar desarrollo y debugging
- **Testing temprano**: Verificar integración entre módulos
- **Versionado**: Git desde el primer commit

#### Deployment
- **Considerar restricciones**: De plataformas cloud desde el diseño
- **Optimizar dependencias**: Minimizar conflictos de versiones
- **Documentar proceso**: Para replicabilidad

### Impacto Educativo

Este proyecto demostró cómo la **integración de IA en el proceso educativo** puede:

- Acelerar el aprendizaje práctico
- Permitir proyectos más ambiciosos
- Enfocarse en conceptos de alto nivel
- Preparar para el futuro del desarrollo de software

---

## Referencias

### Documentación Oficial
- [MediaPipe Face Landmarker](https://ai.google.dev/edge/mediapipe/solutions/vision/face_landmarker)
- [Streamlit Documentation](https://docs.streamlit.io)
- [OpenCV Python Tutorials](https://docs.opencv.org/4.x/d6/d00/tutorial_py_root.html)

### Recursos Educativos
- [Kilo Code - Agente IA](https://kilocode.ai/)
- [Google Colab - Entorno de desarrollo](https://colab.research.google.com/)
- [GitHub - Repositorio del proyecto](https://github.com/Jordi9317/facial-landmarks-app)
- [IFT S24 - Procesamiento Digital de Imágenes](https://ifts24.edu.ar)

### Bibliotecas Utilizadas
- **MediaPipe** 0.10.0 - Google LLC (Apache License 2.0)
- **OpenCV** 4.8.0 - OpenCV Team (Apache License 2.0)
- **Streamlit** 1.28.0 - Streamlit Inc. (Apache License 2.0)
- **NumPy** 1.24.0 - NumPy Developers (BSD License)
- **Pillow** 10.0.0 - Python Imaging Library (PIL)

---

**Fecha de entrega**: 29 de octubre de 2025
**Estado del proyecto**: ✅ Completado y funcional
**Deployment**: ✅ Subido a GitHub (https://github.com/Jordi9317/facial-landmarks-app)
**Streamlit Cloud**: Listo para deploy