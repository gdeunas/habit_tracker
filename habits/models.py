from django.db import models
from django.conf import settings
from django.core.validators import MaxValueValidator, MinValueValidator


class Habit(models.Model):
    user = models.ForeignKey(
        settings.AUTH_USER_MODEL,
        on_delete=models.CASCADE,
        verbose_name="Создатель привычки",
        related_name="habits"
    )
    place = models.CharField(max_length=255, verbose_name="Место")
    time = models.TimeField(verbose_name="Время выполнения")
    action = models.CharField(max_length=255, verbose_name="Действие")

    is_pleasant = models.BooleanField(default=False, verbose_name="Признак приятной привычки")

    related_habit = models.ForeignKey(
        'self',
        on_delete=models.SET_NULL,
        null=True,
        blank=True,
        verbose_name="Связанная привычка",
        related_name="primary_habits"
    )

    # Периодичность в днях (по умолчанию 1 - каждый день)
    periodicity = models.PositiveSmallIntegerField(
        default=1,
        validators=[MinValueValidator(1), MaxValueValidator(7)],
        verbose_name="Периодичность (в днях)"
    )

    reward = models.CharField(max_length=255, null=True, blank=True, verbose_name="Вознаграждение")

    # Время на выполнение в секундах (по ТЗ не больше 2 минут = 120 секунд)
    duration = models.PositiveIntegerField(
        default=60,
        validators=[MaxValueValidator(120)],
        verbose_name="Время на выполнение (в секундах)"
    )

    is_public = models.BooleanField(default=False, verbose_name="Признак публичности")

    class Meta:
        verbose_name = "Привилегия/Привычка"
        verbose_name_plural = "Привычки"
        ordering = ['id']

    def __str__(self):
        return f"{self.user} будет {self.action} в {self.time} в {self.place}"
