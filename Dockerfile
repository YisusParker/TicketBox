# Define como se construye la imagen de la aplicación
FROM python:3.11-slim

WORKDIR /app
# Copia el archivo de requerimientos y lo instala
COPY requirements.txt .
RUN pip install --no-cache-dir -r requirements.txt

# Copia el resto de los archivos de la aplicación
COPY . .

# Expone el puerto 8000
EXPOSE 8000