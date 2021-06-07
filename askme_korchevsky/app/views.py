from django.contrib.auth.decorators import login_required
from django.contrib import auth
from django.shortcuts import redirect
from django.core.paginator import InvalidPage, Paginator
from django.shortcuts import render, reverse
from django import conf
from urllib.parse import urlparse

from django.contrib.auth.models import User
from app.models import Tag, Question, Answer, Profile
from app.forms import LoginForm, SignupForm, QuestionForm, SettingsForm


pop_tags_color = [
    'text-primary',
    'text-danger',
    'text-dark',
    'text-warning',
    'text-success',
    'text-secondary',
    'text-info',
]


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
    zipped_list = zip(pop_tags, pop_tags_color)
    return render(request, 'index.html', {'questions': new_q_list, 'pop_tags': zipped_list, 'page_list': new_q_list})


def hot_questions(request):
    hot_q_list = paginate(Question.objects.hot_questions(), request)
    pop_tags = Tag.objects.pop_tags()
    zipped_list = zip(pop_tags, pop_tags_color)
    return render(request, 'hot_questions.html', {'questions': hot_q_list, 'pop_tags': zipped_list, 'page_list': hot_q_list})


def question(request, pk):
    one_q = Question.objects.one_question(pk)
    pop_tags = Tag.objects.pop_tags()
    answers = paginate(Answer.objects.by_q(pk).order_by('-rating'), request, 5)
    # answers = Answer.objects.by_q(pk).order_by('-rating')
    zipped_list = zip(pop_tags, pop_tags_color)
    return render(request, 'question.html', {'question': one_q, 'answers': answers, 'pop_tags': zipped_list, 'page_list': answers})


@login_required
def settings(request):
    pop_tags = Tag.objects.pop_tags()
    zipped_list = zip(pop_tags, pop_tags_color)
    form = SettingsForm()
    if request.method == 'GET':
        print(request.user)
        form.username = request.user.username
        form.email = request.user.email
        form.password = request.user.password
        form.avatar = request.user.profile.avatar
        return render(request, 'settings.html', {'pop_tags': zipped_list, 'form': form})

    return render(request, 'settings.html', {'pop_tags': zipped_list, 'form': form})


def login(request):
    pop_tags = Tag.objects.pop_tags()
    zipped_list = zip(pop_tags, pop_tags_color)
    if request.method == 'GET':
        form = LoginForm()
        if not request.GET.get('next'):
            return redirect('%s?next=%s' % (conf.settings.LOGIN_URL, urlparse(request.META.get('HTTP_REFERER')).path))
    else:
        next_path = request.POST.get('next')
        form = LoginForm(data=request.POST)
        if form.is_valid():
            user = auth.authenticate(request, **form.cleaned_data)
            if user is not None:
                auth.login(request, user)
                if not next_path:
                    next_path = 'index'
                return redirect(next_path)

    return render(request, 'login.html', {'pop_tags': zipped_list, 'form': form})


def logout(request):
    auth.logout(request)
    return redirect(request.META.get('HTTP_REFERER'))


def signup(request):
    pop_tags = Tag.objects.pop_tags()
    zipped_list = zip(pop_tags, pop_tags_color)
    if request.method == 'GET':
        form = SignupForm()
    else:
        form = SignupForm(request.POST, request.FILES)
        if form.is_valid():
            u = form.save(commit=False)
            u = User.objects.create_user(u.username, u.email, form.cleaned_data['password'])
            p = Profile(user=u, avatar=form.cleaned_data['avatar'])
            p.save()
            user = auth.authenticate(username=p.user.username, password=form.cleaned_data['password'])
            if user is not None:
                auth.login(request, user)
                return redirect(reverse('index'))

    return render(request, 'signup.html', {'pop_tags': zipped_list, 'form': form})


def tag(request, tag):
    tag_q_list = paginate(Question.objects.tag_questions(tag), request, 5)
    pop_tags = Tag.objects.pop_tags()
    zipped_list = zip(pop_tags, pop_tags_color)
    return render(request, 'tag.html', {'tag': tag, 'questions': tag_q_list, 'pop_tags': zipped_list})


@login_required
def ask(request):
    pop_tags = Tag.objects.pop_tags()
    zipped_list = zip(pop_tags, pop_tags_color)
    if request.method == 'GET':
        form = QuestionForm()
    else:
        form = QuestionForm(data=request.POST)
        if form.is_valid():
            q = form.save(commit=False)
            q.author = request.user.profile
            q.save()
            return redirect(reverse('question', kwargs={'pk': q.pk}))

    return render(request, 'ask.html', {'pop_tags': zipped_list, 'form': form})
