from django.shortcuts import render

questions = [
    {
        'id': idx,
        'title': f'Title number {idx}',
        'text': f'Some text for question #{idx}'
    } for idx in range(10)
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


def index(request):
    return render(request, 'index.html', {'questions': questions, 'pop_tags': pop_tags})


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
    return render(request, 'tag.html', {'questions': questions, 'pop_tags': pop_tags, 'tag': tag})


def ask(request):
    return render(request, 'ask.html', {'pop_tags': pop_tags})
