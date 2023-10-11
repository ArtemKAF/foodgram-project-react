ARG PYTHON_VERSION
ARG GUNICORN_VERSION
FROM python:$PYTHON_VERSION
RUN apk update && apk --no-cache add gettext
WORKDIR /app
COPY requirements.txt .
ARG GUNICORN_VERSION
ENV GUNICORN_VERSION=$GUNICORN_VERSION
RUN pip install --upgrade pip --no-cache-dir \
    && pip install gunicorn==$GUNICORN_VERSION --no-cache-dir \
    && pip install -r requirements.txt --no-cache-dir
COPY . .
CMD ["gunicorn", "--bind", "0.0.0.0:8000", "config.wsgi"]
