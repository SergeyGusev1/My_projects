 #!/bin/bash

set -e

cd /app

echo "Waiting for PostgreSQL..."
sleep 10

echo "Applying database migrations..."
python manage.py migrate --noinput

echo "Collecting static files..."
python manage.py collectstatic --noinput

echo "Copying static files..."
mkdir -p /backend_static/static
cp -r /app/collected_static/. /backend_static/static/
echo "Static files:"
ls -la /backend_static/static
exec "$@"