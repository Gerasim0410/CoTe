from django.db import models
from django.contrib.auth.models import AbstractBaseUser, BaseUserManager

CHOICE = 0
WORDS = 1
ANSWER_OPTIONS = [('CHOICE', CHOICE),
                  ('WORDS', WORDS)]


class ProfileUserManager(BaseUserManager):
    def create_user(self, user_id):
        if not user_id:
            raise ValueError("The User ID must be provided")
        user = self.model(user_id=user_id)
        user.save(using=self._db)
        return user

    def create_superuser(self, user_id):
        user = self.create_user(user_id=user_id)
        return user


class Profile(AbstractBaseUser):
    user_id: models.IntegerField = models.IntegerField(
        primary_key=True, unique=True)

    objects = ProfileUserManager()

    USERNAME_FIELD = 'user_id'

    def __str__(self):
        return str(self.user_id)


class TestSession(models.Model):
    # switch for passing the test personally or in group
    # if is_timed - True, then the test is in group
    session_id: models.AutoField = models.AutoField(primary_key=True)
    user_id: models.ForeignKey = models.ForeignKey(
        Profile, on_delete=models.CASCADE)
    # test_questions - onetomany from questions
    # test_results - onetomany from results
    # test_answers - onetomany from answers


class Questions(models.Model):
    # one row - one test type with 10 questions
    test_id: models.AutoField = models.AutoField(primary_key=True)
    TEST_TYPES = [
        #('STROOP1', 'stroop1'),
        ('STROOP2', 'stroop2'),
        ('STROOP3', 'stroop3'),
        ('STROOP4', 'stroop4'),
        ('ARITHM', 'arithm'),
        ('SPATIAL', 'spatial'),
        ('SHAPES', 'shapes'),
        #('COLOR', 'color'),
        ('SHAPES_COLOR', 'shapes_color'),
        ('SHAPES_SPATIAL', 'shapes_spatial'),
        ('MEMORY', 'memory'),
        ('MUNSTER', 'munster'),
        ('RAVEN', 'raven')
    ]
    test_type: models.CharField = models.CharField(
        max_length=255, choices=TEST_TYPES)
    # test_session_id - manytoone to test_questions in test_session
    test_session_id: models.ForeignKey = models.ForeignKey(
        TestSession, on_delete=models.CASCADE)
    # answers_id - onetomany from answers
    # results_id - onetomany from results
    # question_id - onetomany from question


class Question(models.Model):
    question_id: models.AutoField = models.AutoField(primary_key=True)
    # manytoone to questions
    questions_series: models.ForeignKey = models.ForeignKey(
        Questions, on_delete=models.CASCADE)
    question_num: models.IntegerField = models.IntegerField()
    question_desc: models.CharField = models.CharField(max_length=255)


class Answers(models.Model):
    answers_id: models.AutoField = models.AutoField(primary_key=True)
    test_session_id: models.ForeignKey = models.ForeignKey(
        TestSession, on_delete=models.CASCADE)
    # manytoone to questions
    questions_id: models.ForeignKey = models.ForeignKey(
        Questions, on_delete=models.CASCADE)
    results_id: models.ForeignKey = models.ForeignKey(
        'Results', on_delete=models.CASCADE, null=True)
    user_id: models.ForeignKey = models.ForeignKey(
        'Profile', on_delete=models.DO_NOTHING, default=Profile)
    # answer_id - onetomany from answer


class Answer(models.Model):
    answer_id: models.AutoField = models.AutoField(primary_key=True)
    # manytoone to answers
    answers_series: models.ForeignKey = models.ForeignKey(
        Answers, on_delete=models.CASCADE)
    answer_num: models.IntegerField = models.IntegerField()
    answer_options = ANSWER_OPTIONS
    answer_type: models.CharField = models.CharField(
        max_length=255, choices=ANSWER_OPTIONS)
    right_answer: models.CharField = models.CharField(max_length=255)
    given_answer: models.CharField = models.CharField(
        max_length=255, null=True)


class Results(models.Model):
    result_id: models.AutoField = models.AutoField(primary_key=True)
    test_session_id: models.ForeignKey = models.ForeignKey(
        TestSession, on_delete=models.CASCADE)
    # manytoone to questions
    questions_id: models.ForeignKey = models.ForeignKey(
        Questions, on_delete=models.CASCADE)
    answers_id: models.ForeignKey = models.ForeignKey(
        Answers, on_delete=models.CASCADE)
    result: models.CharField = models.CharField(max_length=255)
