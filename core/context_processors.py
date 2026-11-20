from django.core.cache import cache

from questions.models import Tag

from .models import Profile


# сайдбар считается по всей базе, поэтому кешируем его на 5 минут
def sidebar(request):
    return {
        "popular_tags": cache.get_or_set("popular_tags", lambda: list(Tag.objects.popular()), 300),
        "best_members": cache.get_or_set("best_members", lambda: list(Profile.objects.best()), 300),
    }
