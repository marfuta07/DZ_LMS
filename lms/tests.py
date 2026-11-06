from django.test import TestCase
from django.contrib.auth.models import Group
from django.urls import reverse
from rest_framework.test import APITestCase, APIClient
from rest_framework import status

from users.models import User
from lms.models import Course, Lesson, Subscription


class LessonTestCase(APITestCase):
    """Тесты CRUD уроков с разными правами."""

    def setUp(self):
        self.user = User.objects.create_user(email='user@test.com', password='test12345')
        self.moderator = User.objects.create_user(email='mod@test.com', password='test12345')
        self.admin = User.objects.create_superuser(email='admin@test.com', password='test12345')

        group, _ = Group.objects.get_or_create(name='Модераторы')
        self.moderator.groups.add(group)

        self.course = Course.objects.create(title='Курс 1', owner=self.user)
        self.lesson = Lesson.objects.create(
            title='Урок 1', course=self.course,
            video_link='https://youtube.com/watch?v=1', owner=self.user
        )

        self.client = APIClient()

    def test_create_lesson(self):
        self.client.force_authenticate(user=self.admin)
        data = {
            'title': 'Новый урок',
            'course': self.course.id,
            'video_link': 'https://youtube.com/watch?v=2'
        }
        response = self.client.post('/api/lessons/', data)
        self.assertEqual(response.status_code, status.HTTP_201_CREATED)
        self.assertEqual(Lesson.objects.count(), 2)

    def test_create_lesson_invalid_url(self):
        self.client.force_authenticate(user=self.admin)
        data = {
            'title': 'Урок',
            'course': self.course.id,
            'video_link': 'https://vimeo.com/123'
        }
        response = self.client.post('/api/lessons/', data)
        self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)
        self.assertIn('video_link', response.data)

    def test_list_lessons(self):
        self.client.force_authenticate(user=self.user)
        response = self.client.get('/api/lessons/')
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(response.data['count'], 1)

    def test_update_lesson(self):
        self.client.force_authenticate(user=self.user)
        data = {'title': 'Обновлённый урок'}
        response = self.client.patch(f'/api/lessons/{self.lesson.id}/', data)
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.lesson.refresh_from_db()
        self.assertEqual(self.lesson.title, 'Обновлённый урок')

    def test_delete_lesson(self):
        self.client.force_authenticate(user=self.user)
        response = self.client.delete(f'/api/lessons/{self.lesson.id}/')
        self.assertEqual(response.status_code, status.HTTP_204_NO_CONTENT)
        self.assertEqual(Lesson.objects.count(), 0)

    def test_anonymous_cannot_access(self):
        response = self.client.get('/api/lessons/')
        self.assertEqual(response.status_code, status.HTTP_401_UNAUTHORIZED)

    def test_moderator_cannot_create_lesson(self):
        self.client.force_authenticate(user=self.moderator)
        data = {'title': 'Новый урок', 'course': self.course.id}
        response = self.client.post('/api/lessons/', data)
        self.assertEqual(response.status_code, status.HTTP_403_FORBIDDEN)

    def test_moderator_can_view_lessons(self):
        self.client.force_authenticate(user=self.moderator)
        response = self.client.get('/api/lessons/')
        self.assertEqual(response.status_code, status.HTTP_200_OK)

    def test_moderator_cannot_delete_lesson(self):
        self.client.force_authenticate(user=self.moderator)
        response = self.client.delete(f'/api/lessons/{self.lesson.id}/')
        self.assertEqual(response.status_code, status.HTTP_403_FORBIDDEN)

    def test_user_cannot_access_other_lesson(self):
        other_user = User.objects.create_user(email='other@test.com', password='test12345')
        other_course = Course.objects.create(title='Чужой курс', owner=other_user)
        other_lesson = Lesson.objects.create(title='Чужой урок', course=other_course, owner=other_user)

        self.client.force_authenticate(user=self.user)
        response = self.client.get(f'/api/lessons/{other_lesson.id}/')
        self.assertEqual(response.status_code, status.HTTP_404_NOT_FOUND)


class SubscriptionTestCase(APITestCase):
    """Тесты подписки на курс."""

    def setUp(self):
        self.user = User.objects.create_user(email='user@test.com', password='test12345')
        self.course = Course.objects.create(title='Курс 1', owner=self.user)
        self.client = APIClient()

    def test_subscribe_to_course(self):
        self.client.force_authenticate(user=self.user)
        response = self.client.post(
            f'/api/courses/{self.course.id}/subscribe/',
            {'course_id': self.course.id}
        )
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(response.data['message'], 'подписка добавлена')
        self.assertTrue(Subscription.objects.filter(user=self.user, course=self.course).exists())

    def test_unsubscribe_from_course(self):
        self.client.force_authenticate(user=self.user)
        Subscription.objects.create(user=self.user, course=self.course)
        response = self.client.post(
            f'/api/courses/{self.course.id}/subscribe/',
            {'course_id': self.course.id}
        )
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(response.data['message'], 'подписка удалена')
        self.assertFalse(Subscription.objects.filter(user=self.user, course=self.course).exists())

    def test_is_subscribed_field(self):
        self.client.force_authenticate(user=self.user)
        Subscription.objects.create(user=self.user, course=self.course)
        response = self.client.get(f'/api/courses/{self.course.id}/')
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertTrue(response.data['is_subscribed'])
