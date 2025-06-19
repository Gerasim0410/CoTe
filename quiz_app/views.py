import json
import logging
from typing import Tuple
import os
import sqlite3
from django.conf import settings
from django.http import FileResponse, HttpResponseServerError
from django.urls.base import reverse
from django.shortcuts import render, redirect
from django.contrib.auth import authenticate, login, logout
from django.contrib.auth.decorators import login_required
from django.contrib.admin.views.decorators import staff_member_required
from django.db.models import Max
from django.http import \
    HttpResponsePermanentRedirect, HttpResponseRedirect, JsonResponse

from .models import Profile, Answer, Answers, Question, Questions, \
    Results, TestSession, CHOICE, WORDS
from .utils import generate_test_questions
from .forms import RegistrationForm, UserIDLoginForm


logger = logging.getLogger(__name__)
logger.setLevel(level=logging.DEBUG)

def home(request):
    return render(request, 'home.html')


def register(request):
    if request.method == 'POST':
        form = RegistrationForm(request.POST)
        if form.is_valid():
            form.save()
            return redirect('home')
    else:
        form = RegistrationForm()
    return render(request, 'register.html', {'form': form})


def login_view(request):
    if request.method == 'POST':
        form = UserIDLoginForm(request.POST)
        if form.is_valid():
            try:
                user_id = form.cleaned_data['user_id']
                user = authenticate(request, user_id=user_id)
                if user is not None:
                    login(request, user)
                    return redirect('home')
                else:
                    return render(request, 'login.html',
                                  {'form': form, 'error': 'Invalid user ID'})
            except Exception as e:
                return render(request, 'login.html',
                              {'form': form, 'error': e})
    else:
        form = UserIDLoginForm()

    return render(request, 'login.html', {'form': form})


def logout_view(request):
    logout(request)
    return redirect('home')


RENDERING_CONST: dict[str, dict] = \
    {
        'generation_args': {
            #'STROOP1': ('stroop1',),
            'STROOP2': ('stroop2',),
            'STROOP3': ('stroop3',),
            'STROOP4': ('stroop4',),
            'ARITHM': ('arithm',),
            'SHAPES': ('shapes', 1),
            #'COLOR': ('color', 1),
            'SPATIAL': ('spatial', 1),
            'SHAPES_COLOR': ('shapes_color', 1),
            'SHAPES_SPATIAL': ('shapes_spatial', 1),
            'MEMORY': ('memory', 1),
            'MUNSTER': ('munster', 1),
            'RAVEN': ('raven', )},

        'generation_kwargs': {
            #'STROOP1': {}, 
            'STROOP2': {'num_of_questions': 5}, 'STROOP3': {'num_of_questions': 10}, 'STROOP4': {'num_of_questions': 10},
            'ARITHM': {'num_of_questions': 10, 'num_of_answers': 4},
            'SHAPES': {'num_of_visuals': 10},
            #'COLOR': {'num_of_visuals': 20},
            'SPATIAL': {'num_of_visuals': 10},
            'SHAPES_COLOR': {'num_of_visuals': 10},
            'SHAPES_SPATIAL': {'num_of_visuals': 15},
            'MEMORY': {'num_of_words': 13, 'num_of_answers': 6},
            'MUNSTER': {'matrix_size': 20, 'line_length': 20,
                        'max_words_in_line': 3}, 'RAVEN': {}},

        'answer_type': {
            'STROOP1': CHOICE, 'STROOP2': CHOICE,
            'STROOP3': CHOICE, 'STROOP4': CHOICE, 'ARITHM': CHOICE,
            'SHAPES': CHOICE, 'COLOR': CHOICE, 'SPATIAL': CHOICE,
            'SHAPES_COLOR': CHOICE, 'SHAPES_SPATIAL': CHOICE,
            'MEMORY': CHOICE, 'MUNSTER': WORDS, 'RAVEN': CHOICE},

        'template': {
            'STROOP1': 'stroop_test.html', 'STROOP2': 'stroop_test.html',
            'STROOP3': 'stroop_test.html', 'STROOP4': 'stroop_test.html',
            'ARITHM': 'arithm_test.html', 'SHAPES': 'shapes.html',
            'SPATIAL': 'shapes.html', 'COLOR': 'shapes.html',
            'SHAPES_COLOR': 'shapes.html', 'SHAPES_SPATIAL': 'shapes.html',
            'MEMORY': 'memory_test.html', 'MUNSTER': 'munster_test.html',
            'RAVEN': 'raven_test.html'},

        'timer_seconds': {
            'STROOP2': 3,
            #'STROOP1': 3,
            'STROOP3': 3,
            'STROOP4': 3,
            'ARITHM': 3,
            'SHAPES': 3,
            #'COLOR': 3,
            'SPATIAL': 3,
            'SHAPES_COLOR': 3,
            'SHAPES_SPATIAL': 3,
            'MEMORY': 3,
            'MUNSTER': 60,
            'RAVEN': 15,
        }}


