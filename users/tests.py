from rest_framework.test import APITestCase
from django.urls import reverse
from rest_framework import status
from users.models import User, Role


class UserAPITestCase(APITestCase):

    def setUp(self):
        self.admin_role = Role.objects.create(name='admin')
        self.analyst_role = Role.objects.create(name='analyst')

        self.admin = User.objects.create_user(
            email='admin@test.com',
            password='Admin@123',
            name='Admin',
            role=self.admin_role
        )

        self.login_url = reverse('user-login')
        self.user_list_url = reverse('user-list-create')

    def authenticate(self, email, password):
        response = self.client.post(self.login_url, {
            "email": email,
            "password": password
        })
        token = response.data['access']
        self.client.credentials(HTTP_AUTHORIZATION=f'Bearer {token}')


    def test_login_success(self):
        data = {
            "email": "admin@test.com",
            "password": "Admin@123"
        }

        response = self.client.post(self.login_url, data)

        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertIn('access', response.data)
        self.assertIn('refresh', response.data)
        self.assertIn('user', response.data)

    def test_login_invalid_credentials(self):
        data = {
            "email": "admin@test.com",
            "password": "wrongpassword"
        }

        response = self.client.post(self.login_url, data)

        self.assertEqual(response.status_code, status.HTTP_401_UNAUTHORIZED)


    def test_create_user_success(self):
        self.authenticate("admin@test.com", "Admin@123")

        data = {
            "email": "user@test.com",
            "name": "Test User",
            "password": "StrongPass@123",
            "confirm_password": "StrongPass@123",
            "role": self.analyst_role.id
        }

        response = self.client.post(self.user_list_url, data)

        self.assertEqual(response.status_code, status.HTTP_201_CREATED)
        self.assertEqual(User.objects.count(), 2)

    def test_create_user_non_admin(self):
        user = User.objects.create_user(
            email='analyst@test.com',
            password='Test@123',
            name='Analyst',
            role=self.analyst_role
        )

        self.authenticate("analyst@test.com", "Test@123")

        data = {
            "email": "new@test.com",
            "name": "User",
            "password": "StrongPass@123",
            "confirm_password": "StrongPass@123",
            "role": self.analyst_role.id
        }

        response = self.client.post(self.user_list_url, data)

        self.assertEqual(response.status_code, status.HTTP_403_FORBIDDEN)

    def test_create_user_password_mismatch(self):
        self.authenticate("admin@test.com", "Admin@123")

        data = {
            "email": "user@test.com",
            "name": "Test User",
            "password": "12345678",
            "confirm_password": "87654321",
            "role": self.analyst_role.id
        }

        response = self.client.post(self.user_list_url, data)

        self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)


    def test_get_user_detail(self):
        self.authenticate("admin@test.com", "Admin@123")

        url = reverse('user-detail', kwargs={'pk': self.admin.id})
        response = self.client.get(url)

        self.assertEqual(response.status_code, status.HTTP_200_OK)

    def test_update_user(self):
        self.authenticate("admin@test.com", "Admin@123")

        url = reverse('user-detail', kwargs={'pk': self.admin.id})

        response = self.client.patch(url, {"name": "Updated"})

        self.assertEqual(response.status_code, status.HTTP_200_OK)

        self.admin.refresh_from_db()
        self.assertEqual(self.admin.name, "Updated")

    def test_user_detail_non_admin(self):
        user = User.objects.create_user(
            email='analyst@test.com',
            password='Test@123',
            name='Analyst',
            role=self.analyst_role
        )

        self.authenticate("analyst@test.com", "Test@123")

        url = reverse('user-detail', kwargs={'pk': user.id})
        response = self.client.get(url)

        self.assertEqual(response.status_code, status.HTTP_403_FORBIDDEN)