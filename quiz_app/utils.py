import random
import logging
import copy

from .models import Questions


logger = logging.getLogger('root')
TEST_TYPES = Questions.TEST_TYPES


def generate_stroop_test_question(part):
    # Define colors and words
    colors = \
        [('red', 'красный'),
         ('green', 'зеленый'),
         ('blue', 'синий'),
         ('yellow', 'желтый'),
         ('purple', 'фиолетовый'),
         ('black', 'черный')]

    # correct color tuple
    color = random.choice(colors)
    # colors w/o correct color
    colors_w_o_color = colors.copy()
    colors_w_o_color.remove(color)
    if part == '1':
        # color of word
        word_color = 'black'
        # correct answer to the question
        correct_color = color[1]
    elif part == '2':
        word_color = color[0]
        correct_color = color[1]
    elif part == '3':
        word_color = random.choice(colors_w_o_color)[0]
        correct_color = color[1]
    else:
        word_and_correct_color = random.choice(colors_w_o_color)
        word_color = word_and_correct_color[0]
        correct_color = word_and_correct_color[1]

    random.shuffle(colors)

    return_dict = {
        'question': color[1],
        'word_color': word_color,
        'correct_answer': correct_color,
        'answers': colors,
    }

    return return_dict

# #@classmethod
# class Castilla:    
#     array=([1,2,3,4,5,6,7,8,9,10])
#     counter=0
#     #@staticmethod
#     def get_next():
#         if(Castilla.counter==9):
#             Castilla.array.sort()
#             Castilla.counter=0
#         if(Castilla.array[Castilla.counter]>4):
#             return True
#         else: 
#             return False


def generate_arithm_test_question(itt, arr, num_of_answers=4):
    a = random.randint(1, 10)
    b = random.randint(1, 10)
    operator = random.choice(['+', '-', '⨉'])
    if operator == '+':
        answer = a + b
    elif operator == '-':
        # no negative numbers
        if a < b:
            a, b = b, a
        answer = a - b
    else:
        answer = a * b
    if arr[itt[0]] < num_of_answers:
        answer_in_question=answer
    else:
        answer_in_question=answer + random.choice([-3,-2, -1, 1, 2,3])
    if itt[0] < 9:
        itt[0]+=1
    else:
        itt[0]=0
        random.shuffle(arr)

    question = {
        'question': f'{a} {operator} {b} = {answer_in_question}',
        'correct_answer': answer_in_question == answer,
    }
    return question


