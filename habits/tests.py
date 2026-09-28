from django.contrib.auth import get_user_model
from django.urls import reverse
from rest_framework import status
from rest_framework.test import APITestCase
from .models import Habit

User = get_user_model()


class HabitTestCase(APITestCase):

    def setUp(self):
        # Создаем тестового пользователя и авторизуем его
        self.user = User.objects.create_user(username="testuser", password="testpassword123")
        self.client.force_authenticate(user=self.user)

        # Создаем базовую приятную привычку для тестов связанных привычек
        self.pleasant_habit = Habit.objects.create(
            user=self.user,
            place="Дом",
            time="08:00:00",
            action="Принять пенную ванну",
            is_pleasant=True,
            duration=60
        )

    def test_create_habit_success(self):
        """Тест успешного создания полезной привычки."""
        data = {
            "place": "Парк",
            "time": "07:00:00",
            "action": "Пробежка 1 км",
            "is_pleasant": False,
            "reward": "Скушать яблоко",
            "duration": 90,
            "periodicity": 1
        }
        response = self.client.post(reverse('habits-list'), data=data)
        self.assertEqual(response.status_code, status.HTTP_201_CREATED)
        self.assertEqual(Habit.objects.filter(action="Пробежка 1 км").count(), 1)

    def test_duration_validation_error(self):
        """Тест: время выполнения привычки не должно превышать 120 секунд."""
        data = {
            "place": "Парк",
            "time": "07:00:00",
            "action": "Долгая пробежка",
            "duration": 150,  # Ошибка: больше 120
            "periodicity": 1
        }
        response = self.client.post(reverse('habits-list'), data=data)
        self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)

    def test_simultaneous_reward_and_related_error(self):
        """Тест: нельзя одновременно указать награду и связанную привычку."""
        data = {
            "place": "Дом",
            "time": "09:00:00",
            "action": "Почитать книгу",
            "related_habit": self.pleasant_habit.id,
            "reward": "Шоколадка",  # Ошибка: заполнено оба поля
            "duration": 60,
            "periodicity": 1
        }
        response = self.client.post(reverse('habits-list'), data=data)
        self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)

    def test_periodicity_validation_error(self):
        """Тест: периодичность выполнения не может быть реже чем раз в 7 дней."""
        data = {
            "place": "Зал",
            "time": "18:00:00",
            "action": "Тяжелая тренировка",
            "duration": 60,
            "periodicity": 10  # Ошибка: больше 7 дней
        }
        response = self.client.post(reverse('habits-list'), data=data)
        self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)

    def test_get_habits_list_pagination(self):
        """Тест работы пагинации списка привычек текущего пользователя."""
        response = self.client.get(reverse('habits-list'))
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        # Проверяем структуру пагинации, требуемую по ТЗ
        self.assertIn('count', response.data)
        self.assertIn('results', response.data)
