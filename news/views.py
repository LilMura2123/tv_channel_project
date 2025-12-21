from django.shortcuts import render, redirect, get_object_or_404
from django.contrib.auth import login, authenticate
from django.contrib.auth.decorators import login_required, user_passes_test
from django.contrib import messages
from django.db.models import Q, Count
from django.core.paginator import Paginator
from django.utils import timezone
from django import forms
from .models import News, Program, CustomUser
from .forms import NewsForm, ProgramForm, UserRegistrationForm
from datetime import datetime, timedelta


def is_admin(user):
    """Check if user is admin"""
    return user.is_authenticated and (user.is_admin() or user.is_superuser)


def is_editor(user):
    """Check if user is editor or admin"""
    return user.is_authenticated and (user.is_editor() or user.is_admin())


def home(request):
    """Home page with latest news and upcoming programs"""
    latest_news = News.objects.all()[:5]
    upcoming_programs = Program.objects.filter(
        start_time__gte=timezone.now()
    ).order_by('start_time')[:5]
    
    context = {
        'latest_news': latest_news,
        'upcoming_programs': upcoming_programs,
    }
    return render(request, 'news/home.html', context)


def news_list(request):
    """List all news with search and filtering"""
    news_list = News.objects.all()
    
    # Search functionality
    search_query = request.GET.get('search', '')
    if search_query:
        news_list = news_list.filter(
            Q(title__icontains=search_query) |
            Q(content__icontains=search_query)
        )
    
    # Date filtering
    date_filter = request.GET.get('date', '')
    if date_filter:
        try:
            filter_date = datetime.strptime(date_filter, '%Y-%m-%d').date()
            news_list = news_list.filter(created_at__date=filter_date)
        except ValueError:
            messages.error(request, 'Неверный формат даты. Используйте ГГГГ-ММ-ДД.')
    
    # Sorting
    sort_by = request.GET.get('sort', '-created_at')
    if sort_by in ['title', '-title', 'created_at', '-created_at']:
        news_list = news_list.order_by(sort_by)
    
    # Pagination
    paginator = Paginator(news_list, 10)
    page_number = request.GET.get('page')
    news = paginator.get_page(page_number)
    
    context = {
        'news': news,
        'search_query': search_query,
        'date_filter': date_filter,
        'sort_by': sort_by,
    }
    return render(request, 'news/news_list.html', context)


def news_detail(request, pk):
    """View individual news article"""
    news = get_object_or_404(News, pk=pk)
    return render(request, 'news/news_detail.html', {'news': news})


@login_required
@user_passes_test(is_editor)
def news_create(request):
    """Create new news article"""
    if request.method == 'POST':
        form = NewsForm(request.POST)
        if form.is_valid():
            form.save()
            messages.success(request, 'Новость успешно создана!')
            return redirect('news_list')
    else:
        form = NewsForm()
    return render(request, 'news/news_form.html', {'form': form, 'action': 'Создать'})


@login_required
@user_passes_test(is_editor)
def news_update(request, pk):
    """Update existing news article"""
    news = get_object_or_404(News, pk=pk)
    if request.method == 'POST':
        form = NewsForm(request.POST, instance=news)
        if form.is_valid():
            form.save()
            messages.success(request, 'Новость успешно обновлена!')
            return redirect('news_detail', pk=news.pk)
    else:
        form = NewsForm(instance=news)
    return render(request, 'news/news_form.html', {'form': form, 'action': 'Обновить', 'news': news})


@login_required
@user_passes_test(is_editor)
def news_delete(request, pk):
    """Delete news article"""
    news = get_object_or_404(News, pk=pk)
    if request.method == 'POST':
        news.delete()
        messages.success(request, 'Новость успешно удалена!')
        return redirect('news_list')
    return render(request, 'news/news_confirm_delete.html', {'news': news})


def program_list(request):
    """List all programs with search and filtering"""
    program_list = Program.objects.all()
    
    # Search functionality
    search_query = request.GET.get('search', '')
    if search_query:
        program_list = program_list.filter(
            Q(title__icontains=search_query) |
            Q(description__icontains=search_query)
        )
    
    # Date filtering
    date_filter = request.GET.get('date', '')
    if date_filter:
        try:
            filter_date = datetime.strptime(date_filter, '%Y-%m-%d').date()
            program_list = program_list.filter(start_time__date=filter_date)
        except ValueError:
            messages.error(request, 'Неверный формат даты. Используйте ГГГГ-ММ-ДД.')
    
    # Program name filtering
    program_name = request.GET.get('program_name', '')
    if program_name:
        program_list = program_list.filter(title__icontains=program_name)
    
    # Sorting
    sort_by = request.GET.get('sort', 'start_time')
    if sort_by in ['title', '-title', 'start_time', '-start_time']:
        program_list = program_list.order_by(sort_by)
    
    # Pagination
    paginator = Paginator(program_list, 10)
    page_number = request.GET.get('page')
    programs = paginator.get_page(page_number)
    
    context = {
        'programs': programs,
        'search_query': search_query,
        'date_filter': date_filter,
        'program_name': program_name,
        'sort_by': sort_by,
    }
    return render(request, 'news/program_list.html', context)


def program_detail(request, pk):
    """View individual program"""
    program = get_object_or_404(Program, pk=pk)
    return render(request, 'news/program_detail.html', {'program': program})


@login_required
@user_passes_test(is_editor)
def program_create(request):
    """Create new program"""
    if request.method == 'POST':
        form = ProgramForm(request.POST)
        if form.is_valid():
            form.save()
            messages.success(request, 'Программа успешно создана!')
            return redirect('program_list')
    else:
        form = ProgramForm()
    return render(request, 'news/program_form.html', {'form': form, 'action': 'Создать'})


