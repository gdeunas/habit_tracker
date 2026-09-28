import requests
import os
from celery import shared_task
from django.utils import timezone
from .models import Habit
from dotenv import load_dotenv

load_dotenv()
BOT_TOKEN = os.getenv('TELEGRAM_BOT_TOKEN')

@shared_task
def send_habit_reminders():
    current_time = timezone.now().time()
    # Находим привычки, время которых подошло (с точностью до минуты)
    habits = Habit.objects.filter(
        time__hour=current_time.hour,
        time__minute=current_time.minute
    )

    for habit in habits:
        # Проверяем, есть ли у пользователя привязанный телеграм
        if hasattr(habit.user, 'telegram_chat_id') and habit.user.telegram_chat_id:
            text = f"Напоминание! Время пришло: я буду {habit.action} в {habit.time.strftime('%H:%M')} в {habit.place}."

            url = f"https://telegram.org{BOT_TOKEN}/sendMessage"
            data = {"chat_id": habit.user.telegram_chat_id, "text": text}
            requests.post(url, data=data)
