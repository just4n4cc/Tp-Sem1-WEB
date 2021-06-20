import random
from faker import Faker
from random import choice
from django.core.management.base import BaseCommand
from ...models import *
from itertools import islice
from django.core.files import File

faker = Faker()
Faker.seed(0)


class Command(BaseCommand):
    def add_arguments(self, parser):
        parser.add_argument("-t", "--tags", type=int)
        parser.add_argument("-u", "--users", type=int)
        parser.add_argument("-q", "--questions", type=int)
        parser.add_argument("-lq", "--likes_question", type=int)
        parser.add_argument("-a", "--answers", type=int)
        parser.add_argument("-la", "--likes_answer", type=int)
        parser.add_argument("-all", "--all", type=int)

    def handle(self, *args, **options):
        num_t = options["tags"]
        num_u = options["users"]
        num_q = options["questions"]
        num_lq = options["likes_question"]
        num_a = options["answers"]
        num_la = options["likes_answer"]
        num = options["all"]

        if num:
            self.fill_with_tags(num)
            self.fill_with_users(num)
            self.fill_with_questions(num * 10)
            self.fill_with_likes_question(num * 100)
            self.fill_with_answers(num * 100)
            self.fill_with_likes_answer(num * 100)
        if num_t:
            self.fill_with_tags(num_t)
        if num_u:
            self.fill_with_users(num_u)
        if num_q:
            self.fill_with_questions(num_q)
        if num_lq:
            self.fill_with_likes_question(num_lq)
        if num_a:
            self.fill_with_answers(num_a)
        if num_la:
            self.fill_with_likes_answer(num_la)

    def fill_with_tags(self, num):
        faker.random.seed(random.randint(1, num))
        separators = [".", ",", ":", ";", "&", "+", "-", "_", "@", "№", "!", "*", "<", ">", "%", "~", "|"]
        objs = (Tag(title=(faker.word()
                           + str(random.randint(-9, 9))
                           + random.choice(separators)
                           + faker.word()
                           + str(random.randint(-9, 9)))) for i in range(num))

        batch_size = 10000
        while True:
            batch = list(islice(objs, batch_size))
            if not batch:
                break
            Tag.objects.bulk_create(batch, batch_size)


    def fill_with_users(self, num):
        images = [
            "allium.png",
            "bee.png",
            "bookshelf.png",
            "bow.png",
            "bread.png",
            "bucket.png",
            "cactus.png",
            "cake.png",
            "carrot.png",
            "clock.png",
            "coal.png",
            "cookie.png",
            "daisy.png",
            "diamond.png",
            "egg.png",
            "fish.png",
            "goat.png",
            "grass.png",
            "honey.png",
            "ifrit.png",
            "lantern.png",
            "leather.png",
            "melon.png",
            "mushroom.png",
            "pig.png",
            "potato.png",
            "rose.png",
            "seeds.png",
            "slime.png",
            "stick.png",
            "sword.png",
            "torch.png",
            "water.png",
        ]
        separators = [".", ",", ":", ";", "&", "+", "-", "_", "@", "№", "!", "*", "<", ">", "%", "~", "|"]
        for i in range(num):
            user = User.objects.create_user(username=(faker.name()
                                            + str(random.randint(-9, 9))
                                            + random.choice(separators)
                                            + str(random.randint(-9, 9))
                                            + faker.user_name()
                                            + str(random.randint(-50, 50))),
                                            password=faker.password(),
                                            email=faker.email())
            obj = Profile(user=user)
            f = open("./static/img/" + images[i % len(images)], "rb")
            obj.avatar = File(f)
            obj.avatar.save(name=("../avatars/" + images[i % len(images)]), content=File(f), save=True)

    def fill_with_questions(self, num):
        authors = list(Profile.objects.values_list("id", flat=True))
        tags = list(Tag.objects.values_list("id", flat=True))
        for i in range(num):
            obj = Question.objects.create(title=(faker.unique.sentence()[:55][:-1] + '?'),
                                          text=faker.unique.paragraph(nb_sentences=11),
                                          author_id=choice(authors),
                                          pub_date=faker.unique.date_time_between("-150d", "now"),
                                          rating=0)
            for j in range(1, random.randint(2, 5)):
                obj.tags.add(choice(tags))

    def fill_with_likes_question(self, num):
        authors = list(Profile.objects.values_list("id", flat=True))
        questions = list(Question.objects.values_list("id", flat=True))
        objs = []
        for i in range(num):
            obj = LikeQuestion(like_status=choice([-1, 1]),
                               author_id=choice(authors),
                               question_id=choice(questions))
            obj.question.like_recalculate(obj.like_status)
            objs.append(obj)

        batch_size = 10000
        while True:
            batch = list(islice(objs, batch_size))
            del objs[:batch_size]
            if not batch:
                break
            LikeQuestion.objects.bulk_create(batch, batch_size)


    def fill_with_answers(self, num):
        authors = list(Profile.objects.values_list("id", flat=True))
        questions = list(Question.objects.values_list("id", flat=True))
        objs = []
        for i in range(num):
            obj = Answer(question_id=choice(questions),
                         text=faker.unique.paragraph(nb_sentences=15),
                         author_id=choice(authors),
                         pub_date=faker.unique.date_time_between("-150d", "now"),
                         rating=0,
                         is_correct=bool(random.getrandbits(1)))
            objs.append(obj)

        batch_size = 10000
        while True:
            batch = list(islice(objs, batch_size))
            del objs[:batch_size]
            if not batch:
                break
            Answer.objects.bulk_create(batch, batch_size)

    def fill_with_likes_answer(self, num):
        authors = list(Profile.objects.values_list("id", flat=True))
        answers = list(Answer.objects.values_list("id", flat=True))
        objs = []
        for i in range(num):
            obj = LikeAnswer(like_status=choice([-1, 1]),
                             author_id=choice(authors),
                             answer_id=choice(answers))
            obj.answer.like_recalculate(obj.like_status)
            objs.append(obj)

        batch_size = 10000
        while True:
            batch = list(islice(objs, batch_size))
            del objs[:batch_size]
            if not batch:
                break
            LikeAnswer.objects.bulk_create(batch, batch_size)
