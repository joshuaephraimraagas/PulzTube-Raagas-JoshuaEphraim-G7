from django.test import TestCase, Client
from django.urls import reverse
from django.contrib.auth import get_user_model

CustomUser = get_user_model()

class RoleBasedDashboardTests(TestCase):
    def setUp(self):
        self.client = Client()
        self.creator = CustomUser.objects.create_user(
            username='creator_user',
            email='creator@pulztube.com',
            password='Password123!',
            role=CustomUser.Role.CREATOR,
            channel_name='Creator Channel'
        )
        self.admin = CustomUser.objects.create_user(
            username='admin_user',
            email='admin@pulztube.com',
            password='AdminPassword123!',
            role=CustomUser.Role.ADMIN
        )

    def test_creator_login_redirects_to_creator_dashboard(self):
        """A logged-in Creator must land on the Creator Dashboard."""
        self.client.login(username='creator_user', password='Password123!')
        response = self.client.get(reverse('role_redirect'))
        self.assertEqual(response.status_code, 302)
        self.assertEqual(response.url, reverse('creator_dashboard'))

        dashboard_response = self.client.get(reverse('creator_dashboard'))
        self.assertEqual(dashboard_response.status_code, 200)
        self.assertContains(dashboard_response, 'Creator Workspace')
        self.assertContains(dashboard_response, 'Content Production Pipeline')

    def test_admin_login_redirects_to_admin_dashboard(self):
        """A logged-in Admin must land on the Admin Dashboard."""
        self.client.login(username='admin_user', password='AdminPassword123!')
        response = self.client.get(reverse('role_redirect'))
        self.assertEqual(response.status_code, 302)
        self.assertEqual(response.url, reverse('admin_dashboard'))

        admin_dashboard_response = self.client.get(reverse('admin_dashboard'))
        self.assertEqual(admin_dashboard_response.status_code, 200)
        self.assertContains(admin_dashboard_response, 'Administrator Console')
        self.assertContains(admin_dashboard_response, 'Total Registered Users')

    def test_creator_cannot_access_admin_dashboard_by_url(self):
        """
        RUBRIC REQUIREMENT:
        'A user must not be able to open another role’s dashboard by typing its URL.'
        When a Creator types /admin-panel/, they must be denied and redirected.
        """
        self.client.login(username='creator_user', password='Password123!')
        response = self.client.get(reverse('admin_dashboard'), follow=True)
        # Verify redirect occurred to creator_dashboard
        self.assertEqual(response.status_code, 200)
        self.assertRedirects(response, reverse('creator_dashboard'))
        # Verify clear security warning message
        self.assertContains(
            response,
            "Access Denied: You do not have permission to view the Administrator Dashboard."
        )

    def test_admin_accessing_creator_dashboard_redirects_to_admin(self):
        """Admins typing /creator/ are routed back to their admin dashboard."""
        self.client.login(username='admin_user', password='AdminPassword123!')
        response = self.client.get(reverse('creator_dashboard'), follow=True)
        self.assertEqual(response.status_code, 200)
        self.assertRedirects(response, reverse('admin_dashboard'))
