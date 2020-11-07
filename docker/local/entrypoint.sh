#!/usr/bin/env bash

until pg_isready -h "${DB_HOST}" -p "${DB_PORT}" -U "${DB_USER}" 2>/dev/null; do
	echo "waiting for postgres"
	sleep 1
done

# python manage.py collectstatic --no-input --settings=config.settings.${SETTINGS_NAME}
# python manage.py migrate --settings=config.settings.${SETTINGS_NAME}

exec python manage.py runserver "0.0.0.0:8000"
