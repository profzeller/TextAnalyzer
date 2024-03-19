#!/bin/sh

/usr/local/bin/python manage.py collectstatic --noinput
/usr/local/bin/python manage.py makemigrations
/usr/local/bin/python manage.py migrate
/usr/local/bin/python manage.py createcachetable

if [ "$DJANGO_SUPERUSER_USERNAME" ]
then
    echo "Creating superuser..."
    python manage.py createsuperuser \
        --noinput \
        --username $DJANGO_SUPERUSER_USERNAME \
        --email $DJANGO_SUPERUSER_EMAIL
fi

/usr/local/bin/gunicorn hayland.wsgi --bind=0.0.0.0:80