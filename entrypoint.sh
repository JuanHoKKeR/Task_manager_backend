#!/bin/bash
set -e

# Cambiar la propiedad del directorio media a celeryuser
chown -R celeryuser:celeryuser /app/media

# Ejecutar el comando principal como celeryuser
exec su celeryuser -s /bin/bash -c "exec $*"
