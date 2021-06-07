from django.db import models
from django.db.models import Count
from django.contrib.auth.models import User

# ################ MANAGERS ################


class QuestionManger(models.Manager):
    def hot_questions(self):
        req_q = self.all().order_by('-rating')
        return req_q.annotate(number_of_answers=Count('answer'))

    def new_questions(self):
        req_q = self.all().order_by('-pub_date')
        return req_q.annotate(number_of_answers=Count('answer'))

    def tag_questions(self, tag):
        req_q = self.all().filter(tags__title__exact = tag)
        return req_q.annotate(number_of_answers=Count('answer'))

    def one_question(self, pk):
        req_q = self.all().get(id=pk)
        return req_q

    def get_answers_num(self):
        req_q = Answer.objects.filter(question=self.pk).count()
        return req_q.annotate(number_of_answers=Count('answer'))


class TagManager(models.Manager):
    def pop_tags(self):
        return self.filter(id__in=(Question.objects.all().values_list('tags', flat=True)\
                           .annotate(count=Count('id')).order_by('-count').values_list('id', flat=True))).distinct()[:7]


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
    tags = models.ManyToManyField(Tag, default=[])
    rating = models.IntegerField(default=0)

    objects = QuestionManger()

    def __str__(self):
        return self.title

    def like_recalculate(self, like):
        self.rating = self.rating + like
        self.save()

    class Meta:
        verbose_name = 'Question'
        verbose_name_plural = 'Questions'


class Answer(models.Model):
    question = models.ForeignKey(Question, on_delete=models.CASCADE)
    text = models.TextField(max_length=500)
    author = models.ForeignKey(Profile, on_delete=models.CASCADE)
    pub_date = models.DateTimeField(auto_now_add=True)
    is_correct = models.BooleanField()
    rating = models.IntegerField()

    objects = AnswerManager()

    def __str__(self):
        return 'Answer from: ' + self.author.user.username

    def like_recalculate(self, like):
        self.rating = self.rating + like
        self.save()

    class Meta:
        verbose_name = 'Answer'
        verbose_name_plural = 'Answers'


class LikeQuestion(models.Model):
    LIKE = 1
    DISLIKE = -1
    LIKE_CHOICES = [
        (LIKE, 'LIKE'),
        (DISLIKE, 'DISLIKE'),
    ]
    like_status = models.IntegerField(choices=LIKE_CHOICES)
    author = models.ForeignKey(Profile, on_delete=models.CASCADE)
    question = models.ForeignKey(Question, on_delete=models.CASCADE)

    def __str__(self):
        return self.get_like_status_display()

    class Meta:
        verbose_name = 'Question Like'
        verbose_name_plural = 'Question Likes'


class LikeAnswer(models.Model):
    LIKE = 1
    DISLIKE = -1
    LIKE_CHOICES = [
        (LIKE, 'LIKE'),
        (DISLIKE, 'DISLIKE'),
    ]
    like_status = models.IntegerField(choices=LIKE_CHOICES)
    author = models.ForeignKey(Profile, on_delete=models.CASCADE)
    answer = models.ForeignKey(Answer, on_delete=models.CASCADE)

    def __str__(self):
        return self.get_like_status_display()

    class Meta:
        verbose_name = 'Answer Like'
        verbose_name_plural = 'Answer Likes'