def generate_visual_test_question(
        test_type, num_of_questions, proba = 0.4):
    shapes = ['circle', 'square', 'pentagon', 'star']  # 'hexagon', 'triangle',
    colors = ['red', 'green', 'blue']  # , 'yellow', 'purple', 'black']
    spatials = ['up', 'down', 'center']

    # answers have
    RIGHT_ANSWERS_FOR_TYPES = {'shapes_color': 1, 
                               'shapes': 2,
                               'color': 3,
                               'spatial': 4,
                               'shapes_spatial': 5,}
    # SHAPE_AND_COLOR = 1
    # SHAPE = 2
    # COLOR = 3
    # SPATIAL = 4
    # SHAPE_AND_SPATIAL = 5
    # NONE = 6

    num_zeros = int(num_of_questions * proba)
    num_sixes = num_of_questions - num_zeros
    arr = random.sample([0] * num_zeros + [6] * num_sixes, k=num_of_questions-1)
    right_answers = [i if i != 0 else RIGHT_ANSWERS_FOR_TYPES[test_type] for i in arr]

    shapes_seq = random.sample(shapes, k=1)
    colors_seq = random.sample(colors, k=1)
    spatials_seq = random.sample(spatials, k=1)

    for var in right_answers:
        if var == 1:
            shapes_seq.append(shapes_seq[-1])
            colors_seq.append(colors_seq[-1])
            spatials_seq.append(random.sample(spatials, k=1)[0])
        elif var == 2:
            shapes_seq.append(shapes_seq[-1])
            colors_seq.append(random.sample(colors, k=1)[0])
            spatials_seq.append(random.sample(spatials, k=1)[0])
        elif var == 3:
            shapes_seq.append(random.sample(shapes, k=1)[0])
            colors_seq.append(colors_seq[-1])
            spatials_seq.append(random.sample(spatials, k=1)[0])
        elif var == 4:
            shapes_seq.append(random.sample(shapes, k=1)[0])
            colors_seq.append(random.sample(colors, k=1)[0])
            spatials_seq.append(spatials_seq[-1])
        elif var == 5:
            shapes_seq.append(shapes_seq[-1])
            colors_seq.append(random.sample(colors, k=1)[0])
            spatials_seq.append(spatials_seq[-1])
        else:
            if RIGHT_ANSWERS_FOR_TYPES[test_type] == 1:
                shapes_seq.append(random.sample([i for i in shapes if i != shapes_seq[-1]],k=1)[0]) 
                colors_seq.append(random.sample([i for i in colors if i != colors_seq[-1]],k=1)[0])
                spatials_seq.append(random.sample(spatials, k=1)[0])
            elif RIGHT_ANSWERS_FOR_TYPES[test_type] == 2:
                shapes_seq.append(random.sample([i for i in shapes if i != shapes_seq[-1]],k=1)[0])
                colors_seq.append(random.sample(colors, k=1)[0])
                spatials_seq.append(random.sample(spatials, k=1)[0])
            elif RIGHT_ANSWERS_FOR_TYPES[test_type] == 3:
                shapes_seq.append(random.sample(shapes, k=1)[0])
                colors_seq.append(random.sample([i for i in colors if i != colors_seq[-1]],k=1)[0])
                spatials_seq.append(random.sample(spatials, k=1)[0])
            elif RIGHT_ANSWERS_FOR_TYPES[test_type] == 4:
                shapes_seq.append(random.sample(shapes, k=1)[0])
                colors_seq.append(random.sample(colors, k=1)[0])
                spatials_seq.append(random.sample([i for i in spatials if i != spatials_seq[-1]],k=1)[0])
            else: 
                shapes_seq.append(random.sample([i for i in shapes if i != shapes_seq[-1]],k=1)[0])
                colors_seq.append(random.sample(colors, k=1)[0])
                spatials_seq.append(random.sample([i for i in spatials if i != spatials_seq[-1]],k=1)[0])

    question = {
        'shapes_seq': shapes_seq,
        'colors_seq': colors_seq,
        'spatials_seq': spatials_seq,
        'correct_answer': [None] + right_answers
    }

    return question


def generate_memory_test_question(num=10, num_of_answers=3):
    words_to_remember = random.sample(hundred_russian_words,
                                      num_of_answers)
    words_not_to_remember = [word
                             for word in hundred_russian_words
                             if word not in words_to_remember]
    words_to_remember = [
        word.strip() for word in words_to_remember]
    words_not_to_remember = [
        word.strip() for word in words_not_to_remember]
    words_to_add_to_question = random.sample(
        words_not_to_remember,
        num - num_of_answers)
    final_seq = words_to_remember + words_to_add_to_question
    random.shuffle(final_seq)
    answers = [elt[0]
               for elt in enumerate(final_seq)
               if elt[1] in words_to_remember]
    question = {
        'words_to_remember': words_to_remember,
        'words_seq': final_seq,
        'correct_answer': answers}
    return question


