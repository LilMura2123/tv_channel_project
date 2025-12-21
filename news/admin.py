from django.contrib import admin
from django.contrib.auth.admin import UserAdmin as BaseUserAdmin
from django.utils.html import format_html
from .models import News, Program, CustomUser


@admin.register(CustomUser)
class CustomUserAdmin(BaseUserAdmin):
    """Custom user admin with role management"""
    list_display = ['username', 'email', 'role', 'is_staff', 'date_joined']
    list_filter = ['role', 'is_staff', 'is_superuser', 'date_joined']
    fieldsets = BaseUserAdmin.fieldsets + (
        ('Роль', {'fields': ('role',)}),
    )
    add_fieldsets = BaseUserAdmin.add_fieldsets + (
        ('Роль', {'fields': ('role',)}),
    )
    
    def get_queryset(self, request):
        qs = super().get_queryset(request)
        # Admins can see all users, editors can't manage users
        if request.user.is_superuser or request.user.is_admin():
            return qs
        return qs.none()


@admin.register(News)
class NewsAdmin(admin.ModelAdmin):
    """News admin with role-based access"""
    list_display = ['title', 'created_at', 'updated_at', 'preview_content']
    list_filter = ['created_at', 'updated_at']
    search_fields = ['title', 'content']
    readonly_fields = ['created_at', 'updated_at']
    
    fieldsets = (
        ('Содержание', {
            'fields': ('title', 'content')
        }),
        ('Временные метки', {
            'fields': ('created_at', 'updated_at'),
            'classes': ('collapse',)
        }),
    )
    
    def preview_content(self, obj):
        """Show preview of content"""
        return format_html(
            '<span style="max-width: 200px; display: inline-block; overflow: hidden; text-overflow: ellipsis;">{}</span>',
            obj.content[:100] + '...' if len(obj.content) > 100 else obj.content
        )
    preview_content.short_description = 'Предпросмотр содержания'
    
    def has_add_permission(self, request):
        """Only editors and admins can add news"""
        return request.user.is_authenticated and (request.user.is_editor() or request.user.is_admin())
    
    def has_change_permission(self, request, obj=None):
        """Only editors and admins can change news"""
        return request.user.is_authenticated and (request.user.is_editor() or request.user.is_admin())
    
    def has_delete_permission(self, request, obj=None):
        """Only editors and admins can delete news"""
        return request.user.is_authenticated and (request.user.is_editor() or request.user.is_admin())


@admin.register(Program)
class ProgramAdmin(admin.ModelAdmin):
    """Program admin with role-based access"""
    list_display = ['title', 'start_time', 'end_time', 'duration', 'created_at']
    list_filter = ['start_time', 'created_at']
    search_fields = ['title', 'description']
    readonly_fields = ['created_at', 'updated_at']
    
    fieldsets = (
        ('Информация о программе', {
            'fields': ('title', 'description')
        }),
        ('Расписание', {
            'fields': ('start_time', 'end_time')
        }),
        ('Временные метки', {
            'fields': ('created_at', 'updated_at'),
            'classes': ('collapse',)
        }),
    )
    
    def duration(self, obj):
        """Calculate and display program duration"""
        if obj.start_time and obj.end_time:
            delta = obj.end_time - obj.start_time
            hours = delta.total_seconds() / 3600
            if hours < 1:
                minutes = delta.total_seconds() / 60
                return f"{int(minutes)} минут"
            return f"{hours:.1f} часов"
        return "Н/Д"
    duration.short_description = 'Длительность'
    
    def has_add_permission(self, request):
        """Only editors and admins can add programs"""
        return request.user.is_authenticated and (request.user.is_editor() or request.user.is_admin())
    
    def has_change_permission(self, request, obj=None):
        """Only editors and admins can change programs"""
        return request.user.is_authenticated and (request.user.is_editor() or request.user.is_admin())
    
    def has_delete_permission(self, request, obj=None):
        """Only editors and admins can delete programs"""
        return request.user.is_authenticated and (request.user.is_editor() or request.user.is_admin())
