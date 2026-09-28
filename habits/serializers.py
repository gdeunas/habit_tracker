from rest_framework import serializers
from .models import Habit
from rest_framework.pagination import PageNumberPagination
from django.contrib.auth import get_user_model


class HabitValidator:
    def __call__(self, attrs):
        is_pleasant = attrs.get("is_pleasant", False)
        related_habit = attrs.get("related_habit")
        reward = attrs.get("reward")
        periodicity = attrs.get("periodicity")

        # 1. Исключить одновременный выбор связанной привычки и вознаграждения
        if related_habit and reward:
            raise serializers.ValidationError(
                "Нельзя одновременно выбрать связанную привычку и вознаграждение."
            )

        # 2. У приятной привычки не может быть вознаграждения или связанной привычки
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

        # 4. Ограничение периодичности: нельзя выполнять реже, чем 1 раз в 7 дней
        if periodicity is not None and periodicity > 7:
            raise serializers.ValidationError(
                "Интервал выполнения привычки не может превышать 7 дней (минимум 1 раз в неделю)."
            )


class HabitPagination(PageNumberPagination):
    """Пагинация для привычек: по 5 элементов на страницу."""

    page_size = 5
    page_size_query_param = "page_size"
    max_page_size = 50


class HabitSerializer(serializers.ModelSerializer):
    class Meta:
        model = Habit
        fields = "__all__"
        read_only_fields = ("user",)
        validators = [HabitValidator()]


User = get_user_model()


class UserRegisterSerializer(serializers.ModelSerializer):
    password = serializers.CharField(write_only=True)

    class Meta:
        model = User
        fields = ("id", "username", "email", "password")

    def create(self, validated_data):
        # Хешируем пароль перед сохранением в базу данных
        user = User.objects.create_user(
            username=validated_data["username"],
            email=validated_data.get("email", ""),
            password=validated_data["password"],
        )
        return user
