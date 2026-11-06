from django.shortcuts import render
from django.http import Http404
from core.utils import paginate
from .mock_data import QUESTIONS, get_answers
# Create your views here.

def index(request):
    page = paginate(QUESTIONS, request)
    return render(request, "questions/index.html", {"page": page})


def hot(request):
    hot_questions = sorted(QUESTIONS, key=lambda question: question["rating"], reverse=True)
    page = paginate(hot_questions, request)
    return render(request, "questions/hot.html", {"page": page})


def tag(request, tag_name):
    tagged_questions = [question for question in QUESTIONS if tag_name in question["tags"]]
    page = paginate(tagged_questions, request)
    return render(request, "questions/tag.html", {"page": page, "tag_name": tag_name})


def question(request, question_id):
    if not 1 <= question_id <= len(QUESTIONS):
        raise Http404("Question not found")

    current_question = QUESTIONS[question_id - 1]
    page = paginate(get_answers(current_question), request, per_page=5)
    return render(request, "questions/question.html", {"question": current_question, "page": page})


def ask(request):
    return render(request, "questions/ask.html")