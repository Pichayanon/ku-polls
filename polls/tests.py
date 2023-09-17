import datetime

from django.test import TestCase
from django.utils import timezone
from django.urls import reverse
from django.contrib.auth.models import User

from .models import Question, Choice


class QuestionModelTests(TestCase):

    def test_was_published_recently_with_future_question(self):
        """
        was_published_recently() returns False for questions whose pub_date
        is in the future.
        """
        time = timezone.now() + datetime.timedelta(days=30)
        future_question = Question(pub_date=time)
        self.assertFalse(future_question.was_published_recently())

    def test_was_published_recently_with_old_question(self):
        """
        was_published_recently() returns False for questions whose pub_date
        is older than 1 day.
        """
        time = timezone.now() - datetime.timedelta(days=1, seconds=1)
        old_question = Question(pub_date=time)
        self.assertFalse(old_question.was_published_recently())

    def test_was_published_recently_with_recent_question(self):
        """
        was_published_recently() returns True for questions whose pub_date
        is within the last day.
        """
        time = timezone.now() - datetime.timedelta(hours=23, minutes=59, seconds=59)
        recent_question = Question(pub_date=time)
        self.assertTrue(recent_question.was_published_recently())

    def test_is_published_with_future_pub_date(self):
        """
        is_published() returns False for questions whose pub_date
        is in the future.
        """
        time = timezone.now() + datetime.timedelta(days=30)
        future_question = Question(pub_date=time)
        self.assertFalse(future_question.is_published())

    def test_is_published_with_default_pub_date(self):
        """
        is_published() returns True for questions whose pub_date
        is in the default pub date (now).
        """
        time = timezone.now()
        now_question = Question(pub_date=time)
        self.assertTrue(now_question.is_published())

    def test_is_published_with_past_pub_date(self):
        """
        is_published() returns True for questions whose pub_date
        is in the past.
        """
        time = timezone.now() - datetime.timedelta(days=30)
        past_question = Question(pub_date=time)
        self.assertTrue(past_question.is_published())

    def test_can_vote_after_pub_date_before_end_date(self):
        """
        can_vote() returns True if the pub_data is in the past
        and end_date is in the future.
        """
        past = timezone.now() - datetime.timedelta(days=30)
        future = timezone.now() + datetime.timedelta(days=30)
        question = Question(pub_date=past, end_date=future)
        self.assertTrue(question.can_vote())

    def test_can_vote_after_pub_date_null_end_date(self):
        """
        can_vote() returns True if the pub_data is in the past
        and end_date is null.
        """
        past = timezone.now() - datetime.timedelta(days=30)
        question = Question(pub_date=past)
        self.assertTrue(question.can_vote())

    def test_cannot_vote_before_pub_date(self):
        """
        can_vote() returns False if the pub_date is in the future.
        """
        future = timezone.now() + datetime.timedelta(days=30)
        question = Question(pub_date=future)
        self.assertFalse(question.can_vote())

    def test_cannot_vote_after_end_date(self):
        """
        can_vote() returns False if the end_date is in the past.
        """
        past = timezone.now() - datetime.timedelta(days=30)
        question = Question(end_date=past)
        self.assertFalse(question.can_vote())


def create_question(question_text, days):
    """
    Create a question with the given `question_text` and published the
    given number of `days` offset to now (negative for questions published
    in the past, positive for questions that have yet to be published).
    """
    time = timezone.now() + datetime.timedelta(days=days)
    return Question.objects.create(question_text=question_text, pub_date=time)


class QuestionIndexViewTests(TestCase):
    def test_no_questions(self):
        """
        If no questions exist, an appropriate message is displayed.
        """
        response = self.client.get(reverse('polls:index'))
        self.assertEqual(response.status_code, 200)
        self.assertContains(response, "No polls are available.")
        self.assertQuerysetEqual(response.context['latest_question_list'], [])

    def test_past_question(self):
        """
        Questions with a pub_date in the past are displayed on the
        index page.
        """
        question = create_question(question_text="Past question.", days=-30)
        response = self.client.get(reverse('polls:index'))
        self.assertQuerysetEqual(
            response.context['latest_question_list'],
            [question],
        )

    def test_future_question(self):
        """
        Questions with a pub_date in the future aren't displayed on
        the index page.
        """
        create_question(question_text="Future question.", days=30)
        response = self.client.get(reverse('polls:index'))
        self.assertContains(response, "No polls are available.")
        self.assertQuerysetEqual(response.context['latest_question_list'], [])

    def test_future_question_and_past_question(self):
        """
        Even if both past and future questions exist, only past questions
        are displayed.
        """
        question = create_question(question_text="Past question.", days=-30)
        create_question(question_text="Future question.", days=30)
        response = self.client.get(reverse('polls:index'))
        self.assertQuerysetEqual(
            response.context['latest_question_list'],
            [question],
        )

    def test_two_past_questions(self):
        """
        The questions index page may display multiple questions.
        """
        question1 = create_question(question_text="Past question 1.", days=-30)
        question2 = create_question(question_text="Past question 2.", days=-5)
        response = self.client.get(reverse('polls:index'))
        self.assertQuerysetEqual(
            response.context['latest_question_list'],
            [question2, question1],
        )


