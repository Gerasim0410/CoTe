import json

from django.test import TestCase, Client
from django.urls import reverse
from quiz_app.forms import RegistrationForm, UserIDLoginForm
from quiz_app.utils import generate_test_questions
from quiz_app.views import test_setup
from quiz_app.models import Profile, TestSession, Questions, Answers, Results


class ViewsTestCase(TestCase):

    def setUp(self):
        # Create a test user
        self.admin = Profile.objects.create_user(user_id=1)
        self.user = Profile.objects.create_user(user_id=2)

    def test_home_view(self):
        response = self.client.get(reverse('home'))
        self.assertEqual(response.status_code, 200)
        self.assertTemplateUsed(response, 'home.html')

    def test_register_view_get(self):
        response = self.client.get(reverse('register'))
        self.assertEqual(response.status_code, 200)
        self.assertTemplateUsed(response, 'register.html')
        self.assertIsInstance(response.context['form'], RegistrationForm)

    def test_register_view_post_valid(self):
        response = self.client.post(reverse('register'), {
            'user_id': 3,
        })
        self.assertRedirects(response, reverse('home'))
        self.assertTrue(Profile.objects.filter(user_id=3).exists())
        Profile.objects.filter(user_id=3).first().delete()

    def test_register_view_post_invalid(self):
        response = self.client.post(reverse('register'), {
            'user_id': '',  # Invalid
        })
        self.assertEqual(response.status_code, 200)
        self.assertTemplateUsed(response, 'register.html')
        self.assertFormError(response, 'form', 'user_id', 
                             'This field is required.')

    def test_login_view_get(self):
        response = self.client.get(reverse('login'))
        self.assertEqual(response.status_code, 200)
        self.assertTemplateUsed(response, 'login.html')
        self.assertIsInstance(response.context['form'], UserIDLoginForm)

    def test_login_view_post_valid(self):
        response = self.client.post(reverse('login'), {
            'user_id': 1
        })
        self.assertRedirects(response, reverse('home'))
        self.assertTrue(response.wsgi_request.user.is_authenticated)

    def test_login_view_post_invalid(self):
        response = self.client.post(reverse('login'), {
            'user_id': ''
        })
        self.assertEqual(response.status_code, 200)
        self.assertTemplateUsed(response, 'login.html')

    def test_logout_view(self):
        self.client.login(username='testuser', password='testpassword')
        response = self.client.get(reverse('logout'))
        self.assertRedirects(response, reverse('home'))
        self.assertFalse(response.wsgi_request.user.is_authenticated)


class ComprehensiveViewTests(TestCase):
    def setUp(self):
        # Setup a test client, create a test user and profile
        self.client = Client()
        self.profile = Profile.objects.create(user_id=3)
        self.client.login(user_id=3)  # Log in for testing
        # Test that a TestSession is created and questions are generated
        response = self.client.get(reverse('start_test'))
        # Check that it redirects to the 'instruction' page for 'stroop1'
        self.assertEqual(response.status_code, 302)
        self.assertRedirects(response, reverse(
            'instruction', args=['stroop1']))
        self.test_session = TestSession.objects.filter(user_id=1).first()
    
    def test_start_test_view(self):
        
        # Verify that a TestSession and Questions are created
        self.assertIsNotNone(self.test_session)
        
        # Ensures questions were generated
        questions_series = Questions.objects.filter(
            test_session_id=self.test_session).count()
        self.assertGreater(questions_series, len(Questions.TEST_TYPES))  

    def test_test_setup_function(self):
        # Directly test the test_setup utility function
        test_session = TestSession.objects.filter(user_id=1).first()
        test_type = 'stroop1'  # Example test type
        
        timer_seconds, template_name, questions = test_setup(
            test_session, test_type)
        
        # Check returned values
        self.assertEqual(timer_seconds, 20)  # Example timer for stroop1
        self.assertEqual(template_name, 'stroop_test.html')
        self.assertGreater(len(questions), 0)  # Questions should be non-empty

    def test_test_view_get(self):
        # Test GET request to `test` view for rendering the test
        response = self.client.get(reverse('test', args=['stroop1']))
        self.assertEqual(response.status_code, 200)
        self.assertTemplateUsed(response, 'stroop_test.html')

    def test_process_test_submission(self):

        # Mock user answer data for submission
        answers_data = [{'selectedAnswer': 'correct', 'time_taken': 2}]
        result = process_test_submission(self.test_session, answers_data, 'stroop1')

        # Verify results were saved
        saved_answer = Answer.objects.get(pk=answer.pk)
        self.assertEqual(saved_answer.given_answer, 'correct')

        result_entry = Results.objects.filter(test_session_id=test_session, questions_id=questions_series).first()
        self.assertIsNotNone(result_entry)
        self.assertIn('2', result_entry.result)
        
    def tearDown(self):
        self.client = Client()
        Profile.objects.filter(user_id=3).first().delete()