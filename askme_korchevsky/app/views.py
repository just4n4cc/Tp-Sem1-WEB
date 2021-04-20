from django.core.paginator import InvalidPage, Paginator
from django.shortcuts import render

from app.models import Tag, Question, Answer


def paginate(content_list, request, per_page=10):
    paginator = Paginator(content_list, per_page)
    page = request.GET.get('page')
    try:
        new_list = paginator.get_page(page)
    except InvalidPage:
        return paginator.page(1)
    return new_list


def index(request):
    new_q_list = paginate(Question.objects.new_questions(), request)
    pop_tags = Tag.objects.pop_tags()
    return render(request, 'index.html', {'questions': new_q_list, 'pop_tags': pop_tags})


def hot_questions(request):
    hot_q_list = paginate(Question.objects.new_questions(), request)
    pop_tags = Tag.objects.pop_tags()
    return render(request, 'hot_questions.html', {'questions': hot_q_list, 'pop_tags': pop_tags})


def question(request, pk):
    one_q = Question.objects.one_question(pk)
    pop_tags = Tag.objects.pop_tags()
    answers = Answer.objects.by_q(pk)
    return render(request, 'question.html', {'question': one_q, 'answers': answers, 'pop_tags': pop_tags})


def settings(request):
    pop_tags = Tag.objects.pop_tags()
    return render(request, 'settings.html', {'pop_tags': pop_tags})


def login(request):
    pop_tags = Tag.objects.pop_tags()
    return render(request, 'login.html', {'pop_tags': pop_tags})


def signup(request):
    pop_tags = Tag.objects.pop_tags()
    return render(request, 'signup.html', {'pop_tags': pop_tags})


def tag(request, tag):
    tag_q_list = paginate(Question.objects.tag_questions(tag), request, 5)
    pop_tags = Tag.objects.pop_tags()
    return render(request, 'tag.html', {'questions': tag_q_list, 'pop_tags': pop_tags, 'tag': tag})


def ask(request):
    pop_tags = Tag.objects.pop_tags()
    return render(request, 'ask.html', {'pop_tags': pop_tags})
