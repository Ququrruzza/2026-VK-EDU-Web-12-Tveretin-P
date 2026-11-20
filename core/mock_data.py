from django.templatetags.static import static

# пока нет авторизации, на странице профиля показываем заглушку
CURRENT_USER = {
    "display_name": "Dr. Pepper",
    "initials": "DP",
    "color": "#0d6efd",
    "avatar_url": static("core/img/avatar-1.jpg"),
    "login": "dr_pepper",
    "email": "drpepper@",
}
