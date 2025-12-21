from django.db import models
from django.contrib.auth.models import AbstractUser
from django.core.exceptions import ValidationError


class CustomUser(AbstractUser):
    """Custom user model with role-based access control"""
    ROLE_CHOICES = [
        ('admin', 'Администратор'),
        ('editor', 'Редактор'),
        ('user', 'Обычный пользователь'),
    ]
    
    role = models.CharField(max_length=10, choices=ROLE_CHOICES, default='user', verbose_name='Роль')
    
    class Meta:
        verbose_name = 'Пользователь'
        verbose_name_plural = 'Пользователи'
    
    def is_admin(self):
        return self.role == 'admin' or self.is_superuser
    
    def is_editor(self):
        return self.role == 'editor' or self.is_admin()
    
    def __str__(self):
        return f"{self.username} ({self.get_role_display()})"


class News(models.Model):
    """News model with title, content, and timestamps"""
    title = models.CharField(max_length=200, verbose_name='Заголовок')
    content = models.TextField(verbose_name='Содержание')
    created_at = models.DateTimeField(auto_now_add=True, verbose_name='Создано')
    updated_at = models.DateTimeField(auto_now=True, verbose_name='Обновлено')
    
    class Meta:
        ordering = ['-created_at']
        verbose_name = 'Новость'
        verbose_name_plural = 'Новости'
    
    def __str__(self):
        return self.title


class Program(models.Model):
    """Program model with title, description, and time slots"""
    title = models.CharField(max_length=200, verbose_name='Название')
    description = models.TextField(verbose_name='Описание')
    start_time = models.DateTimeField(verbose_name='Время начала')
    end_time = models.DateTimeField(verbose_name='Время окончания')
    created_at = models.DateTimeField(auto_now_add=True, verbose_name='Создано')
    updated_at = models.DateTimeField(auto_now=True, verbose_name='Обновлено')
    
    class Meta:
        ordering = ['start_time']
        verbose_name = 'Программа'
        verbose_name_plural = 'Программы'
    
    def clean(self):
        """Validate that end_time is after start_time"""
        if self.end_time and self.start_time:
            if self.end_time <= self.start_time:
                raise ValidationError('Время окончания должно быть позже времени начала.')
    
    def save(self, *args, **kwargs):
        self.full_clean()
        super().save(*args, **kwargs)
    
    @property
    def duration(self):
        """Calculate program duration in hours"""
        if self.end_time and self.start_time:
            delta = self.end_time - self.start_time
            hours = delta.total_seconds() / 3600
            if hours < 1:
                minutes = delta.total_seconds() / 60
                return f"{int(minutes)} минут"
            return f"{hours:.1f} часов"
        return "Н/Д"
    
    def __str__(self):
        return self.title
