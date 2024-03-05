from rest_framework import generics
from rest_framework.permissions import AllowAny, IsAuthenticated

from lessons.models import Lesson
from lessons.paginators import LessonPaginator
from lessons.permissions import IsSuperuser, IsModerator, IsOwnerOrStaff
from lessons.serilzers import LessonSerializer, LessonListSerializer


class LessonListView(generics.ListAPIView):
    queryset = Lesson.objects.all()
    serializer_class = LessonListSerializer
    pagination_class = LessonPaginator
    permission_classes = [IsAuthenticated]


class LessonCreateView(generics.CreateAPIView):
    queryset = Lesson.objects.all()
    serializer_class = LessonSerializer
    permission_classes = [IsOwnerOrStaff, IsSuperuser]


class LessonUpdateView(generics.UpdateAPIView):
    queryset = Lesson.objects.all()
    serializer_class = LessonSerializer
    permission_classes = [IsOwnerOrStaff]


class LessonRetrieveView(generics.RetrieveAPIView):
    queryset = Lesson.objects.all()
    serializer_class = LessonSerializer
    permission_classes = [IsOwnerOrStaff, IsModerator]


class LessonDestroyView(generics.DestroyAPIView):
    queryset = Lesson.objects.all()
    serializer_class = LessonSerializer
    permission_classes = [IsOwnerOrStaff, IsSuperuser]
