from rest_framework import serializers
from .models import Habit


class HabitValidator:
    """Валидатор для проверки бизнес-логики привычек."""

    def __call__(self, attrs):
        is_pleasant = attrs.get('is_pleasant', False)
        related_habit = attrs.get('related_habit')
        reward = attrs.get('reward')

        # 1. Исключение одновременного выбора связанной привычки и вознаграждения
        if related_habit and reward:
            raise serializers.ValidationError(
                "Нельзя одновременно выбрать связанную привычку и вознаграждение."
            )

        # 4. Условия для приятной привычки: не может иметь вознаграждения или связанной привычки
        if is_pleasant:
            if reward or related_habit:
                raise serializers.ValidationError(
                    "У приятной привычки не может быть вознаграждения или связанной привычки."
                )

        # 3. В связанные привычки могут попадать только привычки с признаком приятной
        if related_habit and not related_habit.is_pleasant:
            raise serializers.ValidationError(
                "В связанные привычки можно добавлять только привычки с признаком приятной."
            )


class HabitSerializer(serializers.ModelSerializer):
    class Meta:
        model = Habit
        fields = '__all__'
        read_only_fields = ('user',)  # Пользователь проставляется автоматически из реквеста
        validators = [HabitValidator()]
