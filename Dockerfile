# Dockerfile 

# Utilizar una imagen base de python
FROM python:3.9-slim

# Establecer variables de entorno
ENV PYTHONUNBUFFERED 1

# Establecer directorio de trabajo
WORKDIR /app

# Instalar dependencias del sistema
RUN apt-get update && apt-get install -y build-essential libpq-dev && rm -rf /var/lib/apt/lists/*

# Copiar e instalar dependencias
COPY requirements.txt /app/
RUN pip install --upgrade pip
RUN pip install -r requirements.txt

# Copiar el código fuente
COPY . /app/

# Exponer el puerto 8000
EXPOSE 8000

# Comando por defecto (override en docker-compose)
CMD ["gunicorn", "taskmanager.wsgi:application", "--bind", "0.0.0.0:8000"]