from rest_framework import viewsets

# from rest_framework import permissions
# from rest_framework.throttling import AnonRateThrottle
from rest_framework.throttling import ScopedRateThrottle
from django_filters.rest_framework import DjangoFilterBackend
from rest_framework import filters

from .models import Achievement, Cat, User

from .serializers import AchievementSerializer, CatSerializer, UserSerializer

from .permissions import OwnerOrReadOnly  # , ReadOnly
from .throttling import WorkingHoursRateThrottle
# from .pagination import CatsPagination


class CatViewSet(viewsets.ModelViewSet):
    queryset = Cat.objects.all()
    serializer_class = CatSerializer
    permission_classes = (OwnerOrReadOnly,)
    throttle_classes = (WorkingHoursRateThrottle, ScopedRateThrottle)
    filter_backends = (DjangoFilterBackend, filters.SearchFilter, filters.OrderingFilter)
    pagination_class = None
    filterset_fields = ("color", "birth_year")
    search_fields = ('name',) 
    ordering_fields = ('name', 'birth_year')
    ordering = ('birth_year',)
    
    def perform_create(self, serializer):
        serializer.save(owner=self.request.user)


class UserViewSet(viewsets.ReadOnlyModelViewSet):
    queryset = User.objects.all()
    serializer_class = UserSerializer


class AchievementViewSet(viewsets.ModelViewSet):
    queryset = Achievement.objects.all()
    serializer_class = AchievementSerializer
