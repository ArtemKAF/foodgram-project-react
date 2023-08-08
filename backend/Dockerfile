ARG PYTHON_VERSION
ARG GUNICORN_VERSION
FROM python:$PYTHON_VERSION
WORKDIR /app
COPY requirements.txt .
RUN apt-get update && apt-get install gettext -y
ARG GUNICORN_VERSION
ENV GUNICORN_VERSION=$GUNICORN_VERSION
RUN pip install gunicorn==$GUNICORN_VERSION --no-cache-dir \
    pip install -r requirements.txt --no-cache-dir
COPY . .
CMD ["gunicorn", "--bind", "0.0.0.0:8000", "config.wsgi"]
