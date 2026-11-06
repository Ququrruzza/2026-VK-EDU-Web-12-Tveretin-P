AVATAR_COLORS = ["#0d6efd", "#198754", "#dc3545", "#6f42c1", "#fd7e14", "#20c997"]


def make_user(user_id, name, avatar=None):
    words = name.replace(".", " ").split()
    return {
        "id": user_id,
        "name": name,
        "avatar": avatar,
        "initials": "".join(word[0] for word in words[:2]).upper(),
        "color": AVATAR_COLORS[user_id % len(AVATAR_COLORS)],
    }


USERS = [
    make_user(1, "Mr. Freeman"),
    make_user(2, "Dr. House"),
    make_user(3, "Bender"),
    make_user(4, "Queen Victoria"),
    make_user(5, "V. Pupkin"),
]

CURRENT_USER = make_user(6, "Dr. Pepper", avatar="core/img/avatar-1.jpg")
CURRENT_USER["login"] = "dr_pepper"
CURRENT_USER["email"] = "drpepper@"

POPULAR_TAGS = [
    {"name": "perl", "css": "text-secondary"},
    {"name": "python", "css": "text-danger fs-5"},
    {"name": "TechnoPark", "css": "text-dark"},
    {"name": "MySQL", "css": "text-danger fs-5"},
    {"name": "django", "css": "text-success"},
    {"name": "Mail.Ru", "css": "text-dark"},
    {"name": "Voloshin", "css": "text-dark"},
    {"name": "Firefox", "css": "text-warning"},
]

BEST_MEMBERS = USERS