inverted_test_types = \
    {v: k for k, v in Questions.TEST_TYPES}


@login_required
def start_test(request):

    # test session number will be similar for the entire group of users
    # TODO maybe make it possible for user to choose test session
    if request.user.user_id == 1:
        TestSession.objects.create(
    user_id=Profile.objects.filter(user_id=request.user.user_id).first()
)

        test_session = TestSession.objects.filter(
            user_id=request.user.user_id).last()
        for test in inverted_test_types:
            inverted_test_type = inverted_test_types[test]
            questions = generate_test_questions(
                *RENDERING_CONST['generation_args'][inverted_test_type],
                **RENDERING_CONST['generation_kwargs'][inverted_test_type])

            new_question_series = Questions.objects.create(
                test_type=inverted_test_types[test],
                test_session_id=test_session
            )

            for num, question in enumerate(questions):

                question_num = Question.objects.create(
                    questions_series=new_question_series,
                    question_num=num,
                    question_desc=json.dumps(
                        question, ensure_ascii=False)
                )

                logging.warning(question_num)
                logging.warning(question['correct_answer'])

    return redirect('instruction', test='stroop2')


@login_required
def instruction(request, test):
    test_dict = {
        #'stroop1': 'Струпа, часть 1',
        'stroop2': 'Струпа, часть 1',
        'stroop3': 'Струпа, часть 2',
        'stroop4': 'Струпа, часть 3',
        'arithm': 'арифметическому',
        'shapes': 'на повторения фигур',
        #'color': 'на повторения цвета',
        'shapes_color': 'на повторения фигур и цвета',
        'spatial': 'на повторения положения',
        'shapes_spatial': 'на повторения фигур и положения',
        'memory': 'на память',
        'munster': 'Мюнстерберга',
        'raven': 'Равена',
    }
    test_instr = {
        'stroop2': 'На экране появляются слова, обозначающие цвет.' +
        ' Нужно выбирать цветовой образец в соответствии с заданием.' +
        '\n В 1-ой части теста Струпа выбирайте цвет по смыслу и цвету (одновременно).' +
        '\n Смысл будет соответсвовать цвету слова',
        #'stroop2': 'Во 2-ой части выбирайте цвет по смыслу и цвету (одновременно).' +
        #'\n Смысл будет соответсвовать цвету слова',
        'stroop3': 'Во 2-ой части выбирайте цвет по смыслу',
        'stroop4': 'В последней части теста Струпа выбирайте цвет по цвету слова',
        'arithm': 'Нажимайте ДА (зеленое поле слева), если показано верное числовое равенство, ' +
        'иначе - НЕТ (красное поле справа)',
        'shapes': 'Нажимайте ДА, если ФОРМА (круг, квадрат, пятиугольник, звезда) текущей фигуры полностью' +
        ' совпадает с ФОРМОЙ предыдущей, иначе - НЕТ',
        #'color': 'Нажимайте ДА, если ЦВЕТ (красный, зеленый, синий) текущей фигуры полностью' +
        #' совпадает с ЦВЕТОМ предыдущей, иначе - НЕТ',
        'shapes_color': 'Нажимайте ДА, если ФОРМА и ЦВЕТ текущей' +
        ' фигуры полностью совпадает с ФОРМОЙ и ЦВЕТОМ предыдущей,' +
        ' иначе - НЕТ',
        'spatial': 'Вам будет показан ряд фигур, имеющие различные форму, цвет и положение на экране. Нажимайте ДА, ' +
        'если ПОЛОЖЕНИЕ (сверху, по середине, снизу) текущей' +
        ' фигуры полностью совпадает с ПОЛОЖЕНИЕМ предыдущей,' +
        ' иначе - НЕТ',
        'shapes_spatial': 'Нажимайте ДА, если ПОЛОЖЕНИЕ и ФОРМА текущей' +
        ' фигуры полностью совпадает с ПОЛОЖЕНИЕМ и ФОРМОЙ предыдущей,' +
        ' иначе - НЕТ',
        'memory': 'За 20 секунд постарайтесь запомнить слова, которые появятся на экране телефона.' +
        ' Далее вам будет показан ряд слов, нажимайте ДА' +
        ' если появившееся слово было в ряде для запоминания, иначе - НЕТ',
        'munster': 'Введите в поле для ввода поочередно все слова, которые вам удастся' +
        ' обнаружить в таблице. Нажмите на кнопку "Проверить слово", чтобы отправить и убедиться, что вы верно все записали',
        'raven': 'Выберите из предложенных вариантов фрагмент,' +
        ' который завершит картинку верно',
    }

    for idx, i in enumerate(Questions.TEST_TYPES):
        if test == i[1] and i != Questions.TEST_TYPES[-1]:
            next_test = Questions.TEST_TYPES[idx + 1][1]
        elif test == i[1]:
            next_test = None

    logger.log(level=logging.WARNING, msg=f'{request.user.user_id}')
    return render(request, 'instruction.html',
                  {'test_name': test_dict[test],
                   'test': test,
                   'next_test': next_test,
                   'test_instr': test_instr[test],
                   'user_id': request.user.user_id})


