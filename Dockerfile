# Use an official Python runtime as a parent image
FROM library/python:3.10-bullseye

RUN apt-get update \
    # dependencies for building Python packages
    && apt-get install -y build-essential gunicorn3 dos2unix\
    # psycopg2 dependencies
    #&& apt-get install -y libpq-dev \
    # Translations dependencies
    #&& apt-get install -y gettext \
    #&& apt-get install -y libcairo2 libpango-1.0-0 libpangocairo-1.0-0 libgdk-pixbuf2.0-0 libffi-dev shared-mime-info \
    # cleaning up unused files
    && apt-get purge -y --auto-remove -o APT::AutoRemove::RecommendsImportant=false \
    && rm -rf /var/lib/apt/lists/*

# Set environment variables
ENV PYTHONDONTWRITEBYTECODE 1
ENV PYTHONUNBUFFERED 1

# Set work directory
RUN mkdir -p /usr/src/app
WORKDIR /usr/src/app

# Install dependencies
COPY ./requirements.txt /requirements.txt
RUN /usr/local/bin/python -m pip install --no-cache-dir -r /requirements.txt \
    && rm -rf /requirements.txt

RUN /usr/local/bin/python manage.py makemigrations
RUN /usr/local/bin/python manage.py makemigrate

# Copy project
COPY . /usr/src/app

RUN /usr/local/bin/python manage.py makemigrations
RUN /usr/local/bin/python manage.py makemigrate

# Expose port 80 for Django
EXPOSE 80

#RUN dos2unix ./runserver.sh
#CMD ["/bin/sh", "./runserver.sh"]

# Run the application
#CMD ["python", "manage.py", "runserver", "0.0.0.0:8000"]
