# AskPupkin
## ДЗ 1 - статическая вёрстка
Верстка сделана на чистом HTML + Bootstrap 5.3.8. Вся статика хранится локально - без CDN

## ДЗ 2 - views, шаблоны, пагинация
Страницы отдаются через Django views, шаблоны наследуются от base.html, есть пагинация и Docker

## ДЗ 3 - база данных
Сделаны модели, админка и команда для заполнения базы тестовыми данными

### Как запустить
Сначала создайте файлы с переменными окружения из примера:
```
cp .env.example .env.local
cp .env.example .env.docker
```
В .env.docker поменяйте DB_HOST=localhost на DB_HOST=db

Через Docker:
```bash
docker compose up --build -d
docker compose exec web python manage.py fill_db 10000
docker compose exec web python manage.py createsuperuser
```

Локально:
```bash
python -m venv venv
venv\Scripts\activate          (на Linux/Mac: source venv/bin/activate)
pip install -r requirements.txt
python manage.py migrate
python manage.py fill_db 100
python manage.py createsuperuser
python manage.py runserver
```

Сайт будет на http://127.0.0.1:8000/ , админка на http://127.0.0.1:8000/admin/

python manage.py fill_db [ratio] : Добавляет пользователей - ratio, тегов - ratio, вопросов - ratio * 10, ответов - ratio * 100, оценок - ratio * 200. Пароль у всех созданных пользователей - password

### Роуты
- `/` - главная, список новых вопросов
- `/hot/` - популярные вопросы
- `/tag/<tag_name>/` - вопросы по тегу
- `/question/<question_id>/` - вопрос с ответами
- `/ask/` - задать вопрос
- `/login/` - вход
- `/signup/` - регистрация
- `/profile/` - настройки профиля (тут юзер залогинен)
- `/admin/` - админка

### Структура
```
.
├── Dockerfile
├── README.md
├── application
│   ├── __init__.py
│   ├── asgi.py
│   ├── settings.py
│   ├── urls.py
│   └── wsgi.py
├── core
│   ├── __init__.py
│   ├── admin.py
│   ├── apps.py
│   ├── context_processors.py
│   ├── migrations
│   │   └── __init__.py
│   ├── mock_data.py
│   ├── models.py
│   ├── static
│   │   └── core
│   │       ├── css
│   │       │   ├── bootstrap.min.css
│   │       │   └── style.css
│   │       ├── img
│   │       │   ├── avatar-1.jpg
│   │       │   └── favicon.png
│   │       └── js
│   │           └── bootstrap.js
│   ├── templates
│   │   └── core
│   │       ├── avatar.html
│   │       ├── base.html
│   │       ├── login.html
│   │       ├── paginator.html
│   │       ├── profile.html
│   │       └── signup.html
│   ├── tests.py
│   ├── urls.py
│   ├── utils.py
│   └── views.py
├── db.sqlite3
├── docker-compose.yml
├── manage.py
├── media
├── public
│   └── static
├── questions
│   ├── __init__.py
│   ├── admin.py
│   ├── apps.py
│   ├── migrations
│   │   └── __init__.py
│   ├── mock_data.py
│   ├── models.py
│   ├── static
│   │   └── questions
│   ├── templates
│   │   └── questions
│   │       ├── answer_card.html
│   │       ├── ask.html
│   │       ├── hot.html
│   │       ├── index.html
│   │       ├── question.html
│   │       ├── question_card.html
│   │       ├── rating.html
│   │       └── tag.html
│   ├── tests.py
│   ├── urls.py
│   └── views.py
└── requirements.txt

20 directories, 50 files
```