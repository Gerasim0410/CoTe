import random
import logging
from django.test import TestCase
from quiz_app.utils \
    import generate_stroop_test_question, generate_arithm_test_question, \
    generate_visual_test_question, generate_munster_test_question, \
    generate_raven_test_question, generate_memory_test_question


logger = logging.getLogger('root')


class TestStroopTestQuestionGenerator(TestCase):

    def setUp(self):
        # Set a fixed seed for reproducibility
        random.seed(0)

    def test_generate_stroop_test_question_part_1(monkeypatch):
        result = generate_stroop_test_question('1')
        assert result['question'] in ['красный', 'зеленый', 'синий',
                                      'желтый', 'фиолетовый', 'черный']
        assert result['word_color'] == 'black'
        assert result['correct_answer'] in ['красный', 'зеленый', 'синий',
                                            'желтый', 'фиолетовый', 'черный']

    def test_generate_stroop_test_question_part_2(monkeypatch):
        random.seed(0)
        result = generate_stroop_test_question('2')
        assert result['question'] in ['красный', 'зеленый', 'синий', 'желтый',
                                      'фиолетовый', 'черный']
        assert result['word_color'] != 'black'
        assert result['correct_answer'] == result['question']

    def test_generate_stroop_test_question_part_3(monkeypatch):
        random.seed(0)
        result = generate_stroop_test_question('3')
        assert result['question'] in ['красный', 'зеленый', 'синий', 'желтый',
                                      'фиолетовый', 'черный']
        assert result['word_color'] != result['correct_answer']
        assert result['correct_answer'] == result['question']

    def test_generate_stroop_test_question_part_4(monkeypatch):
        random.seed(0)
        result = generate_stroop_test_question('4')
        assert result['question'] in ['красный', 'зеленый', 'синий', 'желтый',
                                      'фиолетовый', 'черный']
        assert result['word_color'] != result['correct_answer']
        assert result['correct_answer'] in ['красный', 'зеленый', 'синий',
                                            'желтый', 'фиолетовый', 'черный']

    def test_answers_length(monkeypatch):
        random.seed(0)
        result = generate_stroop_test_question('1')
        assert len(result['answers']) == 6
        for answer in result['answers']:
            assert answer[1] in ['красный', 'зеленый', 'синий',
                                 'желтый', 'фиолетовый', 'черный']


class TestArithmTestQuestionGenerator(TestCase):

    def setUp(self):
        self.questions = [generate_arithm_test_question() for _ in range(10)]

    def test_default_number_of_questions(self):
        self.assertEqual(len(self.questions), 10)

    def test_generate_arithm_test_question(self):
        # Test the function generates a question
        self.assertIn('question', self.questions[0])
        self.assertIn('correct_answer', self.questions[0])

    def test_question_format(self):
        # Test if the question is formatted correctly
        self.assertRegex(self.questions[0]['question'],
                         r'^\d+ [\+\-\*] \d+ = \d+$',
                         msg=f'{self.questions[0]}')

    def test_correct_answer(self):
        # Test if the correct answer is identified correctly
        a, operator, b = \
            map(str.strip, self.questions[0]['question'].split('=')[0].split())
        a, b = int(a), int(b)
        if operator == '+':
            expected_answer = a + b
        elif operator == '-':
            expected_answer = a - b
        else:  # operator == '*'
            expected_answer = a * b

        self.assertEqual(self.questions[0]['correct_answer'],
                         self.questions[0]['question'].endswith(
                             str(expected_answer)))

    def test_multiple_questions(self):
        # Test if multiple questions can be generated without error
        for i in range(10):
            self.assertIn('question', self.questions[i])
            self.assertIn('correct_answer', self.questions[i])

    def test_answer_choices(self):
        # Test if the answer is either correct or wrong
        a, operator, b = \
            map(str.strip, self.questions[0]['question'].split('=')[0].split())
        a, b = int(a), int(b)
        if operator == '+':
            correct_answer = a + b
        elif operator == '-':
            correct_answer = a - b
        else:  # operator == '*'
            correct_answer = a * b

        # Check if the answer in the question is either the correct answer
        # or a wrong answer
        self.assertIn(
            int(self.questions[0]['question'].split('=')[1].strip()),
            [correct_answer] + [i for i in range(0, 9) if i != correct_answer])


