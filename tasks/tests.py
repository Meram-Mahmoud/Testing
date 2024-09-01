from django.test import TestCase
from django.contrib.auth.models import User
from tasks.models import Task
from rest_framework import status
from rest_framework.test import APIClient

class TaskTests(TestCase):
    def setUp(self):
        self.user = User.objects.create_user(username='testuser', password='12345')
        self.client = APIClient()
        self.client.force_authenticate(user=self.user)
        self.task = Task.objects.create(title="Test Task", description="Test Description", status=False, user=self.user)

    def test_create_task_success(self):
        response = self.client.post('/', {'user': self.user.id,'title': 'New Task', 'description': 'New Description', 'status': True}, format='json')
        self.assertEqual(response.status_code, status.HTTP_201_CREATED)
        self.assertEqual(response.data['title'], 'New Task')

    def test_create_task_missing_field(self):
        response = self.client.post('/', {'description': 'New Description', 'status': True}, format='json')
        self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)

    def test_read_task_success(self):
        response = self.client.get(f'/{self.task.id}/')
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(response.data['title'], 'Test Task')

    def test_read_task_not_found(self):
        response = self.client.get('/999/')
        self.assertEqual(response.status_code, status.HTTP_404_NOT_FOUND)

    def test_update_task_success(self):
        response = self.client.put(f'/{self.task.id}/', {'user': self.user.id, 'title': 'Updated Task', 'description': 'Updated Description', 'status': True}, format='json')
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(response.data['title'], 'Updated Task')

    def test_update_task_invalid_data(self):
        response = self.client.put(f'/{self.task.id}/', {'title': ''}, format='json')
        self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)

    def test_delete_task_success(self):
        response = self.client.delete(f'/{self.task.id}/')
        self.assertEqual(response.status_code, status.HTTP_204_NO_CONTENT)

    def test_delete_task_not_found(self):
        response = self.client.delete('/999/')
        self.assertEqual(response.status_code, status.HTTP_404_NOT_FOUND)