@login_required
@user_passes_test(is_editor)
def program_update(request, pk):
    """Update existing program"""
    program = get_object_or_404(Program, pk=pk)
    if request.method == 'POST':
        form = ProgramForm(request.POST, instance=program)
        if form.is_valid():
            form.save()
            messages.success(request, 'Программа успешно обновлена!')
            return redirect('program_detail', pk=program.pk)
    else:
        form = ProgramForm(instance=program)
    return render(request, 'news/program_form.html', {'form': form, 'action': 'Обновить', 'program': program})


@login_required
@user_passes_test(is_editor)
def program_delete(request, pk):
    """Delete program"""
    program = get_object_or_404(Program, pk=pk)
    if request.method == 'POST':
        program.delete()
        messages.success(request, 'Программа успешно удалена!')
        return redirect('program_list')
    return render(request, 'news/program_confirm_delete.html', {'program': program})


def register(request):
    """User registration with password confirmation"""
    if request.method == 'POST':
        form = UserRegistrationForm(request.POST)
        if form.is_valid():
            user = form.save(commit=False)
            # Only allow admins to create admin/editor accounts
            if not request.user.is_authenticated or not request.user.is_admin():
                if user.role in ['admin', 'editor']:
                    user.role = 'user'  # Force regular user role
            user.save()
            username = form.cleaned_data.get('username')
            messages.success(request, f'Аккаунт для {username} создан! Теперь вы можете войти.')
            return redirect('login')
    else:
        form = UserRegistrationForm()
        # Hide role field for non-admin users
        if not request.user.is_authenticated or not request.user.is_admin():
            form.fields['role'].widget = forms.HiddenInput()
            form.fields['role'].initial = 'user'
    return render(request, 'news/register.html', {'form': form})


def login_view(request):
    """User login"""
    if request.method == 'POST':
        username = request.POST.get('username')
        password = request.POST.get('password')
        user = authenticate(request, username=username, password=password)
        if user is not None:
            login(request, user)
            messages.success(request, f'Добро пожаловать, {username}!')
            return redirect('home')
        else:
            messages.error(request, 'Неверное имя пользователя или пароль.')
    return render(request, 'news/login.html')


@login_required
def logout_view(request):
    """User logout"""
    from django.contrib.auth import logout
    logout(request)
    messages.success(request, 'Вы успешно вышли из системы.')
    return redirect('login')


@login_required
def statistics(request):
    """Statistics page with charts and graphs"""
    from django.db.models.functions import TruncMonth
    
    total_users = CustomUser.objects.count()
    total_news = News.objects.count()
    total_programs = Program.objects.count()
    
    # News by month
    news_by_month = News.objects.annotate(
        month=TruncMonth('created_at')
    ).values('month').annotate(count=Count('id')).order_by('month')
    
    # Programs by month
    programs_by_month = Program.objects.annotate(
        month=TruncMonth('created_at')
    ).values('month').annotate(count=Count('id')).order_by('month')
    
    # Users by role
    users_by_role = CustomUser.objects.values('role').annotate(count=Count('id'))
    
    # Format dates for charts
    news_data = [{'month': str(item['month'])[:7], 'count': item['count']} for item in news_by_month]
    programs_data = [{'month': str(item['month'])[:7], 'count': item['count']} for item in programs_by_month]
    
    context = {
        'total_users': total_users,
        'total_news': total_news,
        'total_programs': total_programs,
        'news_by_month': news_data,
        'programs_by_month': programs_data,
        'users_by_role': list(users_by_role),
    }
    return render(request, 'news/statistics.html', context)


def about(request):
    """About the Author page"""
    context = {
        'developer_name': 'Хутраев Хаджимурад Мубаризович',
        'developer_contact': '89993359305',
        'project_start_date': '01.11.2025',
        'project_end_date': '15.12.2025',
        'technologies': [
            'Python 3.8+',
            'Django 5.2.8',
            'PostgreSQL 12+',
            'HTML5/CSS3',
            'JavaScript (Chart.js)',
            'Bootstrap 5',
        ],
        'project_timeline': [
            {'date': '2024-01-15', 'event': 'Инициализация проекта и настройка базы данных'},
            {'date': '2024-01-20', 'event': 'Реализация аутентификации пользователей и управления доступом на основе ролей'},
            {'date': '2024-01-25', 'event': 'Операции CRUD для новостей и программ'},
            {'date': '2024-02-01', 'event': 'Функциональность поиска и фильтрации'},
            {'date': '2024-02-05', 'event': 'Админ-панель и страница статистики'},
            {'date': '2024-02-10', 'event': 'Дизайн UI/UX в стиле газеты'},
        ]
    }
    return render(request, 'news/about.html', context)


@login_required
@user_passes_test(is_admin)
def user_management(request):
    """User management page for admins"""
    users = CustomUser.objects.all()
    
    # Search functionality
    search_query = request.GET.get('search', '')
    if search_query:
        users = users.filter(
            Q(username__icontains=search_query) |
            Q(email__icontains=search_query)
        )
    
    # Role filtering
    role_filter = request.GET.get('role', '')
    if role_filter:
        users = users.filter(role=role_filter)
    
    # Pagination
    paginator = Paginator(users, 10)
    page_number = request.GET.get('page')
    users_page = paginator.get_page(page_number)
    
    context = {
        'users': users_page,
        'search_query': search_query,
        'role_filter': role_filter,
    }
    return render(request, 'news/user_management.html', context)
