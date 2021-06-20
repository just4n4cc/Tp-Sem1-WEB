from django.contrib.auth.decorators import login_required
from django.contrib import auth
from django.shortcuts import redirect
from django.core.paginator import InvalidPage, Paginator
from django.shortcuts import render, reverse
from django import conf
from urllib.parse import urlparse

from django.contrib.auth.models import User
from app.models import Tag, Question, Answer, Profile
from app.forms import LoginForm, SignupForm, QuestionForm, SettingsForm, AnswerForm


pop_tags_color = [
    'text-primary',
    'text-danger',
    'text-dark',
    'text-warning',
    'text-success',
    'text-secondary',
    'text-info',
]


def paginate(content_list, request, per_page=10, last=False):
    paginator = Paginator(content_list, per_page)
    if last:
        page = paginator.num_pages
    else:
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
    request.path += '#lala'
    print(request.path)
    one_q = Question.objects.one_question(pk)
    pop_tags = Tag.objects.pop_tags()
    answers = paginate(Answer.objects.by_q(pk), request, 5)
    zipped_list = zip(pop_tags, pop_tags_color)
    form = AnswerForm()
    if request.method == 'POST':
        if not request.user.is_authenticated:
            form = AnswerForm(data=request.POST)
            form.add_error(None, "You have to log in to leave any answers!")
        else:
            Answer.objects.create(
                question=one_q,
                text=request.POST.get('answer'),
                author=request.user.profile
            )
            answers = paginate(Answer.objects.by_q(pk).order_by(), request, 5, True)

    return render(request, 'question.html', {
        'question': one_q,
        'answers': answers,
        'pop_tags': zipped_list,
        'form': form,
        'page_list': answers})


@login_required
def settings(request):
    pop_tags = Tag.objects.pop_tags()
    zipped_list = zip(pop_tags, pop_tags_color)
    if request.method == 'GET':
        form = SettingsForm(initial={'username': request.user.username, 'email': request.user.email, 'avatar': request.user.profile.avatar})
    else:
        form = SettingsForm({'username': request.POST.get('username'), 'email': request.POST.get('email'), 'avatar': request.POST.get('avatar')})
        if form.is_valid():
            u = request.user
            u.email = form.cleaned_data['email']
            u.username = form.cleaned_data['username']
            u.save()
            if request.FILES.get('avatar') is not None:
                u.profile.avatar = request.FILES.get('avatar')
            u.profile.save()
            form = SettingsForm(initial={'username': u.username, 'email': u.email, 'avatar': u.profile.avatar})

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
    return render(request, 'tag.html', {'tag': tag, 'questions': tag_q_list, 'pop_tags': zipped_list, 'page_list': tag_q_list})


@login_required
def ask(request):
    pop_tags = Tag.objects.pop_tags()
    zipped_list = zip(pop_tags, pop_tags_color)
    if request.method == 'GET':
        form = QuestionForm()
    else:
        form = QuestionForm({'title': request.POST.get('title'), 'text': request.POST.get('text')})
        if form.is_valid():
            # raise
            q = form.save(commit=False)
            q.author = request.user.profile
            tags = []
            for i in range(5):
                if request.POST.get('tags_' + str(i)) != '' and request.POST.get('tags_' + str(i)) not in tags:
                    if not Tag.objects.filter(title=request.POST.get('tags_' + str(i))):
                        Tag.objects.create(title=request.POST.get('tags_' + str(i)))
                    tags.append(request.POST.get('tags_' + str(i)))
            q.save()
            q.tags.set(Tag.objects.filter(title__in=tags))
            q.save()
            return redirect(reverse('question', kwargs={'pk': q.pk}))

    return render(request, 'ask.html', {'pop_tags': zipped_list, 'form': form})
