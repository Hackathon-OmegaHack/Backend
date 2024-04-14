# Usa una imagen base de Python
FROM python:3.9-slim

# Establece el directorio de trabajo en /app
WORKDIR /app

# Copia el archivo requirements.txt al directorio de trabajo
COPY requirements.txt .

# Instala las dependencias del proyecto
RUN pip install --no-cache-dir -r requirements.txt

# Copia todo el contenido del directorio actual al directorio de trabajo en el contenedor
COPY . .

# Expone el puerto 80 en el contenedor
EXPOSE 80

# Comando para ejecutar la aplicación cuando se inicie el contenedor
CMD ["uvicorn", "app:app", "--host", "0.0.0.0", "--port", "80"]