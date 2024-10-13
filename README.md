# Task Manager Backend

## Descripción

Task Manager Backend es una API RESTful desarrollada con Django y Django REST Framework, diseñada para permitir a los usuarios gestionar sus tareas diarias. La aplicación incluye funcionalidades de creación, actualización, eliminación y visualización de tareas, así como autenticación de usuarios mediante JWT. Además, soporta la subida de archivos adjuntos a las tareas, notificaciones por correo electrónico para tareas próximas a vencer, análisis de estadísticas y la organización de tareas mediante etiquetas personalizadas.

## Tabla de Contenidos

- [Características](#características)
- [Tecnologías](#tecnologías)
- [Instalación](#instalación)
- [Configuración](#configuración)
- [Uso](#uso)
- [Dockerización](#dockerización)
- [Migraciones y Superusuario](#migraciones-y-superusuario)
- [Ejecutar Pruebas](#ejecutar-pruebas)
- [Documentación de la API](#documentación-de-la-api)
- [Contribuciones](#contribuciones)
- [Licencia](#licencia)

## Características

- **Gestión de Tareas:** Crear, leer, actualizar y eliminar tareas.
- **Autenticación:** Registro e inicio de sesión de usuarios utilizando JWT.
- **Subida de Archivos:** Adjuntar archivos a las tareas.
- **Notificaciones por Email:** Envío de recordatorios para tareas próximas a vencer.
- **Análisis de Estadísticas:** Visualizar estadísticas sobre el estado de las tareas.
- **Etiquetas Personalizadas:** Organizar tareas mediante etiquetas según el usuario.
- **Dockerización Completa:** Facilita la instalación y despliegue utilizando Docker y Docker Compose.

## Tecnologías

- **Backend:**
  - Python 3.9
  - Django
  - Django REST Framework
  - PostgreSQL
  - Celery
  - Redis
  - Docker
  - Docker Compose

## Instalación

### Requisitos Previos

- **Docker:** Asegúrate de tener Docker instalado en tu máquina. Puedes descargarlo [aquí](https://www.docker.com/get-started).
- **Docker Compose:** Generalmente viene incluido con Docker Desktop.

### Pasos de Instalación

1. **Clonar el Repositorio:**

    ```bash
    git clone https://github.com/tu_usuario/task-manager-backend.git
    cd task-manager-backend
    ```

2. **Crear el Archivo `.env`:**

    Crea un archivo `.env` en la raíz del proyecto con las siguientes variables de entorno:

    ```env
    # .env

    DATABASE_URL=postgres://postgres:postgres@db:5432/taskdb
    CELERY_BROKER_URL=redis://redis:6379/0
    EMAIL_HOST_USER=tu_email@gmail.com
    EMAIL_HOST_PASSWORD=tu_contraseña
    ```

    **Nota:** Asegúrate de reemplazar `tu_email@gmail.com` y `tu_contraseña` con tus credenciales reales de correo electrónico. Para mayor seguridad, considera utilizar variables de entorno seguras o servicios de gestión de secretos.

3. **Construir y Levantar los Servicios con Docker Compose:**

    ```bash
    docker-compose up --build
    ```

    Esto levantará los siguientes servicios:

    - **db:** Base de datos PostgreSQL.
    - **redis:** Broker para Celery.
    - **web:** Servidor Django.
    - **celery:** Worker de Celery.
    - **celery-beat:** Scheduler de Celery Beat.

## Configuración

### Variables de Entorno

El archivo `.env` debe contener las siguientes variables:

- `DATABASE_URL`: URL de conexión a la base de datos PostgreSQL.
- `CELERY_BROKER_URL`: URL del broker de Celery (Redis).
- `EMAIL_HOST_USER`: Dirección de correo electrónico para enviar notificaciones.
- `EMAIL_HOST_PASSWORD`: Contraseña del correo electrónico.

### Configuración de Django

Todas las configuraciones relevantes están gestionadas en `taskmanager/settings.py`, incluyendo la configuración de la base de datos, Celery y el backend de correo electrónico.

## Uso

### Acceder a la API

Una vez que los servicios estén levantados, puedes acceder a la API en:

```
http://localhost:8000/api/
```

### Registro e Inicio de Sesión

- **Registro de Usuario:**

  - **Endpoint:** `POST /api/users/`
  - **Body (JSON):**
    ```json
    {
        "username": "usuario",
        "password": "contraseña"
    }
    ```

- **Obtener Token JWT:**

  - **Endpoint:** `POST /api/token/`
  - **Body (JSON):**
    ```json
    {
        "username": "usuario",
        "password": "contraseña"
    }
    ```

  - **Respuesta:**
    ```json
    {
        "refresh": "token_de_refresh",
        "access": "token_de_access"
    }
    ```

### Operaciones CRUD de Tareas

- **Crear una Tarea:**

  - **Endpoint:** `POST /api/tasks/`
  - **Headers:**
    - `Authorization: Bearer <token_de_access>`
  - **Body (JSON):**
    ```json
    {
        "title": "Título de la tarea",
        "description": "Descripción de la tarea",
        "status": "pending",
        "deadline": "2024-12-31",
        "tags": [
            {"name": "Universidad"},
            {"name": "Estudio"}
        ]
    }
    ```

- **Obtener Lista de Tareas:**

  - **Endpoint:** `GET /api/tasks/`
  - **Headers:**
    - `Authorization: Bearer <token_de_access>`

- **Actualizar una Tarea:**

  - **Endpoint:** `PUT /api/tasks/<id>/`
  - **Headers:**
    - `Authorization: Bearer <token_de_access>`
  - **Body (JSON):** Similar al de creación.

- **Eliminar una Tarea:**

  - **Endpoint:** `DELETE /api/tasks/<id>/`
  - **Headers:**
    - `Authorization: Bearer <token_de_access>`

### Subida de Archivos

- **Adjuntar un Archivo a una Tarea:**

  - **Endpoint:** `POST /api/tasks/`
  - **Headers:**
    - `Authorization: Bearer <token_de_access>`
  - **Body:**
    - Tipo: `form-data`
    - Campos:
      - `title`: `Título de la tarea`
      - `description`: `Descripción`
      - `status`: `pending`
      - `deadline`: `2024-12-31`
      - `attachment`: (Selecciona un archivo)

### Notificaciones por Email

Las notificaciones por correo electrónico se envían automáticamente a los usuarios cuando una tarea está próxima a vencer (configurado para 3 días antes). Asegúrate de que los usuarios tengan un correo electrónico válido asociado a su cuenta.

### Sección de Análisis (Estadísticas)

- **Endpoint:** `GET /api/statistics/`
- **Headers:**
  - `Authorization: Bearer <token_de_access>`
- **Respuesta:**
  ```json
  {
      "total_tasks": 10,
      "completed_tasks": 7,
      "pending_tasks": 2,
      "abandoned_tasks": 1,
      "overdue_tasks": 0
  }
  ```

### Gestión de Etiquetas

- **Crear una Etiqueta:**

  - **Endpoint:** `POST /api/tags/`
  - **Headers:**
    - `Authorization: Bearer <token_de_access>`
  - **Body (JSON):**
    ```json
    {
        "name": "Trabajo"
    }
    ```

- **Obtener Lista de Etiquetas:**

  - **Endpoint:** `GET /api/tags/`
  - **Headers:**
    - `Authorization: Bearer <token_de_access>`

## Dockerización

### Estructura de Archivos

- **Dockerfile:** Define la imagen Docker para el backend.
- **docker-compose.yml:** Orquesta los servicios necesarios (PostgreSQL, Redis, Django, Celery, Celery Beat).
- **entrypoint.sh:** Script de entrada para configurar permisos y ejecutar comandos como usuario no root.

### Dockerfile

```dockerfile
# Dockerfile 

# Utilizar una imagen base de python
FROM python:3.9-slim

# Establecer variables de entorno
ENV PYTHONUNBUFFERED 1

# Instalar dependencias del sistema
RUN apt-get update && apt-get install -y build-essential libpq-dev && rm -rf /var/lib/apt/lists/*

# Crear un usuario no root
RUN useradd -m celeryuser

# Establecer directorio de trabajo
WORKDIR /app

# Copiar e instalar dependencias
COPY requirements.txt /app/
RUN pip install --upgrade pip
RUN pip install -r requirements.txt

# Copiar el código fuente
COPY . /app/

# Crear el directorio para media files
RUN mkdir -p /app/media/attachments

# Copiar el script de entrada
COPY entrypoint.sh /entrypoint.sh
RUN chmod +x /entrypoint.sh

# Exponer el puerto 8000
EXPOSE 8000

# Configurar el script de entrada
ENTRYPOINT ["/entrypoint.sh"]

# Comando por defecto (override en docker-compose)
CMD ["gunicorn", "taskmanager.wsgi:application", "--bind", "0.0.0.0:8000"]
```

### docker-compose.yml

```yaml
version: '3'

services:
  db:
    image: postgres:17.0
    environment:
      POSTGRES_DB: 'taskdb'
      POSTGRES_USER: 'postgres'
      POSTGRES_PASSWORD: 'postgres'
    ports:
      - '5432:5432'
    volumes:
      - db_data:/var/lib/postgresql/data
    networks:
      - backend

  redis:
    image: redis:6.0.20
    ports:
      - '6379:6379'
    networks:
      - backend

  web:
    build: .
    command: gunicorn taskmanager.wsgi:application --bind 0.0.0.0:8000
    volumes:
      - .:/app
      - media_volume:/app/media
    ports:
      - '8000:8000'
    depends_on:
      - db
      - redis
    env_file:
      - .env
    networks:
      - backend

  celery:
    build: .
    command: celery -A taskmanager worker -l info
    volumes:
      - .:/app
      - media_volume:/app/media
    depends_on:
      - web
      - redis
    env_file:
      - .env
    networks:
      - backend
    
  celery-beat:
    build: .
    command: celery -A taskmanager beat -l info
    volumes:
      - .:/app
      - media_volume:/app/media
    depends_on:
      - web
      - redis
    env_file:
      - .env
    networks:
      - backend

volumes:
  db_data:
  media_volume:

networks:
  backend: 
    driver: bridge
```

### entrypoint.sh

```bash
#!/bin/bash
set -e

# Cambiar la propiedad del directorio media a celeryuser
chown -R celeryuser:celeryuser /app/media

# Ejecutar el comando principal como celeryuser
exec su celeryuser -s /bin/bash -c "exec $*"
```

**Nota:** Asegúrate de que `entrypoint.sh` tiene permisos de ejecución. Puedes hacerlo con:

```bash
chmod +x entrypoint.sh
```

### Ejecutar los Servicios

Para construir y levantar todos los servicios, ejecuta:

```bash
docker-compose up --build
```

Esto iniciará los servicios de la base de datos, Redis, el servidor Django, Celery y Celery Beat.

## Migraciones y Superusuario

1. **Aplicar Migraciones:**

    ```bash
    docker-compose exec web python manage.py migrate
    ```

2. **Crear un Superusuario:**

    ```bash
    docker-compose exec web python manage.py createsuperuser
    ```

    Sigue las instrucciones en pantalla para configurar tu superusuario.

## Ejecutar Pruebas

Para ejecutar las pruebas unitarias, asegúrate de que los servicios estén corriendo y ejecuta:

```bash
docker-compose exec web python manage.py test
```

Esto ejecutará las pruebas definidas en `tasks/tests.py`.

## Documentación de la API

La API está documentada utilizando **Swagger** a través de **DRF Yasg**. Para acceder a la documentación:

1. Asegúrate de que los servicios están levantados.
2. Navega a: [http://localhost:8000/swagger/](http://localhost:8000/swagger/)

Aquí encontrarás una interfaz interactiva para explorar y probar los endpoints de la API.

## Contribuciones

¡Las contribuciones son bienvenidas! Si deseas contribuir a este proyecto, por favor sigue los siguientes pasos:

1. **Fork del Repositorio**
2. **Crear una Rama para tu Feature:**

    ```bash
    git checkout -b nombre-de-tu-feature
    ```

3. **Realizar los Cambios Necesarios**
4. **Commit de tus Cambios:**

    ```bash
    git commit -m "Descripción de tus cambios"
    ```

5. **Push a tu Rama:**

    ```bash
    git push origin nombre-de-tu-feature
    ```

6. **Crear un Pull Request**

## Licencia

Este proyecto está bajo la licencia [MIT](LICENSE).

---

## Notas Adicionales

- **Seguridad:** Asegúrate de manejar las credenciales sensibles de manera segura. No compartas el archivo `.env` y considera utilizar herramientas adicionales para la gestión de secretos en producción.
- **Medios y Archivos:** Los archivos subidos se almacenan en el directorio `media/attachments/`. En entornos de producción, considera usar servicios de almacenamiento externos como Amazon S3.
- **Optimización de Celery:** Para proyectos más grandes, podrías considerar escalar los workers de Celery y optimizar las tareas para mejorar la eficiencia.

Si tienes alguna duda o encuentras algún problema, no dudes en abrir una issue en el repositorio o contactarme directamente. ¡Éxito con tu proyecto!