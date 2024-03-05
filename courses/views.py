from django.http import Http404
from rest_framework import viewsets
from rest_framework.permissions import IsAuthenticated
from rest_framework.response import Response
from rest_framework.views import APIView
from courses.models import Course, CourseSubscription
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


class SubscriptionAPIView(APIView):
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

        subs_item = CourseSubscription.objects.filter(user=user, course=course)

        if subs_item.exists():
            subs_item.delete()
            message = 'Подписка на курс удалена'
        else:
            CourseSubscription.objects.create(user=user, course=course)
            message = 'Подписка на курс добавлена'

        return Response({"message": message, "user": user_data})

# class CourseSubscriptionAPIView(APIView):
#     """Creating a subscription to course updates"""
#     permission_classes = [IsAuthenticated, IsOwner]
#     def get(self, request):
#         user = request.user
#         if user.is_authenticated:
#             # Getting all subscriptions for the current user
#             subscriptions = CourseSubscription.objects.filter(user=user)
#             subscription_serializer = CourseSubscriptionSerializer(subscriptions, many=True)
#             # Getting all courses
#             courses = Course.objects.all()
#             course_serializer = CourseSerializer(courses, many=True, context={'request': request})
#             # Returning JSON with data about courses and subscriptions
#             return Response({"courses": course_serializer.data, "subscriptions": subscription_serializer.data},
#                             status=status.HTTP_200_OK)
#         else:
#             # Return an error message if the user is not authenticated
#             return Response({"message": "Authentication required"}, status=status.HTTP_401_UNAUTHORIZED)
#     def post(self, request, course_id):
#         user = request.user
#         if user.is_authenticated:
#             # Getting the course object from the database using get_object_or_404
#             course = get_object_or_404(Course, id=course_id)
#             # Retrieving subscription objects by current user and course
#             subscription, created = CourseSubscription.objects.get_or_create(user=user, course=course)
#             if created:
#                 message = 'Subscription has been created successfully.'
#             else:
#                 subscription.delete()
#                 message = 'Subscription has been deleted successfully.'
#             serializer = CourseSubscriptionSerializer(subscription)
#             return Response({"message": message, "subscription": serializer.data}, status=status.HTTP_200_OK)
#         else:
#             # Return an error message if the user is not authenticated
#             return Response({"message": "Authentication required"}, status=status.HTTP_401_UNAUTHORIZED)