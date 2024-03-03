from django.urls import path
from rest_framework.routers import DefaultRouter

from courses.apps import CoursesConfig
from courses.views import CourseViewSet, CourseSubscriptionAPIView

app_name = CoursesConfig.name

router = DefaultRouter()

router.register(r'course', CourseViewSet, basename='course')

urlpatterns = [
    path('subscription/', CourseSubscriptionAPIView.as_view(), name='course-subscription'),
] + router.urls
