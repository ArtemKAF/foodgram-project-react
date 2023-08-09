# Foodgram **https://foodgram-yap.sytes.net**

![workflow](https://github.com/ArtemKAF/foodgram-project-react/actions/workflows/main.yml/badge.svg)

Проект для публикации рецептов. Позволяет добавлять рецепты в избранное,
подписываться на любимых авторов рецептов, а также скачивать список покупок
необходимых ингредиентов из выбранных для этого рецептов.

## Использованные технологии:
- Python 3.9.16
- Django 4.2.2
- DRF 3.14.0
- Docker
- Postgres

## Для локального запуска в Docker контейнерах:

Необходимо предварительно установить:  
    - [Docker](https://docs.docker.com/engine/install/) и [Docker Compose](https://docs.docker.com/compose/install/)  
    или  
    - [Docker Desktop ](https://docs.docker.com/desktop/install/windows-install/)  
- В папке backend подготовить файл .env и наполнить по шаблону .env.example
- Запустить сборку и запуск контейнером командой
```
sudo docker compose up -d
```
По завершении работы команды проект станет доступен по адресу [http://localhost/](http://localhost/) или [http://127.0.0.1/](http://127.0.0.1/)  

По адресу [http://localhost/api/docs/](http://localhost/api/docs/) будет доступна спецификация к API проекта.
