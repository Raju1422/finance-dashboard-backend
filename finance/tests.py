from rest_framework.test import APITestCase
from django.urls import reverse
from rest_framework import status
from users.models import User, Role
from finance.models import Category, Record
from datetime import date


class FinanceAPITestCase(APITestCase):

    def setUp(self):
        self.admin_role = Role.objects.create(name='admin')
        self.analyst_role = Role.objects.create(name='analyst')
        self.viewer_role = Role.objects.create(name='viewer')

        self.admin = User.objects.create_user(
            email='admin@test.com',
            password='Admin@123',
            name='Admin',
            role=self.admin_role
        )

        self.analyst = User.objects.create_user(
            email='analyst@test.com',
            password='Test@123',
            name='Analyst',
            role=self.analyst_role
        )
        self.viewer = User.objects.create_user(
            email='viewer@test.com',
            password='Viewer@123',
            name='Viewer',
            role=self.viewer_role
        )

        self.login_url = reverse('user-login')
        self.category_url = reverse('category-list-create')
        self.record_url = reverse('record-list-create')
        self.dashboard_url = reverse('dashboard')

        self.category = Category.objects.create(name="food", type="expense")
        self.income_category = Category.objects.create(name="salary", type="income")

    def authenticate(self, email, password):
        response = self.client.post(self.login_url, {
            "email": email,
            "password": password
        })
        token = response.data['access']
        self.client.credentials(HTTP_AUTHORIZATION=f'Bearer {token}')


    def test_create_category_admin(self):
        self.authenticate("admin@test.com", "Admin@123")

        data = {"name": "Transport", "type": "expense"}
        response = self.client.post(self.category_url, data)

        self.assertEqual(response.status_code, status.HTTP_201_CREATED)

    def test_create_category_non_admin(self):
        self.authenticate("analyst@test.com", "Test@123")

        data = {"name": "Transport", "type": "expense"}
        response = self.client.post(self.category_url, data)

        self.assertEqual(response.status_code, status.HTTP_403_FORBIDDEN)

    def test_duplicate_category(self):
        self.authenticate("admin@test.com", "Admin@123")

        data = {"name": "Food", "type": "expense"}
        response = self.client.post(self.category_url, data)

        self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)


    def test_create_record_admin(self):
        self.authenticate("admin@test.com", "Admin@123")

        data = {
            "amount": 500,
            "category": self.category.id,
            "date": str(date.today()),
            "description": "Lunch"
        }

        response = self.client.post(self.record_url, data)

        self.assertEqual(response.status_code, status.HTTP_201_CREATED)

    def test_create_record_analyst_forbidden(self):
        self.authenticate("analyst@test.com", "Test@123")

        data = {
            "amount": 500,
            "category": self.category.id,
            "date": str(date.today())
        }

        response = self.client.post(self.record_url, data)

        self.assertEqual(response.status_code, status.HTTP_403_FORBIDDEN)
    
    def test_viewer_cannot_create_record(self):
        self.authenticate("viewer@test.com", "Viewer@123")

        data = {
            "amount": 500,
            "category": self.category.id,
            "date": str(date.today())
        }

        response = self.client.post(self.record_url, data)

        self.assertEqual(response.status_code, status.HTTP_403_FORBIDDEN)
        
    def test_viewer_cannot_access_records(self):
        self.authenticate("viewer@test.com", "Viewer@123")

        response = self.client.get(self.record_url)

        self.assertEqual(response.status_code, status.HTTP_403_FORBIDDEN)
        
    def test_invalid_amount(self):
        self.authenticate("admin@test.com", "Admin@123")

        data = {
            "amount": -100,
            "category": self.category.id,
            "date": str(date.today())
        }

        response = self.client.post(self.record_url, data)

        self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)

    def test_filter_by_category(self):
        self.authenticate("admin@test.com", "Admin@123")

        Record.objects.create(
            user=self.admin,
            amount=200,
            category=self.category,
            date=date.today()
        )

        url = f"{self.record_url}?category={self.category.id}"
        response = self.client.get(url)

        self.assertEqual(response.status_code, status.HTTP_200_OK)


    def test_dashboard(self):
        self.authenticate("admin@test.com", "Admin@123")

        Record.objects.create(
            user=self.admin,
            amount=5000,
            category=self.income_category,
            date=date.today()
        )

        Record.objects.create(
            user=self.admin,
            amount=1000,
            category=self.category,
            date=date.today()
        )

        response = self.client.get(self.dashboard_url)

        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertIn('total_income', response.data)
        self.assertIn('total_expense', response.data)
        self.assertIn('net_balance', response.data)
        
    def test_viewer_can_access_dashboard(self):
        self.authenticate("viewer@test.com", "Viewer@123")

        response = self.client.get(self.dashboard_url)

        self.assertEqual(response.status_code, status.HTTP_200_OK)