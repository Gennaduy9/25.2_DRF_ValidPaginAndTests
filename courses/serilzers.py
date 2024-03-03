from rest_framework import serializers
from rest_framework.fields import SerializerMethodField

from courses.models import Course, Subscriptions
from lessons.models import Lesson


class CourseSerializer(serializers.ModelSerializer):
    # Cоздание поля для подсчёта уроков
    lesson_count = SerializerMethodField()

    def get_lesson_count(self, obj):
        return Lesson.objects.filter(course=obj.pk).count()

    def get_is_subscribed(self, obj):
        # Получаем текущего пользователя из запроса
        user = self.context['request'].user

        # Проверка подписки пользователя на этот курс
        if user.is_authenticated:
            return Subscriptions.objects.filter(user=user, course=obj.pk).exists()
        else:
            return False

    class Meta:
        model = Course
        fields = ["name", "preview_image", "description", "lesson_count", "user"]


class SubscriptionSerializer(serializers.ModelSerializer):
    class Meta:
        model = Subscriptions
        fields = ["course", "user"]





# class DetailSerializer(serializers.ModelSerializer):
#     is_subscribed = serializers.SerializerMethodField()
#
#     def get_is_subscribed(self, obj):
#         # Получаем текущего пользователя из запроса
#         user = self.context['request'].user
#
#         # Проверка подписки пользователя на этот курс
#         if user.is_authenticated:
#             return Subscriptions.objects.filter(user=user, course=obj.pk).exists()
#         else:
#             return False
#
#     class Meta:
#         model = Course
#         fields = ["name", "preview_image", "description", "lesson_count", "user"]


# class CourseDetailSerializer(serializers.ModelSerializer):
#     """
#     Serializer для модели Course с подробной информацией.
#     Включает SerializerMethodField для расчета количества уроков в курсе.
#     """
#     lesson_count = SerializerMethodField()
#     lessons = LessonSerializer(source='lesson_set', many=True, read_only=True)
#
#     def get_lesson_count(self, obj):
#         """
#         Метод расчета количества уроков, связанных с курсом.
#         """
#         return Lesson.objects.filter(course=obj.pk).count()
#
#     class Meta:
#         model = Course
#         fields = ["name", "preview_image", "description", "lesson_count", "user"]


# class SubscriptionSerializer(serializers.ModelSerializer):
#     lessons = LessonSerializer(source='lesson_set', many=True, read_only=True)
#     is_subscribe = SerializerMethodField()
#
#     def get_is_subscribe(self, obj):
#         # Получаем текущего пользователя из запроса
#         user = self.context['request'].user
#
#         for sub in Subscriptions.objects.filter(user=user, course=obj.pk):
#             for user in obj.user.all():
#                 if sub.user == user:
#                     return True
#         return False
#
#     class Meta:
#         model = Subscriptions
#         fields = ["course", "user"]
