# Учебный проект
### Описание
Этот проект собирает отзывы пользователей на произведения.  Сами произведения в проекте не хранятся, здесь нельзя посмотреть фильм или послушать музыку. По адресу http://localhost/redoc/ доступна документация API. 
### Технологии
- Python 3.8.0
- Django Rest Framework 3.12.4
- Gunicorn 20.0.4
- Nginx 1.21.3
### Запуск проекта в dev-режиме
- Требуется создать файл ``` .env ``` в директории ``` infra ```, в файле требуется указать необходимые для работы проекта переменные окружения, пример перечня минимально необходимых переменных указан в файле ``` .env.example ```
- Перейдите в директорию с docker-compose файлом, и выполните команду: ``` docker-compose up ```
- Выполните миграции ``` docker-compose exec web python manage.py migrate ```
- Создайте супер юзера для доступа к админке командой ``` docker-compose exec web python manage.py createsuperuser ```. Укажите логин, почту и пароль для админской учётки
- Настройте статику проекта командой: ``` docker-compose exec web python manage.py collectstatic --no-input ```
- В случае успешного выполнения инструкций, проект будет доступен по ссылке ``` http://localhost ```
### Автор:
Токарев Николай  
nickotoko@yandex.ru

Ссылка на работающий проект: ``` http://51.250.80.138/ ```
![example workflow](https://github.com/nickotoko/yamdb_final/actions/workflows/yamdb_workflow.yml/badge.svg)