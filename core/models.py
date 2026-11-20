import os
import uuid

from django.contrib.auth.models import User
from django.db import models
from django.db.models import Count

AVATAR_COLORS = ["#0d6efd", "#198754", "#dc3545", "#6f42c1", "#fd7e14", "#20c997"]


# случайное имя файла, чтобы аватарки нельзя было перебрать по адресу
def avatar_upload_to(instance, filename):
    extension = os.path.splitext(filename)[1].lower()
    return f"avatars/{uuid.uuid4().hex}{extension}"


class ProfileManager(models.Manager):
    def best(self):
        return self.select_related("user").annotate(answers_total=Count("user__answers")).order_by("-answers_total")[:10]


class Profile(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE, related_name="profile", verbose_name="пользователь")
    nickname = models.CharField("никнейм", max_length=30, blank=True)
    avatar = models.ImageField("аватар", upload_to=avatar_upload_to, blank=True, null=True)

    objects = ProfileManager()

    class Meta:
        verbose_name = "профиль"
        verbose_name_plural = "профили"

    def __str__(self):
        return self.display_name()

    def display_name(self):
        return self.nickname or self.user.username

    def initials(self):
        words = self.display_name().split()
        return "".join(word[0] for word in words[:2]).upper()

    def color(self):
        return AVATAR_COLORS[self.user_id % len(AVATAR_COLORS)]

    def avatar_url(self):
        if self.avatar:
            return self.avatar.url
        return None
