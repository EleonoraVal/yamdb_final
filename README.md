# yamdb_final
yamdb_final
https://github.com/EleonoraVal/yamdb_final/actions/workflows/yamdb_workflow.yml/badge.svg

### Описание проекта:

Yamdb:

Проект YaMDb собирает отзывы пользователей на различные произведения. Произведения делятся на жанры и категории.
```
Файл .env содержит данные с переменными окружения для работы с базой данных:

DB_ENGINE= # указываем, с какой базой данных работаем

DB_NAME= # имя базы данных

POSTGRES_USER= # логин для подключения к базе данных

POSTGRES_PASSWORD= # пароль для подключения к БД 

DB_HOST= # название сервиса (контейнера)

DB_PORT= # порт для подключения к БД

### Как запустить проект:

Клонировать репозиторий и перейти в него в командной строке:

```
git clone https://github.com/EleonoraVal/yamdb_final.git
```

cd api_yamdb
```

cd infra
```
Разверните контейнеры:
```

docker-compose up -d --build

```

Выполнить миграции:

```
docker-compose exec web python manage.py migrate
```
Создать суперпользователя:
```
docker-compose exec web python manage.py createsuperuser
```
Собрать статику:
```
docker-compose exec web python manage.py collectstatic --no-input
```

### Развернутый и запущенный на сервере проектт:
https://mysocialnetwork.ddns.net
