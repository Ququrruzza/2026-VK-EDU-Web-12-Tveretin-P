import random
from datetime import timedelta

from django.contrib.auth.hashers import make_password
from django.contrib.auth.models import User
from django.core.management.base import BaseCommand
from django.db.models import Count, OuterRef, Subquery, Sum
from django.db.models.functions import Coalesce
from django.utils import timezone
from faker import Faker

from core.models import Profile
from questions.models import Answer, AnswerLike, Question, QuestionLike, Tag

BATCH_SIZE = 5000
fake = Faker("ru_RU")


def random_date():
    return timezone.now() - timedelta(days=random.randint(0, 365), minutes=random.randint(0, 1440))


class Command(BaseCommand):
    help = "Заполняет базу тестовыми данными"

    def add_arguments(self, parser):
        parser.add_argument("ratio", type=int)

    def handle(self, *args, **options):
        ratio = options["ratio"]

        users = self.create_users(ratio)
        tags = self.create_tags(ratio)
        questions = self.create_questions(ratio * 10, users, tags)
        answers = self.create_answers(ratio * 100, users, questions)
        self.create_likes(ratio * 200, users, questions, answers)
        self.update_counters(questions, answers)

        self.stdout.write(self.style.SUCCESS("Готово"))

    def create_users(self, count):
        # пароль хешируется долго, поэтому делаем это один раз для всех
        password = make_password("password")
        start = User.objects.count()

        users = []
        for i in range(count):
            username = f"{fake.user_name()}_{start + i}"
            users.append(User(
                username=username,
                email=f"{username}@example.com",
                first_name=fake.first_name(),
                last_name=fake.last_name(),
                password=password,
            ))
        users = User.objects.bulk_create(users, batch_size=BATCH_SIZE)

        profiles = [Profile(user=user, nickname=f"{user.first_name} {user.last_name}"[:30]) for user in users]
        Profile.objects.bulk_create(profiles, batch_size=BATCH_SIZE)

        self.stdout.write(f"Пользователи: {len(users)}")
        return [user.id for user in users]

    def create_tags(self, count):
        existing = set(Tag.objects.values_list("name", flat=True))
        start = len(existing)
        tags = []
        for i in range(count):
            name = fake.word()
            if name in existing:
                name = f"{name}-{start + i}"
            existing.add(name)
            tags.append(Tag(name=name))
        tags = Tag.objects.bulk_create(tags, batch_size=BATCH_SIZE)

        self.stdout.write(f"Теги: {len(tags)}")
        return [tag.id for tag in tags]

    def create_questions(self, count, user_ids, tag_ids):
        questions = []
        for _ in range(count):
            questions.append(Question(
                author_id=random.choice(user_ids),
                title=fake.sentence(nb_words=6)[:-1] + "?",
                text=fake.paragraph(nb_sentences=5),
                created_at=random_date(),
            ))
        questions = Question.objects.bulk_create(questions, batch_size=BATCH_SIZE)
        question_ids = [question.id for question in questions]

        question_tags = []
        for question_id in question_ids:
            for tag_id in random.sample(tag_ids, min(random.randint(1, 3), len(tag_ids))):
                question_tags.append(Question.tags.through(question_id=question_id, tag_id=tag_id))
        Question.tags.through.objects.bulk_create(question_tags, batch_size=BATCH_SIZE)

        self.stdout.write(f"Вопросы: {len(question_ids)}")
        return question_ids

    def create_answers(self, count, user_ids, question_ids):
        # создаём пачками, чтобы не держать миллион объектов в памяти
        answer_ids = []
        with_correct = set()
        batch = []
        for _ in range(count):
            question_id = random.choice(question_ids)
            is_correct = question_id not in with_correct and random.random() < 0.3
            if is_correct:
                with_correct.add(question_id)
            batch.append(Answer(
                question_id=question_id,
                author_id=random.choice(user_ids),
                text=fake.paragraph(nb_sentences=3),
                is_correct=is_correct,
                created_at=random_date(),
            ))
            if len(batch) == BATCH_SIZE:
                answer_ids += [answer.id for answer in Answer.objects.bulk_create(batch)]
                batch = []
        answer_ids += [answer.id for answer in Answer.objects.bulk_create(batch)]

        self.stdout.write(f"Ответы: {len(answer_ids)}")
        return answer_ids

    def create_likes(self, count, user_ids, question_ids, answer_ids):
        # половина оценок вопросам, половина ответам
        created = self.create_likes_for(QuestionLike, "question_id", count // 2, user_ids, question_ids)
        created += self.create_likes_for(AnswerLike, "answer_id", count - count // 2, user_ids, answer_ids)
        self.stdout.write(f"Оценки: {created}")

    def create_likes_for(self, model, field, count, user_ids, object_ids):
        per_user = count // len(user_ids)
        extra = count % len(user_ids)
        created = 0
        batch = []
        for i, user_id in enumerate(user_ids):
            likes_count = min(per_user + (1 if i < extra else 0), len(object_ids))
            # random.sample не даёт повторов, поэтому один юзер не лайкнет одно и то же дважды
            for object_id in random.sample(object_ids, likes_count):
                value = 1 if random.random() < 0.75 else -1
                batch.append(model(user_id=user_id, value=value, created_at=random_date(), **{field: object_id}))
            if len(batch) >= BATCH_SIZE:
                model.objects.bulk_create(batch)
                created += len(batch)
                batch = []
        model.objects.bulk_create(batch)
        return created + len(batch)

    def update_counters(self, question_ids, answer_ids):
        # считаем рейтинг и число ответов одним UPDATE на таблицу, а не по одному объекту
        question_rating = QuestionLike.objects.filter(question=OuterRef("pk")).values("question").annotate(s=Sum("value")).values("s")
        answers_count = Answer.objects.filter(question=OuterRef("pk")).values("question").annotate(c=Count("id")).values("c")
        answer_rating = AnswerLike.objects.filter(answer=OuterRef("pk")).values("answer").annotate(s=Sum("value")).values("s")

        Question.objects.filter(id__gte=question_ids[0]).update(
            rating=Coalesce(Subquery(question_rating), 0),
            answers_count=Coalesce(Subquery(answers_count), 0),
        )
        Answer.objects.filter(id__gte=answer_ids[0]).update(rating=Coalesce(Subquery(answer_rating), 0))
        self.stdout.write("Рейтинги посчитаны")
