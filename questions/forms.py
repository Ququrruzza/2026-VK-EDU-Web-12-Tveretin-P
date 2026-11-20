from django import forms
from django.core.exceptions import ValidationError
from django.db import transaction
from django.db.models import F

from core.forms import BootstrapFormMixin

from .models import LIKE_CHOICES, Answer, AnswerLike, Question, QuestionLike, Tag

MAX_TAGS = 3


class QuestionForm(BootstrapFormMixin, forms.ModelForm):
    tags = forms.CharField(label="Tags", max_length=150, help_text="Up to 3 tags separated by commas.")

    class Meta:
        model = Question
        fields = ["title", "text"]
        labels = {"title": "Title", "text": "Text"}
        help_texts = {"title": "Short and clear, up to 120 characters."}
        widgets = {"text": forms.Textarea(attrs={"rows": 8})}

    def clean_tags(self):
        tags = []
        for name in self.cleaned_data["tags"].split(","):
            name = name.strip().lower()
            if name and name not in tags:
                tags.append(name)
        if not tags:
            raise ValidationError("Укажите хотя бы один тег.")
        if len(tags) > MAX_TAGS:
            raise ValidationError(f"Можно указать не больше {MAX_TAGS} тегов.")
        if any(len(name) > 50 for name in tags):
            raise ValidationError("Тег не может быть длиннее 50 символов.")
        return tags

    @transaction.atomic
    def save(self, author):
        question = super().save(commit=False)
        question.author = author
        question.save()
        for name in self.cleaned_data["tags"]:
            tag, _ = Tag.objects.get_or_create(name=name)
            question.tags.add(tag)
        return question


class AnswerForm(BootstrapFormMixin, forms.ModelForm):
    class Meta:
        model = Answer
        fields = ["text"]
        labels = {"text": "Your answer"}
        widgets = {"text": forms.Textarea(attrs={"rows": 5, "placeholder": "Enter your answer here..."})}

    @transaction.atomic
    def save(self, author, question):
        answer = super().save(commit=False)
        answer.author = author
        answer.question = question
        answer.save()
        Question.objects.filter(id=question.id).update(answers_count=F("answers_count") + 1)
        return answer


# общая логика лайка, в наследниках указывается поле объекта и модель лайка
class LikeForm(forms.Form):
    value = forms.TypedChoiceField(choices=LIKE_CHOICES, coerce=int)
    object_field = None
    like_model = None

    def __init__(self, user, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.user = user

    def clean(self):
        cleaned_data = super().clean()
        obj = cleaned_data.get(self.object_field)
        value = cleaned_data.get("value")
        if obj and value:
            already = self.like_model.objects.filter(user=self.user, value=value, **{self.object_field: obj})
            if already.exists():
                raise ValidationError("Вы уже поставили такую оценку.")
        return cleaned_data

    @transaction.atomic
    def save(self):
        obj = self.cleaned_data[self.object_field]
        value = self.cleaned_data["value"]
        like, created = self.like_model.objects.get_or_create(
            user=self.user, defaults={"value": value}, **{self.object_field: obj}
        )
        # если оценка меняется с лайка на дизлайк, рейтинг сдвигается на 2
        delta = value if created else value - like.value
        if not created:
            like.value = value
            like.save(update_fields=["value"])
        type(obj).objects.filter(id=obj.id).update(rating=F("rating") + delta)
        obj.refresh_from_db(fields=["rating"])
        return {"rating": obj.rating, "value": value}


class QuestionLikeForm(LikeForm):
    question = forms.ModelChoiceField(queryset=Question.objects.all())
    object_field = "question"
    like_model = QuestionLike


class AnswerLikeForm(LikeForm):
    answer = forms.ModelChoiceField(queryset=Answer.objects.all())
    object_field = "answer"
    like_model = AnswerLike


class CorrectAnswerForm(forms.Form):
    question = forms.ModelChoiceField(queryset=Question.objects.all())
    answer = forms.ModelChoiceField(queryset=Answer.objects.all())

    def __init__(self, user, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.user = user

    def clean(self):
        cleaned_data = super().clean()
        question = cleaned_data.get("question")
        answer = cleaned_data.get("answer")
        if question and answer:
            if answer.question_id != question.id:
                raise ValidationError("Этот ответ относится к другому вопросу.")
            if question.author_id != self.user.id:
                raise ValidationError("Отмечать правильный ответ может только автор вопроса.")
        return cleaned_data

    @transaction.atomic
    def save(self):
        answer = self.cleaned_data["answer"]
        answer.is_correct = not answer.is_correct
        # правильный ответ у вопроса может быть только один
        if answer.is_correct:
            Answer.objects.filter(question_id=answer.question_id, is_correct=True).update(is_correct=False)
        answer.save(update_fields=["is_correct"])
        return {"answer": answer.id, "is_correct": answer.is_correct}
