from django.contrib.auth.models import AbstractUser
from django.db import models


class UserRole(models.TextChoices):
    ADMIN = 'admin', 'Admin'
    LAB_MANAGER = 'lab_manager', 'Lab Manager'
    TEACHER = 'teacher', 'Teacher'


class User(AbstractUser):
    role = models.CharField(max_length=50, choices=UserRole.choices, default=UserRole.TEACHER)
    person = models.OneToOneField(
        'assignment.Person',
        on_delete=models.SET_NULL,
        null=True,
        blank=True,
        related_name='user',
    )

    class Meta:
        verbose_name = 'User'
        verbose_name_plural = 'Users'

    def __str__(self):
        return f'{self.username} ({self.role})'
