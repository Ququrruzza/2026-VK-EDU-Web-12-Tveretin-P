from django.shortcuts import get_object_or_404, render

from core.utils import paginate
from .models import Answer, Question, Tag
# Create your views here.

def questions_list(request, template, questions, context=None):
    context = context or {}
    context["page"] = paginate(questions, request)
    return render(request, template, context)


def index(request):
    return questions_list(request, "questions/index.html", Question.objects.new())


def hot(request):
    return questions_list(request, "questions/hot.html", Question.objects.hot())


def tag(request, tag_name):
    tag = get_object_or_404(Tag, name=tag_name)
    return questions_list(request, "questions/tag.html", Question.objects.by_tag(tag), {"tag": tag})


def question(request, question_id):
    question = get_object_or_404(Question.objects.with_related(), id=question_id)
    page = paginate(Answer.objects.for_question(question), request, per_page=5)
    return render(request, "questions/question.html", {"question": question, "page": page})


def ask(request):
    return render(request, "questions/ask.html")
