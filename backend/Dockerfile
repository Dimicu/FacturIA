# Usar una imagen base de Python
FROM python:3.12

RUN apt-get update && apt-get install -y tesseract-ocr tesseract-ocr-spa

# Establecer el directorio de trabajo
WORKDIR /backend

# Copiar los archivos del backend
COPY requirements.txt .
RUN pip install --no-cache-dir -r requirements.txt
COPY . /backend


# Instalar dependencias


# Exponer el puerto (ajústalo si tu backend usa otro puerto)
EXPOSE 8000

# Comando para ejecutar el backend
CMD ["uvicorn", "app:app", "--host", "0.0.0.0", "--port", "8000"]