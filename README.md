# AskPupkin
## ДЗ 1 - статическая вёрстка
Верстка сделана на чистом HTML + Bootstrap 5.3.8. Вся статика хранится локально - без CDN

## ДЗ 2 - views, шаблоны, пагинация
Страницы отдаются через Django views, шаблоны наследуются от base.html, есть пагинация и Docker

## ДЗ 3 - база данных
Сделаны модели, админка и команда для заполнения базы тестовыми данными

## ДЗ 4 - авторизация и формы
Вход, выход, регистрация и редактирование профиля с загрузкой аватарки. Формы добавления вопроса и ответа. Лайки/дизлайки и отметка правильного ответа работают через AJAX

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
- `/logout/` - выход
- `/profile/` - настройки профиля (тут юзер залогинен)
- `/admin/` - админка

AJAX (POST, ответ в JSON):
- `/question/like/` - лайк/дизлайк вопроса, параметры question, value (1 или -1)
- `/answer/like/` - лайк/дизлайк ответа, параметры answer, value
- `/answer/correct/` - отметить правильный ответ (только автор вопроса), параметры question, answer

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
│   ├── forms.py
│   ├── migrations
│   │   ├── 0001_initial.py
│   │   ├── 0002_avatar_upload_to.py
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
│   │           ├── bootstrap.js
│   │           └── main.js
│   ├── templates
│   │   └── core
│   │       ├── avatar.html
│   │       ├── base.html
│   │       ├── form_errors.html
│   │       ├── form_field.html
│   │       ├── login.html
│   │       ├── paginator.html
│   │       ├── profile.html
│   │       └── signup.html
│   ├── tests.py
│   ├── urls.py
│   ├── utils.py
│   └── views.py
├── docker-compose.yml
├── manage.py
├── media
├── questions
│   ├── __init__.py
│   ├── admin.py
│   ├── apps.py
│   ├── forms.py
│   ├── management
│   │   ├── __init__.py
│   │   └── commands
│   │       ├── __init__.py
│   │       └── fill_db.py
│   ├── migrations
│   │   ├── 0001_initial.py
│   │   └── __init__.py
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

20 directories, 59 files
```