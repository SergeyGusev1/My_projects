Foodgram
Продуктовый помощник, сервис на котором есть возможность зарегестрироваться и выкладывать свои рецепты. 
Пользователь может сортировать все рецепты по тегам, смотреть ингредиентыЮ добавлять в свою корзину рецепты. Есть возможность скачивать корзину.
В ней будут все ингредиенты для рецептов в корзине и их количество.
Имеется возможность подписываться на других пользователей.
Рецепты можно также добавлять в избранное, где удобно их просматривать.

Для запуска на сервере:
Клонировать репозиторий.
Установить Docker, Docker Compose
В разделе GitHub Actions нужно создать Secrets:
SECRET_KEY
DOCKER_PASSWORD
DOCKER_USERNAME
HOST
USER
PASSPHRASE
SSH_KEY
TELEGRAM_TO
TELEGRAM_TOKEN
ALLOWED_HOSTS

После чего запустить проект.

Используемые технологии:
Python, Django, DRF, Docker, Gunicorn, NGINX, PostreSQL.

Как локально запустить проект:
1) Колинровать репозиторий:
git clone git@github.com:SergeyGusev1/foodgram.git
2) Запустить докер композ:
docker compose -f docker-compose.yml up -d --build
3) Добавить ингредиенты:
docker compose -f infra/docker-local.yml python manage.py add_ingredients
4) Создать супер позьзователя:
docker compose -f infra/docker-local.yml python manage.py createsuperuser
5) Зайти в админку и создать теги


Домен: https://kittygramlazyx.zapto.org/
Админ пользователь: 
mail: gusiev2003@mail.ru 
password: Sportland
ip: 84.201.177.141