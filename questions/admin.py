from django.contrib import admin

from .models import Answer, AnswerLike, Question, QuestionLike, Tag


class AnswerInline(admin.TabularInline):
    model = Answer
    fields = ("author", "text", "is_correct", "rating", "created_at")
    readonly_fields = ("author",)
    extra = 0

    def get_queryset(self, request):
        return super().get_queryset(request).select_related("author")

    # новые ответы добавляются в разделе "Ответы", здесь только список и редактирование
    def has_add_permission(self, request, obj=None):
        return False


@admin.register(Question)
class QuestionAdmin(admin.ModelAdmin):
    list_display = ("id", "title", "author", "rating", "answers_count", "created_at")
    list_select_related = ("author",)
    list_filter = ("created_at",)
    search_fields = ("title",)
    raw_id_fields = ("author",)
    autocomplete_fields = ("tags",)
    inlines = [AnswerInline]
    show_full_result_count = False


@admin.register(Tag)
class TagAdmin(admin.ModelAdmin):
    list_display = ("id", "name", "created_at")
    list_filter = ("created_at",)
    search_fields = ("name",)


@admin.register(Answer)
class AnswerAdmin(admin.ModelAdmin):
    list_display = ("id", "question", "author", "is_correct", "rating", "created_at")
    list_select_related = ("question", "author")
    list_filter = ("is_correct", "created_at")
    search_fields = ("=question__id",)
    raw_id_fields = ("question", "author")
    ordering = ("-id",)
    show_full_result_count = False


@admin.register(QuestionLike)
class QuestionLikeAdmin(admin.ModelAdmin):
    list_display = ("id", "user", "question", "value", "created_at")
    list_select_related = ("user", "question")
    list_filter = ("value", "created_at")
    search_fields = ("=question__id",)
    raw_id_fields = ("user", "question")
    ordering = ("-id",)
    show_full_result_count = False


@admin.register(AnswerLike)
class AnswerLikeAdmin(admin.ModelAdmin):
    list_display = ("id", "user", "answer", "value", "created_at")
    list_select_related = ("user", "answer")
    list_filter = ("value", "created_at")
    search_fields = ("=answer__id",)
    raw_id_fields = ("user", "answer")
    ordering = ("-id",)
    show_full_result_count = False