def generate_munster_test_question(matrix_size=20, line_length=20,
                                   max_words_in_line=3):
    words = random.sample(hundred_russian_words, 50)
    words = [i.strip() for i in words]

    matrix, correct_words = [], []
    russian_letters = [chr(code) for code in range(ord('а'), ord('я') + 1)]
    available_words = words.copy()

    for _ in range(matrix_size):
        line = [''] * line_length
        remaining_space = line_length
        max_words = random.sample([0,0,1,1,1,2,2,2,3,3,3], k=1)[0]
        chosen_words = random.sample(
            [w for w in available_words if len(w) <= remaining_space],
            k=min(max_words, len(available_words))
        )

        for word in chosen_words:
            if len(word) <= remaining_space:
                possible_positions = [
                    i for i in range(line_length - len(word) + 1)
                    if all(c == '' for c in line[i:i + len(word)])
                ]
                if possible_positions:
                    available_words.remove(word)
                    correct_words.append(word)
                    start_pos = random.choice(possible_positions)
                    line[start_pos:start_pos + len(word)] = list(word)
                    remaining_space -= len(word)

        matrix.append([c if c else random.choice(russian_letters)
                       for c in line])

    question = {
        'matrix': matrix,
        'correct_answer': correct_words
    }

    return question


def generate_raven_test_question(itt, arr):

    # TODO answer to the first raven question is wrong
    # question_idx: (right_answer_num, amount_of_answers)
    RAVEN_ANSWERS = [6,6,1,4,3,5,3,5,7,1,7,1,8,2,8]
    RAVEN_POSSIBLE_ANSWERS = [1,2,3,4,5,6,7,8]
    question = arr[itt[0]]
    if itt[0] < 9:
        itt[0] += 1
    else:
        itt[0]=0
    question = {
        'question': f'{question}',
        'answers': RAVEN_POSSIBLE_ANSWERS,
        'correct_answer': RAVEN_ANSWERS[question-1]
    }
    return question


with open('quiz_app/static/words_in_russian.txt', 'r',
          encoding='utf-8') as file:
    hundred_russian_words = [line for line in file]


# num=1 for memory test, for visual tests
def generate_test_questions(test, num=10, **kwargs):
    itt = [0]
    arr_arithm = random.sample([i for i in range(10)], k=10)
    arr_raven = random.sample([i for i in range(1, 16)], k=10)
    if test == 'stroop2':
       num = 5
    print(test, "                                                                                             ", num)
    # test goes from TEST_TYPES[:, 1]
    test_function_map = {
        # stroop
        #TEST_TYPES[0][1]: lambda: generate_stroop_test_question(test[-1]),
        TEST_TYPES[0][1]: lambda: generate_stroop_test_question(test[-1]),
        TEST_TYPES[1][1]: lambda: generate_stroop_test_question(test[-1]),
        TEST_TYPES[2][1]: lambda: generate_stroop_test_question(test[-1]),
        # arithm
        TEST_TYPES[3][1]: lambda: generate_arithm_test_question(itt, arr_arithm),
        # visual
        TEST_TYPES[4][1]: lambda: generate_visual_test_question(
            test, kwargs['num_of_visuals']),
        TEST_TYPES[5][1]: lambda: generate_visual_test_question(
            test, kwargs['num_of_visuals']),
        #TEST_TYPES[6][1]: lambda: generate_visual_test_question(
        #    test, kwargs['num_of_visuals']),
        TEST_TYPES[6][1]: lambda: generate_visual_test_question(
            test, kwargs['num_of_visuals']),
        TEST_TYPES[7][1]: lambda: generate_visual_test_question(
            test, kwargs['num_of_visuals']),
        # memory
        TEST_TYPES[8][1]: lambda: generate_memory_test_question(
            kwargs['num_of_words'], kwargs['num_of_answers']),
        # munster
        TEST_TYPES[9][1]: lambda: generate_munster_test_question(
            kwargs['matrix_size'], kwargs['line_length'],
            kwargs['max_words_in_line']),
        # raven
        TEST_TYPES[10][1]: lambda: generate_raven_test_question(itt, arr_raven)
    }

    # Determine the appropriate function based on the test type
    for key in test_function_map:
        if key in test:
            questions = [test_function_map[key]() for _ in range(num)]
            return questions
    raise ValueError("Invalid test type")


