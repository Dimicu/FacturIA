# FacturIA - Sistema Inteligente de Gestión de Facturas

## 📝 Descripción

FacturIA es un sistema avanzado de gestión de facturas que combina la potencia de la Inteligencia Artificial con una interfaz de usuario intuitiva para automatizar y simplificar el proceso de gestión de facturas. El sistema está diseñado para procesar, almacenar y gestionar facturas de manera eficiente, utilizando tecnologías de vanguardia en el procesamiento de lenguaje natural y reconocimiento de imágenes.

## 🎯 Características Principales

### 🤖 Procesamiento Inteligente de Facturas

- **OCR Avanzado**: Utiliza Tesseract OCR para extraer texto de imágenes de facturas
- **IA para Interpretación**: Implementa modelos de IA (OpenAI) para interpretar y estructurar la información de las facturas
- **Extracción Automática**: Identifica automáticamente elementos clave como:
  - Números de factura
  - Fechas
  - Montos
  - Detalles del vendedor y comprador
  - Conceptos y descripciones

### 💼 Gestión de Facturas

- **Almacenamiento Seguro**: Guarda tanto las imágenes como los datos estructurados de las facturas
- **Edición Inteligente**: Permite modificar y actualizar la información extraída
- **Categorización**: Clasifica automáticamente las facturas por tipo
- **Balance Automático**: Calcula y mantiene un balance actualizado de ingresos y gastos

### 🔐 Seguridad y Autenticación

- Sistema de registro y login seguro
- Gestión de sesiones de usuario
- Almacenamiento seguro de datos en Supabase
- Protección de información sensible

### 📊 Monitoreo y Rendimiento

- Sistema de monitoreo de rendimiento en tiempo real
- Tracking de errores y excepciones
- Métricas de uso de la API
- Optimización de recursos

## 🛠️ Tecnologías Principales

- **Backend**: FastAPI (Python)

  - Procesamiento de imágenes con PIL
  - OCR con Tesseract
  - IA con OpenAI y LangChain
  - API RESTful

- **Frontend**: Streamlit

  - Interfaz de usuario moderna y responsiva
  - Visualización de datos en tiempo real
  - Gestión de archivos intuitiva

- **Base de Datos**: Supabase

  - Almacenamiento seguro de datos
  - Gestión de usuarios
  - Sistema de autenticación

- **IA y Procesamiento**:
  - OpenAI GPT para interpretación de texto
  - Tesseract OCR para extracción de texto
  - LangChain para procesamiento estructurado

## 🚀 Casos de Uso

1. **Subida de Facturas**:

   - El usuario sube una imagen de factura
   - El sistema extrae automáticamente el texto
   - La IA interpreta y estructura la información
   - Los datos se almacenan de forma organizada

2. **Gestión de Facturas**:

   - Visualización de todas las facturas
   - Edición de información extraída
   - Filtrado y búsqueda
   - Exportación de datos

3. **Análisis Financiero**:
   - Balance automático de ingresos/gastos
   - Categorización de gastos
   - Historial de transacciones

## 🔧 Requisitos del Sistema

- Python 3.8 o superior
- Tesseract OCR instalado
- Cuenta de OpenAI con API key
- Cuenta en Supabase
- Docker (opcional)

## 📦 Instalación

1. Clonar el repositorio:

```bash
git clone https://github.com/tu-usuario/FacturIA.git
cd FacturIA
```

2. Instalar dependencias:

```bash
# Backend
cd backend
pip install -r requirements.txt

# Frontend
cd ../frontend
pip install -r requirements.txt
```

3. Configurar variables de entorno:

```bash
# Crear archivo .env con:
OPENAI_API_KEY=tu_api_key
SUPABASE_URL=tu_url
SUPABASE_KEY=tu_key
```

## 🚀 Uso

1. Iniciar el backend:

```bash
cd backend
uvicorn app:app --reload
```

2. Iniciar el frontend:

```bash
cd frontend
streamlit run index.py
```

3. Acceder a la aplicación:

- Abrir navegador en `http://localhost:8501`
- Registrar una cuenta nueva
- Comenzar a gestionar facturas

## 🤝 Contribuir

El proyecto está abierto a contribuciones. Por favor, sigue estos pasos:

1. Fork el repositorio
2. Crea una rama para tu feature
3. Realiza tus cambios
4. Envía un Pull Request

## 📝 Licencia

Este proyecto está bajo la Licencia MIT. Ver el archivo [LICENSE](LICENSE) para más detalles.

## 👥 Autores

- [Dimicu](https://github.com/Dimicu) - _Desarrollador_
- [JoseMLG03](https://github.com/JoseMLG03) - _Desarrollador_
- [Julalz](https://github.com/Julalz) - _Desarrollador_

## 🙏 Agradecimientos

- OpenAI por su API de GPT
- Tesseract OCR por su potente motor de reconocimiento
- FastAPI por su framework web moderno
- Streamlit por su interfaz de usuario intuitiva
- Supabase por su plataforma de backend
