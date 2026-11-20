from django.contrib.auth.models import User
from django.db import models
from django.db.models import Count
from django.urls import reverse
from django.utils import timezone


class TagManager(models.Manager):
    def popular(self):
        return self.annotate(questions_total=Count("questions")).order_by("-questions_total")[:10]


class Tag(models.Model):
    name = models.CharField("название", max_length=50, unique=True)
    created_at = models.DateTimeField("дата создания", default=timezone.now)

    objects = TagManager()

    class Meta:
        verbose_name = "тег"
        verbose_name_plural = "теги"

    def __str__(self):
        return self.name

    def get_absolute_url(self):
        return reverse("tag", args=[self.name])


class QuestionManager(models.Manager):
    def with_related(self):
        return self.select_related("author__profile").prefetch_related("tags")

    def new(self):
        return self.with_related().order_by("-created_at")

    def hot(self):
        return self.with_related().order_by("-rating", "-created_at")

    def by_tag(self, tag):
        return self.new().filter(tags=tag)


class Question(models.Model):
    author = models.ForeignKey(User, on_delete=models.CASCADE, related_name="questions", verbose_name="автор")
    title = models.CharField("заголовок", max_length=120)
    text = models.TextField("текст")
    tags = models.ManyToManyField(Tag, related_name="questions", blank=True, verbose_name="теги")
    created_at = models.DateTimeField("дата создания", default=timezone.now, db_index=True)
    rating = models.IntegerField("рейтинг", default=0, db_index=True)
    answers_count = models.PositiveIntegerField("количество ответов", default=0)

    objects = QuestionManager()

    class Meta:
        verbose_name = "вопрос"
        verbose_name_plural = "вопросы"

    def __str__(self):
        return self.title

    def get_absolute_url(self):
        return reverse("question", args=[self.id])


class AnswerManager(models.Manager):
    def for_question(self, question):
        return self.filter(question=question).select_related("author__profile").order_by("-is_correct", "-rating", "created_at")


class Answer(models.Model):
    question = models.ForeignKey(Question, on_delete=models.CASCADE, related_name="answers", verbose_name="вопрос")
    author = models.ForeignKey(User, on_delete=models.CASCADE, related_name="answers", verbose_name="автор")
    text = models.TextField("текст")
    is_correct = models.BooleanField("правильный ответ", default=False)
    created_at = models.DateTimeField("дата создания", default=timezone.now)
    rating = models.IntegerField("рейтинг", default=0)

    objects = AnswerManager()

    class Meta:
        verbose_name = "ответ"
        verbose_name_plural = "ответы"

    def __str__(self):
        return f"Ответ #{self.id}"


LIKE_CHOICES = [(1, "лайк"), (-1, "дизлайк")]


class QuestionLike(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE, related_name="question_likes", verbose_name="пользователь")
    question = models.ForeignKey(Question, on_delete=models.CASCADE, related_name="likes", verbose_name="вопрос")
    value = models.SmallIntegerField("оценка", choices=LIKE_CHOICES, default=1)
    created_at = models.DateTimeField("дата", default=timezone.now)

    class Meta:
        verbose_name = "оценка вопроса"
        verbose_name_plural = "оценки вопросов"
        unique_together = ("user", "question")

    def __str__(self):
        return f"{self.user_id} -> {self.question_id}: {self.value}"


class AnswerLike(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE, related_name="answer_likes", verbose_name="пользователь")
    answer = models.ForeignKey(Answer, on_delete=models.CASCADE, related_name="likes", verbose_name="ответ")
    value = models.SmallIntegerField("оценка", choices=LIKE_CHOICES, default=1)
    created_at = models.DateTimeField("дата", default=timezone.now)

    class Meta:
        verbose_name = "оценка ответа"
        verbose_name_plural = "оценки ответов"
        unique_together = ("user", "answer")

    def __str__(self):
        return f"{self.user_id} -> {self.answer_id}: {self.value}"
