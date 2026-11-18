from django.test import TestCase, Client
from django.urls import reverse
from django.contrib.auth import get_user_model

CustomUser = get_user_model()

class AccountFeatureTests(TestCase):
    def setUp(self):
        self.client = Client()
        # Creator user
        self.creator = CustomUser.objects.create_user(
            username='testcreator',
            email='creator@pulztube.com',
            password='Password123!',
            first_name='Joshua',
            last_name='Raagas',
            role=CustomUser.Role.CREATOR,
            channel_name='Joshua Tech',
            niche='Tech & Coding'
        )
        # Admin user
        self.admin = CustomUser.objects.create_user(
            username='testadmin',
            email='admin@pulztube.com',
            password='AdminPassword123!',
            first_name='Admin',
            last_name='User',
            role=CustomUser.Role.ADMIN
        )

    def test_account_registration_success(self):
        """Test successful registration with password hashing and default CREATOR role."""
        response = self.client.post(reverse('signup'), {
            'username': 'newcreator',
            'email': 'new@pulztube.com',
            'first_name': 'New',
            'last_name': 'Creator',
            'channel_name': 'My New Channel',
            'niche': 'Gaming',
            'contact_number': '+639123456789',
            'password1': 'SecurePass123!',
            'password2': 'SecurePass123!',
        })
        self.assertEqual(response.status_code, 302)  # Redirects to login
        self.assertTrue(CustomUser.objects.filter(username='newcreator').exists())
        user = CustomUser.objects.get(username='newcreator')
        self.assertEqual(user.role, CustomUser.Role.CREATOR)
        self.assertTrue(user.check_password('SecurePass123!'))

    def test_account_registration_duplicate_email(self):
        """Test that registering with an existing email is rejected."""
        response = self.client.post(reverse('signup'), {
            'username': 'anotheruser',
            'email': 'creator@pulztube.com',  # Duplicate email
            'first_name': 'Duplicate',
            'last_name': 'User',
            'password1': 'SecurePass123!',
            'password2': 'SecurePass123!',
        })
        self.assertEqual(response.status_code, 200)
        self.assertFalse(CustomUser.objects.filter(username='anotheruser').exists())
        self.assertFormError(
            response.context['form'],
            'email',
            'An account with this email address already exists.'
        )

    def test_account_registration_password_mismatch(self):
        """Test that non-matching password confirmation is rejected."""
        response = self.client.post(reverse('signup'), {
            'username': 'mismatchuser',
            'email': 'mismatch@pulztube.com',
            'first_name': 'Mismatch',
            'last_name': 'User',
            'password1': 'SecurePass123!',
            'password2': 'DifferentPass123!',
        })
        self.assertEqual(response.status_code, 200)
        self.assertFalse(CustomUser.objects.filter(username='mismatchuser').exists())

    def test_login_success(self):
        """Test successful login redirects through role dispatch."""
        response = self.client.post(reverse('login'), {
            'username': 'testcreator',
            'password': 'Password123!',
        })
        self.assertEqual(response.status_code, 302)
        # Follow redirect to role_redirect -> creator_dashboard
        redirect_response = self.client.get(response.url)
        self.assertEqual(redirect_response.status_code, 302)
        self.assertEqual(redirect_response.url, reverse('creator_dashboard'))

    def test_login_invalid_credentials(self):
        """Test login with wrong password shows error message."""
        response = self.client.post(reverse('login'), {
            'username': 'testcreator',
            'password': 'WrongPassword!',
        })
        self.assertEqual(response.status_code, 200)
        self.assertContains(response, 'Invalid username or password')

    def test_logout(self):
        """Test logging out terminates the session."""
        self.client.login(username='testcreator', password='Password123!')
        response = self.client.post(reverse('logout'))
        self.assertEqual(response.status_code, 302)
        # Attempting to access profile afterwards redirects to login
        profile_response = self.client.get(reverse('profile'))
        self.assertEqual(profile_response.status_code, 302)
        self.assertIn('/accounts/login/', profile_response.url)

    def test_protected_pages_redirect_logged_out_users(self):
        """Test that unauthenticated users cannot view protected profile or dashboard."""
        self.client.logout()
        for url_name in ['profile', 'profile_edit', 'creator_dashboard', 'admin_dashboard']:
            response = self.client.get(reverse(url_name))
            self.assertEqual(response.status_code, 302)
            self.assertIn('/accounts/login/', response.url)

    def test_user_can_view_and_edit_own_profile(self):
        """Test user can view and update their profile details."""
        self.client.login(username='testcreator', password='Password123!')
        
        # View profile
        view_response = self.client.get(reverse('profile'))
        self.assertEqual(view_response.status_code, 200)
        self.assertContains(view_response, 'creator@pulztube.com')
        self.assertContains(view_response, 'Joshua Tech')

        # Edit profile
        edit_response = self.client.post(reverse('profile_edit'), {
            'first_name': 'Joshua Ephraim',
            'last_name': 'Raagas',
            'email': 'creator_updated@pulztube.com',
            'channel_name': 'Joshua Tech Pro',
            'channel_id': '@joshuatechpro',
            'niche': 'Software Development',
            'content_interests': 'Django, Python, YouTube Growth',
            'contact_number': '+639999999999',
        })
        self.assertEqual(edit_response.status_code, 302)
        self.creator.refresh_from_db()
        self.assertEqual(self.creator.first_name, 'Joshua Ephraim')
        self.assertEqual(self.creator.channel_name, 'Joshua Tech Pro')
        self.assertEqual(self.creator.email, 'creator_updated@pulztube.com')