VISUAL_TEST_TYPES = [
    ('SPATIAL', 'spatial'),
    ('SHAPES', 'shapes'),
    ('COLOR', 'color'),
    ('SPATIAL', 'spatial'),
    ('SHAPES_COLOR', 'shapes_color'),
    ('SHAPES_SPATIAL', 'shapes_spatial'),
]


class TestGenerateVisualTestQuestion(TestCase):

    def test_question_structure(self):
        """Test that the generated question has the correct structure."""
        for test_type in VISUAL_TEST_TYPES:
            question = generate_visual_test_question(test_type[1], 5)
            self.assertIn('shapes_seq', question)
            self.assertIn('colors_seq', question)
            self.assertIn('spatials_seq', question)
            self.assertIn('correct_answer', question)

            self.assertIsInstance(question['shapes_seq'], list)
            self.assertIsInstance(question['colors_seq'], list)
            self.assertIsInstance(question['spatials_seq'], list)
            self.assertIsInstance(question['correct_answer'], list)

            self.assertEqual(len(question['shapes_seq']), 5)
            self.assertEqual(len(question['colors_seq']), 5)
            self.assertEqual(len(question['spatials_seq']), 5)
            # correct_answer will include 0 for the first answer
            self.assertEqual(len(question['correct_answer']), 5)

    def test_answer_values(self):
        """Test that the answers are within the expected range."""
        for test_type in VISUAL_TEST_TYPES:
            question = generate_visual_test_question(test_type[1], 5)
            for answer in question['correct_answer']:
                self.assertIn(answer, range(1, 7))

    def test_initial_answer(self):
        """Test that the first answer is always 'none of the above' (6)."""
        for test_type in VISUAL_TEST_TYPES:
            question = generate_visual_test_question(test_type[1], 5)
            self.assertEqual(question['correct_answer'][0], 6)

    def test_shape_color_spatial_logic(self):
        """
        Test that shapes, colors, and spatials follow the logic
        defined in the function.
        """
        for test_type in VISUAL_TEST_TYPES:
            question = generate_visual_test_question(test_type[1], 5)
            for i in range(1, len(question['correct_answer'])):
                if question['correct_answer'][i] in [1, 2, 5]:  # Same shape
                    self.assertEqual(question['shapes_seq'][i],
                                     question['shapes_seq'][i - 1], i)
                else:  # Different shape
                    self.assertNotEqual(question['shapes_seq'][i],
                                        question['shapes_seq'][i - 1], i)

                if question['correct_answer'][i] in [1, 3]:  # Same color
                    self.assertEqual(question['colors_seq'][i],
                                     question['colors_seq'][i - 1])
                else:  # Different color
                    self.assertNotEqual(question['colors_seq'][i],
                                        question['colors_seq'][i - 1], i)

                if question['correct_answer'][i] in [4, 5]:  # Same spatial
                    self.assertEqual(question['spatials_seq'][i],
                                     question['spatials_seq'][i - 1], i)
                else:  # Different spatial
                    self.assertNotEqual(question['spatials_seq'][i],
                                        question['spatials_seq'][i - 1], i)

    def test_randomness(self):
        """
        Test that the function generates different
        questions on multiple calls.
        """
        for test_type in VISUAL_TEST_TYPES:
            question1 = generate_visual_test_question(test_type[1], 5)
            question2 = generate_visual_test_question(test_type[1], 5)
            self.assertNotEqual(question1, question2)


