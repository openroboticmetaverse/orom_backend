from django.test import TestCase
from django.urls import reverse
from django.contrib.auth import get_user_model

from .forms import RegisterForm



class UserIntegrationTest(TestCase):

    def test_user_registration(self):
        """Test that a user can register and is redirected to the homepage"""
        response = self.client.post(reverse('register'), {
            'email': 'test@example.com',
            'username': 'testuser',
            'password1': 'Testpass123',
            'password2': 'Testpass123'
        })

        self.assertEqual(response.status_code, 302)  # Check for redirection
        self.assertRedirects(response, reverse('home'))  # Check redirection to home page

        user = get_user_model().objects.get(email='test@example.com')
        self.assertIsNotNone(user)  # Ensure the user is created



    def test_user_login(self):
        """Test that a user can log in"""
        # First, create a user manually
        user = get_user_model().objects.create_user(
            email='testlogin@example.com',
            username='loginuser',
            password='Testpass123'
        )

        # Now try to log the user in
        response = self.client.post(reverse('login'), {
            'username': 'testlogin@example.com',  # Since we log in using email
            'password': 'Testpass123'
        })

        self.assertEqual(response.status_code, 302)  # Check for redirection after login
        self.assertRedirects(response, reverse('home'))  # Ensure it redirects to the homepage



    def test_user_logout(self):
        """Test that a user can log out"""
        # First, log the user in
        self.client.login(username='testlogin@example.com', password='Testpass123')

        # Then log the user out
        response = self.client.get(reverse('logout'))

        self.assertEqual(response.status_code, 302)  # Check for redirection after logout
        self.assertRedirects(response, reverse('home'))  # Ensure it redirects to the homepage



class RegisterFormTest(TestCase):

    def test_register_form_valid(self):
        """Test that the registration form is valid with correct data"""
        form_data = {
            'email': 'user@example.com',
            'username': 'newuser',
            'password1': 'strongpassword123',
            'password2': 'strongpassword123'
        }
        form = RegisterForm(data=form_data)
        self.assertTrue(form.is_valid())



    def test_register_form_password_mismatch(self):
        """Test that the registration form raises error for password mismatch"""
        form_data = {
            'email': 'user@example.com',
            'username': 'newuser',
            'password1': 'strongpassword123',
            'password2': 'differentpassword123'
        }
        form = RegisterForm(data=form_data)
        self.assertFalse(form.is_valid())
        self.assertIn('password2', form.errors)



class CustomUserModelTest(TestCase):

    def test_create_user_with_email_and_username(self):
        """Test creating a new user with an email and username is successful"""
        email = 'test@example.com'
        username = 'testuser'
        password = 'Testpass123'
        user = get_user_model().objects.create_user(
            email=email,
            username=username,
            password=password
        )

        self.assertEqual(user.email, email)
        self.assertEqual(user.username, username)
        self.assertTrue(user.check_password(password))



    def test_new_user_email_normalized(self):
        """Test the email for a new user is normalized"""
        email = 'test@EXAMPLE.COM'
        user = get_user_model().objects.create_user(email, 'testuser', 'test123')
        self.assertEqual(user.email, email.lower())



    def test_create_user_invalid_email(self):
        """Test creating user with no email raises error"""
        with self.assertRaises(ValueError):
            get_user_model().objects.create_user(None, 'testuser', 'test123')



    def test_create_superuser(self):
        """Test creating a superuser"""
        user = get_user_model().objects.create_superuser(
            'super@example.com',
            'superuser',
            'superpassword123'
        )
        self.assertTrue(user.is_admin)
