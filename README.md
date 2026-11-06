# AskPupkin
## ДЗ 1 - статическая вёрстка
Верстка сделана на чистом HTML + Bootstrap 5.3.8. Вся статика хранится локально - без CDN

### Как запустить
Сначала создайте `.env` из примера и впишите туда свой `SECRET_KEY`:
```
cp .env.example .env
```

Локально:
```
python -m venv venv
venv\Scripts\activate          (на Linux/Mac: source venv/bin/activate)
pip install -r requirements.txt
python manage.py runserver
```

Через Docker:
```
docker compose up --build -d
```
Сайт будет на http://127.0.0.1:8000/



### Роуты
- `/` - главная, список новых вопросов
- `/hot/` - популярные вопросы
- `/tag/<tag_name>/` - вопросы по тегу
- `/question/<question_id>/` - вопрос с ответами
- `/ask/` - задать вопрос
- `/login/` - вход
- `/signup/` - регистрация
- `/profile/` - настройки профиля (тут юзер залогинен)

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