from django.db import models
# from django.db.models import Count
from django.contrib.auth.models import User

# ################ MANAGERS ################


class QuestionManger(models.Manager):
    def hot_questions(self):
        return self.all().annotate(likes_count=(LikeQuestion.objects.filter(question__exact=self)\
            .count())).order_by('-likes_count')

    def new_questions(self):
        return self.all().order_by('-pub_date')

    def tag_questions(self, tag):
        return self.all().filter(tags__title__contains=tag)

    def one_question(self, pk):
        return self.all().get(id=pk)


class TagManager(models.Manager):
    def pop_tags(self):
        # return self.all().filter(id__in=(Question.objects.hot_questions().values_list('question_tags', flat=True)))\
        # .distinct()[:7]
        return self.all()


class AnswerManager(models.Manager):
    def by_q(self, q_id):
        return self.filter(question_id=q_id)


# ################ MODELS ################


class Profile(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE)
    avatar = models.ImageField(upload_to='avatars/', blank=True)

    def __str__(self):
        return self.user.username

    class Meta:
        verbose_name = 'Profile'
        verbose_name_plural = 'Profiles'


class Tag(models.Model):
    title = models.CharField(max_length=50, unique=True)

    def __str__(self):
        return self.title

    objects = TagManager()

    class Meta:
        verbose_name = 'Tag'
        verbose_name_plural = 'Tags'


class Question(models.Model):
    title = models.CharField(max_length=255)
    text = models.TextField(max_length=500)
    author = models.ForeignKey(Profile, on_delete=models.CASCADE)
    pub_date = models.DateTimeField(auto_now_add=True)
    tags = models.ManyToManyField(Tag)
    # rating = models.IntegerField()

    objects = QuestionManger()

    def __str__(self):
        return self.title

    class Meta:
        verbose_name = 'Question'
        verbose_name_plural = 'Questions'


class Answer(models.Model):
    question = models.ForeignKey(Question, on_delete=models.CASCADE)
    text = models.TextField(max_length=500)
    author = models.ForeignKey(Profile, on_delete=models.CASCADE)
    pub_date = models.DateTimeField(auto_now_add=True)
    is_correct = models.BooleanField()

    objects = AnswerManager()

    def __str__(self):
        return 'Answer from: ' + self.author.user.username

    class Meta:
        verbose_name = 'Answer'
        verbose_name_plural = 'Answers'


class Like(models.Model):
    LIKE = 1
    # NOTHING = 0
    DISLIKE = -1
    LIKE_CHOICES = [
        (LIKE, 'LIKE'),
        # (NOTHING, 'NOTHING'),
        (DISLIKE, 'DISLIKE'),
    ]
    like_status = models.IntegerField(choices=LIKE_CHOICES)
    author = models.ForeignKey(Profile, on_delete=models.CASCADE)
    # like_status = models.IntegerField(choices=LIKE_CHOICES, default=NOTHING)

    def __str__(self):
        return self.get_like_status_display()

    class Meta:
        verbose_name = 'Like'
        verbose_name_plural = 'Likes'


class LikeQuestion(Like):
    question = models.ForeignKey(Question, on_delete=models.CASCADE)


class LikeAnswer(Like):
    answer = models.ForeignKey(Answer, on_delete=models.CASCADE)