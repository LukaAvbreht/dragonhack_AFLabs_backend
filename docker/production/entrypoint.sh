#!/usr/bin/env bash

until pg_isready -h "${DB_HOST}" -p "${DB_PORT}" -U "${DB_USER}" 2>/dev/null; do
	echo "waiting for postgres"
	sleep 1
done

python manage.py collectstatic --no-input --settings=config.settings.${SETTINGS_NAME}
python manage.py migrate --settings=config.settings.${SETTINGS_NAME}

exec uwsgi --chdir=/app --module=config.wsgi:application --env DJANGO_SETTINGS_MODULE=config.settings.${SETTINGS_NAME} --master --protocol=uwsgi --socket=0.0.0.0:3030 --enable-threads --processes=2