class QuestionDetailViewTests(TestCase):
    def test_future_question(self):
        """
        The detail view of a question with a pub_date in the future
        returns a 302.
        """
        future_question = create_question(question_text='Future question.', days=5)
        url = reverse('polls:detail', args=(future_question.id,))
        response = self.client.get(url)
        self.assertEqual(response.status_code, 302)

    def test_past_question(self):
        """
        The detail view of a question with a pub_date in the past
        displays the question's text.
        """
        past_question = create_question(question_text='Past Question.', days=-5)
        url = reverse('polls:detail', args=(past_question.id,))
        response = self.client.get(url)
        self.assertContains(response, past_question.question_text)


class AuthenticationTests(TestCase):
    def setUp(self):
        """
        Set up initial data for testing.
        """
        self.password = "test1234"
        self.tester = User.objects.create_user(username="tester", password=self.password)
        self.tester.first_name = "Tester"
        self.tester.save()
        self.question = Question.objects.create(question_text="Test question")
        self.question.save()
        self.choice = Choice(choice_text=f"Test choice", question=self.question)
        self.choice.save()

    def test_can_login_with_correct_username_password(self):
        """
        Test visitor log in with the correct username and password.
        After the visitor successfully logs in, they will move to the index page.
        """
        login = reverse("login")
        self.assertTrue(User.objects.filter(username=self.tester.username).exists())
        response = self.client.post(login, {"username": self.tester.username,
                                            "password": self.password})
        self.assertRedirects(response, reverse("polls:index"))

    def test_can_not_login_with_incorrect_password(self):
        """
        Test visitor who log in with the incorrect password.
        If the visitor enters the incorrect password, they will remain on the login page.
        """
        login = reverse("login")
        self.assertTrue(User.objects.filter(username=self.tester.username).exists())
        response = self.client.post(login, {"username": self.tester.username,
                                            "password": ""})
        self.assertEqual(response.status_code, 200)

    def test_can_not_login_with_incorrect_username(self):
        """
        Test visitor who log in with the incorrect username.
        If the visitor enters the incorrect username, they will remain on the login page.
        """
        login = reverse("login")
        self.assertFalse(User.objects.filter(username="").exists())
        response = self.client.post(login, {"username": "",
                                            "password": self.password})
        self.assertEqual(response.status_code, 200)

    def test_can_signup_with_valid_username_password(self):
        """
        Test visitor can register with a valid username and password.
        After visitor user register is complete, they will move to the index page.
        """
        signup = reverse("signup")
        response = self.client.post(signup, {"username": "Tester_Signup",
                                             "password1": "TS12345678", "password2": "TS12345678"})
        self.assertTrue(User.objects.filter(username="Tester_Signup").exists())
        self.assertRedirects(response, reverse("polls:index"))

    def test_can_not_signup_with_invalid_password(self):
        """
        Test visitor can register with an invalid password.
        If the visitor enters an invalid password, they will remain on the signup page.
        """
        signup = reverse("signup")
        response = self.client.post(signup, {'username': "Tester_Signup",
                                             'password1': "", 'password2': ""})
        self.assertFalse(User.objects.filter(username="Tester_Signup").exists())
        self.assertEqual(response.status_code, 200)

    def test_can_not_signup_with_invalid_username(self):
        """
        Test visitor can register with an invalid username.
        If the visitor enters an invalid username, they will remain on the signup page.
        """
        signup = reverse("signup")
        response = self.client.post(signup, {'username': "$",
                                             'password1': "TS12345678", "password2": "TS12345678"})
        self.assertFalse(User.objects.filter(username="Tester_Signup").exists())
        self.assertEqual(response.status_code, 200)

    def test_can_not_signup_with_invalid_confirm_password(self):
        """
        Test visitor can register with an invalid confirm password.
        If the visitor enters an invalid confirm password, they will remain on the signup page.
        """
        signup = reverse("signup")
        response = self.client.post(signup, {"username": "Tester_Signup",
                                             "password1": "TS12345678", "password2": "TS123456789"})
        self.assertFalse(User.objects.filter(username="Tester_Signup").exists())
        self.assertEqual(response.status_code, 200)

    def test_logout(self):
        """
        Test user logout.
        After the user logs out, they will move to the login page.
        """
        logout = reverse("logout")
        response = self.client.get(logout)
        self.assertRedirects(response, reverse("login"))
