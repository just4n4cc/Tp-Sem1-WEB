from django.core.paginator import InvalidPage, Paginator
from django.shortcuts import render

questions = [
    {
        'id': idx,
        'title': f'Title number {idx}',
        'text': f'Some text for question #{idx}'
    } for idx in range(30)
]

pop_tags = [
    {
        'id': 0,
        'title': f'perl',
        'color': f''
    },
    {
        'id': 1,
        'title': f'python',
        'color': f'text-danger'
    },
    {
        'id': 2,
        'title': f'TechnoPark',
        'color': f'text-dark'
    },
    {
        'id': 3,
        'title': f'MySQL',
        'color': f'text-danger'
    },
    {
        'id': 4,
        'title': f'django',
        'color': f'text-success'
    },
    {
        'id': 5,
        'title': f'Mail.Ru',
        'color': f''
    },
    {
        'id': 6,
        'title': f'Google',
        'color': f''
    }
]

def paginate(list, request, per_page=10):
    paginator = Paginator(list, per_page)
    page = request.GET.get('page')
    try:
        new_list = paginator.get_page(page)
    except InvalidPage:
        return paginator.page(1)
    return new_list


def index(request):
    list = paginate(questions, request)
    return render(request, 'index.html', {'questions': list, 'pop_tags': pop_tags})


def hot_questions(request):
    list = paginate(questions, request)
    return render(request, 'hot_questions.html', {'questions': list, 'pop_tags': pop_tags})


def question(request, pk):
    question = questions[pk]
    return render(request, 'question.html', {'question': question, 'pop_tags': pop_tags})


def settings(request):
    return render(request, 'settings.html', {'pop_tags': pop_tags})


def login(request):
    return render(request, 'login.html', {'pop_tags': pop_tags})


def signup(request):
    return render(request, 'signup.html', {'pop_tags': pop_tags})


def tag(request, tag):
    list = paginate(questions, request, 5)
    return render(request, 'tag.html', {'questions': list, 'pop_tags': pop_tags, 'tag': tag})


def ask(request):
    return render(request, 'ask.html', {'pop_tags': pop_tags})
