from rest_framework import viewsets, mixins
from rest_framework.permissions import IsAuthenticated
from .models import Habit
from .serializers import HabitSerializer
from .permissions import IsOwner
from .serializers import HabitPagination

from rest_framework import generics
from rest_framework.permissions import AllowAny
from django.contrib.auth import get_user_model
from .serializers import UserRegisterSerializer


class HabitViewSet(viewsets.ModelViewSet):
    """CRUD для привычек текущего пользователя."""
    serializer_class = HabitSerializer
    permission_classes = [IsAuthenticated, IsOwner]

    def get_queryset(self):
        # Пользователь видит только свои привычки
        return Habit.objects.filter(user=self.request.user)

    def perform_create(self, serializer):
        # Автоматически привязываем создателя к привычке
        serializer.save(user=self.request.user)

    pagination_class = HabitPagination



class PublicHabitViewSet(mixins.ListModelMixin, viewsets.GenericViewSet):
    """Просмотр списка всех публичных привычек."""
    serializer_class = HabitSerializer
    queryset = Habit.objects.filter(is_public=True)
    permission_classes = [IsAuthenticated]

class UserRegisterView(generics.CreateAPIView):
    """Эндпоинт регистрации нового пользователя."""
    queryset = get_user_model().objects.all()
    serializer_class = UserRegisterSerializer
    permission_classes = [AllowAny]