class TestGenerateMunsterTestQuestion(TestCase):

    def setUp(self):

        self.question = generate_munster_test_question(matrix_size=5,
                                                       line_length=10,
                                                       max_words_in_line=3)

    def test_generate_munster_test_question_structure(self):

        # Check if the returned question is a dictionary
        self.assertIsInstance(self.question, dict)

        # Check if the matrix is present and has the correct structure
        self.assertIn('matrix', self.question)
        self.assertIsInstance(self.question['matrix'], list)
        # Check matrix size
        self.assertEqual(len(self.question['matrix']), 5)

        for line in self.question['matrix']:
            self.assertIsInstance(line, list)
            self.assertEqual(len(line), 10)  # Check line length

    def test_correct_words_included(self):

        # Check if the correct answer is present
        self.assertIn('correct_answer', self.question)
        self.assertIsInstance(self.question['correct_answer'], list)

        # Ensure that the correct words are in the matrix
        correct_words = self.question['correct_answer']
        matrix_flat = [letter for line in self.question['matrix']
                       for letter in line]
        matrix_flat = ''.join(matrix_flat)
        self.assertEqual(sum(
            [word in matrix_flat for word in correct_words]),
                         len(correct_words))

    def test_word_placement(self):
        # Check if words are placed correctly in the matrix
        matrix = self.question['matrix']
        for line in matrix:
            for word in self.question['correct_answer']:
                if word in ''.join(line):
                    self.assertIn(word, ''.join(line))


class TestRavenQuestionGenerator(TestCase):

    def test_generate_raven_test_question_structure(self):
        question_data = generate_raven_test_question()
        self.assertIn('question', question_data)
        self.assertIn('answers', question_data)
        self.assertIn('correct_answer', question_data)

    def test_question_number(self):
        question_data = generate_raven_test_question()
        question_number = question_data['question']
        self.assertTrue(1 <= int(question_number) <= 15)

    def test_answers_length(self):
        RAVEN_ANSWERS = {idx: value
                         for idx, value in enumerate(
                          [(1, 5), (6, 6), (1, 6),
                           (3, 6), (4, 6), (5, 6),
                           (3, 6), (5, 6), (1, 1),
                           (1, 8), (7, 8), (5, 8),
                           (8, 8), (2, 9), (8, 8)], 1)}
        question_data = generate_raven_test_question()
        question_number = question_data['question']
        num_answers = RAVEN_ANSWERS[int(question_number)][1]
        self.assertEqual(len(question_data['answers']), num_answers)

    def test_correct_answer_in_answers(self):
        question_data = generate_raven_test_question()
        correct_answer = question_data['correct_answer']
        self.assertIn(correct_answer, question_data['answers'])


class TestQuestionGeneration(TestCase):

    def test_generate_stroop_test_question(self):
        # Test for part 1
        result = generate_stroop_test_question('1')
        self.assertIn('question', result)
        self.assertIn('word_color', result)
        self.assertIn('correct_answer', result)
        self.assertIn('answers', result)
        self.assertIsInstance(result['answers'], list)

        # Test for part 2
        result = generate_stroop_test_question('2')
        self.assertIn('question', result)
        self.assertIn('word_color', result)
        self.assertIn('correct_answer', result)
        self.assertIn('answers', result)

        # Test for part 3
        result = generate_stroop_test_question('3')
        self.assertIn('question', result)
        self.assertIn('word_color', result)
        self.assertIn('correct_answer', result)
        self.assertIn('answers', result)

        # Test for part 4
        result = generate_stroop_test_question('4')
        self.assertIn('question', result)
        self.assertIn('word_color', result)
        self.assertIn('correct_answer', result)
        self.assertIn('answers', result)

    def test_generate_arithm_test_question(self):
        result = generate_arithm_test_question(
            num_of_questions=10, num_of_answers=4)
        self.assertIn('question', result)
        self.assertIn('correct_answer', result)

    def test_generate_visual_test_question(self):
        for type in VISUAL_TEST_TYPES:
            result = generate_visual_test_question(
                'some_test_type', num_of_questions=5)
            self.assertIn('shapes_seq', result)
            self.assertIn('colors_seq', result)
            self.assertIn('spatials_seq', result)
            self.assertIn('correct_answer', result)

    def test_generate_memory_test_question(self):
        result = generate_memory_test_question(
            num=10, num_of_answers=3)
        self.assertIn('words_to_remember', result)
        self.assertIn('words_seq', result)
        self.assertIn('correct_answer', result)

    def test_generate_munster_test_question(self):
        result = generate_munster_test_question(
            matrix_size=5, line_length=10, max_words_in_line=3)
        self.assertIn('matrix', result)
        self.assertIn('correct_answer', result)

    def test_generate_raven_test_question(self):
        result = generate_raven_test_question()
        self.assertIn('question', result)
        self.assertIn('answers', result)
        self.assertIn('correct_answer', result)
