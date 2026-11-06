# AskPupkin
## ДЗ 1 - статическая вёрстка
Верстка сделана на чистом HTML + Bootstrap 5.3.8. Вся статика хранится локально - без CDN

### Как открыть
Откройте файл `public/index.html` в любом браузере
(двойной клик по файлу). Все страницы связаны ссылками.

### Роуты
- `index.html` - главная, список новых вопросов
- `hot.html` - популярные вопросы
- `tag.html` - вопросы по тегу
- `question.html` - вопрос с ответами
- `ask.html` - задать вопрос
- `login.html` - вход
- `signup.html` - регистрация
- `profile.html` - настройки профиля (тут юзер залогинен)
- `base.html` - общий шаблон для всех страниц

### Структура
```
2026-VK-EDU-Web-12-Tveretin-P/
├── README.md
└── public
    ├── ask.html
    ├── base.html
    ├── hot.html
    ├── index.html
    ├── login.html
    ├── profile.html
    ├── question.html
    ├── signup.html
    ├── static
    │   ├── css
    │   │   ├── bootstrap.min.css
    │   │   └── style.css
    │   ├── img
    │   │   ├── avatar-1.png
    │   │   ├── avatar-2.png
    │   │   ├── avatar-3.png
    │   │   ├── avatar-4.png
    │   │   ├── avatar-default.png
    │   │   └── favicon.png
    │   └── js
    │       └── bootstrap.js
    └── tag.html

6 directories, 19 files
```