from django.test import TestCase
from django.urls import reverse
from django.contrib.auth.models import User

from polls.models import Question, Choice


class AuthenticationTests(TestCase):
    def setUp(self):
        """
        Set up initial data for testing.
        """
        self.password = "test1234"
        self.tester = User.objects.create_user(username="tester",
                                               password=self.password)
        self.tester.first_name = "Tester"
        self.tester.save()
        self.question = Question.objects.create(question_text="Test question")
        self.question.save()
        self.choice = Choice(choice_text="Test choice", question=self.question)
        self.choice.save()

    def test_can_login_with_correct_username_password(self):
        """
        If the visitor log in with the correct username and password,
        they will move to the index page.
        """
        login = reverse("login")
        response = self.client.post(login, {"username": self.tester.username,
                                            "password": self.password})
        self.assertRedirects(response, reverse("polls:index"))

    def test_can_not_login_with_incorrect_username_password(self):
        """
        If the visitor log in with the incorrect username or password,
        they will remain on the login page.
        """
        login = reverse("login")
        # Check not exists username
        response = self.client.post(login, {"username": "",
                                            "password": self.password})
        self.assertEqual(response.status_code, 200)

        # Check incorrect password
        response = self.client.post(login, {"username": self.tester.username,
                                            "password": ""})
        self.assertEqual(response.status_code, 200)

    def test_can_signup_with_valid_username_password(self):
        """
        If the visitor register with a valid username and password,
        they will move to the index page.
        """
        signup = reverse("signup")
        response = self.client.post(signup, {"username": "Tester_Signup",
                                             "password1": "TS12345678",
                                             "password2": "TS12345678"})
        self.assertTrue(User.objects.filter(username="Tester_Signup").exists())
        self.assertRedirects(response, reverse("polls:index"))

    def test_can_not_signup_with_invalid_username_password(self):
        """
        If the visitor register with an invalid username or password,
        they will remain on the signup page.
        """
        signup = reverse("signup")
        # Check invalid username
        response = self.client.post(signup, {"username": "$",
                                             "password1": "TS12345678",
                                             "password2": "TS12345678"})
        self.assertFalse(User.objects.filter(username="$").exists())
        self.assertEqual(response.status_code, 200)

        # Check invalid password
        response = self.client.post(signup, {"username": "Tester_Signup",
                                             "password1": "1",
                                             "password2": "1"})
        self.assertEqual(response.status_code, 200)

        # Check exists username
        response = self.client.post(signup, {"username": self.tester.username,
                                             "password1": "TS12345678",
                                             "password2": "TS12345678"})
        self.assertEqual(response.status_code, 200)

    def test_logout(self):
        """
        Test user logout.
        After the user logs out, they will move to the login page.
        """
        logout = reverse("logout")
        response = self.client.get(logout)
        self.assertRedirects(response, reverse("login"))