def process_test_submission(test_session, answers_data, test, user):
    try:
        logger.log(level=logging.DEBUG, msg=f'{test}')
        question_set = Questions.objects.filter(
            test_session_id=test_session.session_id,
            test_type=inverted_test_types[test]
        ).last()
        if not question_set:
            raise ValueError("Question set not found for the given test.")

        answer_set = Answers.objects.create(
            test_session_id=test_session,
            questions_id=question_set,
            results_id=None,
            user_id=user
        )
        answer_set.save()
        if not answer_set:
            raise ValueError("Answer set was not created.")
        max_questions = Question.objects.filter(
            questions_series=question_set.test_id).aggregate(
                Max('question_num'))
        if ((not max_questions
           or max_questions['question_num__max'] is None)
           and 'munster' not in test):
            raise ValueError("No questions found for the given test.")

        inverted_test_type = inverted_test_types[test]
        times_taken = []
        logging.warning('been there')
        if 'stroop' in test or 'raven' in test or 'arithm' in test:
            for idx, answer_data in enumerate(answers_data):
                selected_answer = answer_data.get('selectedAnswer')
                time_taken = answer_data.get('time_taken')
                logger.warning(selected_answer)
                if idx > max_questions['question_num__max']:
                    continue

                question = Question.objects.filter(
                    questions_series=question_set,
                    question_num=idx
                ).first()
                curr_answ = Answer.objects.create(
                    answers_series=answer_set,
                    answer_num=idx,
                    answer_type=RENDERING_CONST['answer_type'][
                        inverted_test_type],
                    right_answer=json.loads(
                        question.question_desc)['correct_answer']
                )
                if not curr_answ:
                    logger.warning(
                        f'Answer not found for answer_num {idx}' +
                        f' in answer_set {answer_set}')
                    continue

                curr_answ.given_answer = selected_answer
                curr_answ.save()
                times_taken.append(time_taken)
            logger.warning(f'{curr_answ}')
            logger.warning(f'{times_taken}')
        elif 'munster' in test:
            logging.warning('been there')
            times_taken = answers_data.get('time_taken')
            selected_answers = answers_data.get('selectedAnswer')
            logging.warning('been there')
            try:
                question = Question.objects.filter(
                    questions_series=question_set,
                    question_num=0
                ).first()
                curr_answ = Answer.objects.create(
                    answers_series=answer_set,
                    answer_num=0,
                    answer_type=RENDERING_CONST['answer_type'][
                        inverted_test_type],
                    right_answer=json.loads(
                        question.question_desc)['correct_answer']
                )
            except Exception as e:
                logging.warning(e)
            logging.warning('been there')
            if not curr_answ:
                raise ValueError("Answer not found for the given test.")
            logging.warning('been there')
            curr_answ.given_answer = selected_answers
            logger.warning(curr_answ)
            curr_answ.save()
            logging.warning('been there')
        else:
            selected_answers = []
            for idx, answer_data in enumerate(answers_data):
                selected_answer = answer_data.get('selectedAnswer')
                if isinstance(selected_answer, str):
                    selected_answer = selected_answer.lower()
                time_taken = answer_data.get('time_taken')
                selected_answers.append(selected_answer)
                times_taken.append(time_taken)

            question = Question.objects.filter(
                questions_series=question_set,
                question_num=0
            ).first()
            curr_answ = Answer.objects.create(
                answers_series=answer_set,
                answer_num=0,
                answer_type=RENDERING_CONST['answer_type'][
                    inverted_test_type],
                right_answer=json.loads(
                        question.question_desc)['correct_answer']
            )

            if not curr_answ:
                raise ValueError("Answer not found for the given test.")

            curr_answ.given_answer = selected_answers
            curr_answ.save()
            logger.warning(f'{curr_answ}')
            logger.warning(f'{times_taken}')

        logger.warning(f'{answer_set}')
        logger.warning(f'{times_taken}')

        result = Results.objects.create(
            test_session_id=test_session,
            questions_id=question_set,
            answers_id=answer_set,
            result=str(times_taken)
        )
        result.save()
        answer_set.results_id = result.result_id
        answer_set.save()

    except Exception as e:
        return {"status": "error", "message": str(e)}


