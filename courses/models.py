from django.db import models

from config import settings

NULLABLE = {'blank': True, 'null': True}


class Course(models.Model):
    name = models.CharField(max_length=100, verbose_name='Название')
    preview_image = models.ImageField(upload_to='course_previews/', verbose_name='Изображение', **NULLABLE)
    description = models.TextField(**NULLABLE, verbose_name='Описание')
    owner = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.SET_NULL, verbose_name='Владелец',
                              **NULLABLE)
    def __str__(self):
        return self.name

    class Meta:
        verbose_name = 'Курс'
        verbose_name_plural = 'Курсы'


class CourseSubscription(models.Model):
    course = models.ForeignKey(Course, on_delete=models.CASCADE, verbose_name='Курс')
    user = models.ForeignKey('users.User', on_delete=models.CASCADE, verbose_name='Пользователь')

    def __str__(self):
        return f"{self.user} {self.course}"

    class Meta:
        verbose_name = 'Подписка'
        verbose_name_plural = 'Подписки'
