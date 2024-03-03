from django.http import Http404
from rest_framework import viewsets
from rest_framework.permissions import IsAuthenticated
from rest_framework.response import Response
from rest_framework.views import APIView
from courses.models import Course, Subscriptions
from courses.paginators import CoursePaginator
from courses.serilzers import CourseSerializer
from lessons.permissions import IsSuperuser, IsOwnerOrStaff, IsModerator
from users.serilzers import UserSerializer


class CourseViewSet(viewsets.ModelViewSet):
    queryset = Course.objects.all()
    serializer_class = CourseSerializer
    pagination_class = CoursePaginator

    def get_permissions(self):
        # Возвращает соответствующие разрешения в зависимости от действия.
        if self.action == 'create':
            self.permission_classes = [IsAuthenticated, IsSuperuser | IsModerator]
        elif self.action == 'destroy':
            self.permission_classes = [IsAuthenticated, IsSuperuser]
        elif self.action == 'update':
            self.permission_classes = [IsAuthenticated, IsSuperuser]
        elif self.action == 'retrieve':
            self.permission_classes = [IsAuthenticated, IsSuperuser | IsOwnerOrStaff | IsModerator]
        else:
            self.action = [IsAuthenticated]
        return [permission() for permission in self.permission_classes]

    # def retrieve(self, request, pk=None):
    #
    #     queryset = Course.objects.all()
    #     user = get_object_or_404(queryset, pk=pk)
    #     serializer = CourseDetailSerializer(user)
    #     return Response(serializer.data)


class CourseSubscriptionAPIView(APIView):
    queryset = Course.objects.all()
    serializer_class = CourseSerializer
    permission_classes = [IsAuthenticated]

    def post(self, request, *args, **kwargs):
        user = self.request.user
        user_data = UserSerializer(user).data

        course_id = request.data.get('course_id')

        if course_id is None:
            return Response({"message": "Отсутствует идентификатор курса в запросе"}, status=400)

        try:
            course = Course.objects.get(id=course_id)
        except Course.DoesNotExist:
            raise Http404("Курс с таким идентификатором не найден")

        subs_item = Subscriptions.objects.filter(user=user, course=course)

        if subs_item.exists():
            subs_item.delete()
            message = 'Подписка на курс удалена'
        else:
            Subscriptions.objects.create(user=user, course=course)
            message = 'Подписка на курс добавлена'

        return Response({"message": message, "user": user_data})
