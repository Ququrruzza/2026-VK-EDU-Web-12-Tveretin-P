from django.contrib.auth.decorators import login_required
from django.contrib.auth.views import redirect_to_login
from django.http import JsonResponse
from django.shortcuts import get_object_or_404, redirect, render
from django.views.decorators.http import require_POST

from core.utils import paginate
from .forms import AnswerForm, AnswerLikeForm, CorrectAnswerForm, QuestionForm, QuestionLikeForm
from .models import ANSWERS_PER_PAGE, Answer, Question, Tag
# Create your views here.

def questions_list(request, template, questions, context=None):
    context = context or {}
    context["page"] = paginate(questions, request)
    return render(request, template, context)


def index(request):
    return questions_list(request, "questions/index.html", Question.objects.new(request.user))


def hot(request):
    return questions_list(request, "questions/hot.html", Question.objects.hot(request.user))


def tag(request, tag_name):
    tag = get_object_or_404(Tag, name=tag_name)
    return questions_list(request, "questions/tag.html", Question.objects.by_tag(tag, request.user), {"tag": tag})


def question(request, question_id):
    question = get_object_or_404(Question.objects.with_related(request.user), id=question_id)
    form = AnswerForm(request.POST or None)
    if request.method == "POST":
        if not request.user.is_authenticated:
            return redirect_to_login(request.get_full_path())
        if form.is_valid():
            return redirect(form.save(request.user, question))
    page = paginate(Answer.objects.for_question(question, request.user), request, per_page=ANSWERS_PER_PAGE)
    return render(request, "questions/question.html", {"question": question, "page": page, "form": form})


@login_required
def ask(request):
    form = QuestionForm(request.POST or None)
    if request.method == "POST" and form.is_valid():
        return redirect(form.save(request.user))
    return render(request, "questions/ask.html", {"form": form})


# общая обработка AJAX-запросов: проверка авторизации, валидация формы, JSON в ответ
def ajax_form_response(request, form_class):
    if not request.user.is_authenticated:
        return JsonResponse({"error": "Войдите, чтобы выполнить это действие."}, status=401)
    form = form_class(request.user, request.POST)
    if not form.is_valid():
        errors = [error for field_errors in form.errors.values() for error in field_errors]
        return JsonResponse({"error": " ".join(errors)}, status=400)
    return JsonResponse(form.save())


@require_POST
def question_like(request):
    return ajax_form_response(request, QuestionLikeForm)


@require_POST
def answer_like(request):
    return ajax_form_response(request, AnswerLikeForm)


@require_POST
def correct_answer(request):
    return ajax_form_response(request, CorrectAnswerForm)