def test_setup(test_session, test) -> Tuple[int, str, list[dict]] | \
        HttpResponsePermanentRedirect | HttpResponseRedirect:

    questions_series = Questions.objects.filter(
        test_type=inverted_test_types[test],
        test_session_id=test_session).last()
    questions_dicts = Question.objects.filter(
        questions_series=questions_series).order_by('question_num').values()
    questions = [json.loads(i['question_desc']) for i in questions_dicts]
    inverted_test_type = inverted_test_types[test]

    timer_seconds: int = RENDERING_CONST['timer_seconds'][inverted_test_type]
    template_name: str = RENDERING_CONST['template'][inverted_test_type]

    return timer_seconds, template_name, questions


@login_required
def test(request, test):

    try:

        user_id = Profile.objects.filter(
            user_id=request.user.user_id).first()

        if not user_id:
            logger.warning(
                f"Profile not found for user: {request.user.user_id}")
            return redirect('home')

        test_session = TestSession.objects.filter(
            user_id=1).last()

        if request.method == 'GET':

            result = test_setup(test_session, test)
            if not (isinstance(result, HttpResponseRedirect)
                    or isinstance(result, HttpResponsePermanentRedirect)):
                timer_seconds, template_name, questions = result
            else:
                return result

            test_url = reverse('test_submit', kwargs={'test': test})

            return render(request, template_name,
                          {'test': test,
                           'test_url': test_url,
                           'questions': questions,
                           'timer_seconds': timer_seconds,
                           'user_id': user_id,
                           'current_question_index': 0})

    except Exception as e:
        logger.exception(
            f"Unexpected error {e} occurred during the test view.")
        return redirect('home')


@login_required
def test_submit(request, test):

    if request.method != 'POST':
        return JsonResponse({"error": "Invalid request method."}, status=405)
    try:
        test_session = TestSession.objects.filter(
            user_id=1).last()
        if not test_session:
            raise ValueError("Test session not found for the user.")

        data = json.loads(request.body)
        answers_data = data.get('answers', [])
        logger.warning(f'answers_data: {answers_data}')
        if not answers_data:
            raise ValueError("No answers provided in the request data.")

        process_test_submission(test_session, answers_data,
                                test, request.user)
        logging.debug('test submitted')

        for idx, i in enumerate(Questions.TEST_TYPES):
            if test == i[1] and i != Questions.TEST_TYPES[-1]:
                next_test = Questions.TEST_TYPES[idx + 1][1]
                return JsonResponse({
                    'message': 'Тест закончен!',
                    'redirect_url': reverse('instruction',
                                            kwargs={'test': next_test})})
            elif test == i[1]:
                return JsonResponse({
                    'message': 'Тест закончен!',
                    'redirect_url': reverse('end_test')})

    except json.JSONDecodeError:
        logger.error("Invalid JSON in request body.")
        return JsonResponse({"error": "Invalid JSON format."}, status=400)

    except ValueError as ve:
        logger.error(f"Validation error: {ve}")
        return JsonResponse({"error": str(ve)}, status=400)

    except Exception as e:
        logger.exception("Unexpected error occurred.")
        return JsonResponse(
            {"error":
             f"An unexpected error {e} occurred. Please try again later."},
            status=500)


def thank_you(request):
    user_id = Profile.objects.filter(
        user_id=request.user.user_id).first()
    request.session.flush()
    return render(request, 'thank_you.html', {'user_id': user_id})


@staff_member_required
def results(request):
    return redirect('results')

def net(request):
    try:
        db_path = os.path.join(settings.BASE_DIR, 'db.sqlite3')
        backup_path = os.path.join(settings.BASE_DIR, 'db_backup.sqlite3')

        with sqlite3.connect(db_path) as src:
            with sqlite3.connect(backup_path) as dst:
                src.backup(dst)  # безопасное копирование

        return FileResponse(open(backup_path, 'rb'), as_attachment=True, filename='db.sqlite3')

    except Exception as e:
        return HttpResponseServerError(f"Ошибка при создании резервной копии: {e}")