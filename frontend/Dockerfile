# Usar una imagen base de Python
FROM python:3.12

# Establecer el directorio de trabajo
WORKDIR /app

# Copiar los archivos del backend
COPY . /app

# Instalar dependencias
RUN pip install --no-cache-dir -r requirements.txt

# Exponer el puerto (ajústalo si tu backend usa otro puerto)
EXPOSE 8501

# Comando para ejecutar el backend
CMD ["streamlit", "run", "index.py", "--server.port=8501", "--server.address=0.0.0.0"]