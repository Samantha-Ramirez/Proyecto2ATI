from django.shortcuts import redirect
from django.shortcuts import render
from django.utils.translation import gettext_lazy as _
from django.contrib.auth import authenticate, login as auth_login
from django.contrib.auth import logout as auth_logout
from .models import JobOffer


# Sección de perfil y autenticación
def login(request):
    if request.method == 'POST':
        u = request.POST.get('username')
        p = request.POST.get('password')

        user = authenticate(request, username=u, password=p)

        if user is not None:
            auth_login(request, user)
            return redirect('feed')

    return render(request, 'login.html')


def logout(request):
    auth_logout(request)
    return redirect('login')


def register(request):
    return render(request, 'register.html')


def profile(request):
    # En el futuro, aquí buscaremos al usuario real: user = request.user
    context = {
        'page_title': _('Perfil'),
        'show_bottom_nav': True,
        'desktop_search': True,
        'show_search_menu': True,
        'show_menu': True,

        # Datos de prueba para los posts
        'message_rows': [
            {
                'name': 'First Guy',
                'time': '17 h',
                'message': 'Java Technical Lead',
                'bold': True
            },
        ],
    }

    return render(request, 'profile.html', context)


def manage_profile(request):
    return render(request, 'manage_profile.html', {
        'page_title': _('Ajustes'),
        'show_search_menu': True,
        'desktop_search': True,
        'show_bottom_nav': True,
    })


# Sección laboral
def search_jobs(request):
    jobs = JobOffer.objects.all().order_by('-created_at')
    context = {
        'page_title': _('Zona laboral'),
        'show_bottom_nav': True,
        'desktop_search': True,
        'show_search_menu': True,
        'jobs': jobs,
    }
    return render(request, 'search_jobs.html', context)


def apply_job(request, job_id):
    pass


def post_job(request):
    if request.method == 'POST':
        title = request.POST.get('title')
        content = request.POST.get('content')
        position = request.POST.get('position')
        industry = request.POST.get('industry')
        salary = request.POST.get('salary')
        working_hours = request.POST.get('working_hours')
        job_description = request.POST.get('job_description')
        requirements = request.POST.get('requirements')
        offer_status = request.POST.get('offer_status', 'open')
        image = request.FILES.get('image')

        if salary == '':
            salary = None

        JobOffer.objects.create(
            author=request.user,
            title=title,
            content=content,
            image=image,
            position=position,
            industry=industry,
            salary=salary,
            working_hours=working_hours,
            job_description=job_description,
            requirements=requirements,
            offer_status=offer_status,
        )

        return redirect('feed')

    return render(request, 'post_job.html')


def search_staff(request):
    profesionales = [
        {'id': 1, 'nombre': 'Luis Colina', 'rol': 'Frontend Developer', 'skills': ['React', 'CSS', 'Figma']},
        {'id': 2, 'nombre': 'Juan Pérez', 'rol': 'Backend Developer', 'skills': ['Python', 'Django', 'Docker']},
        {'id': 3, 'nombre': 'Ana Gómez', 'rol': 'Data Scientist', 'skills': ['Python', 'SQL', 'Machine Learning']},
    ]

    return render(request, 'search_staff.html', {
        'page_title': _('Buscar Talento'),
        'profesionales': profesionales,
    })


def professional_detail(request, pk):
    return render(request, 'professional_profile.html', {
        'page_title': _('Perfil del Candidato'),
        'candidato_id': pk,
    })


def manage_staff(request):
    return render(request, 'manage_staff.html', {
        'page_title': _('Gestionar Profesionales'),
    })


# Sección de muro y mensajería
def feed(request):
    context = {
        'desktop_search': True,
        'page_title': '',
        'show_bottom_nav': True,
    }
    return render(request, 'feed.html', context)


def follow_user(request, user_id):
    pass


def comment_post(request, post_id):
    context = {
        'desktop_search': True,
        'page_title': '',
    }
    return render(request, 'post.html', context)


def messages(request):
    message_rows = [
        {'name': 'Samantha Ramirez', 'message': _('Por supuesto'), 'time': '10:07 AM', 'bold': True},
        {'name': 'Gustavo Berne', 'message': _('Tu: OK'), 'time': _('Lun'), 'bold': False},
        {'name': 'Jose Campos', 'message': _('Tu: Creo que deberia cambiarse'), 'time': _('Vie'), 'bold': False},
        {'name': 'Luisdavid Colina', 'message': _('Tu: Luego lo revisare'), 'time': _('Mie'), 'bold': False},
        {'name': 'Gabriel Padilla', 'message': _('Hola, tengo una sugerencia'), 'time': _('Mar'), 'bold': False},
        {'name': 'First Guy', 'message': _('LinkedOut es lo maximo'), 'time': _('Dom'), 'bold': False},
        {'name': 'Second Guy', 'message': _('Tu: OK'), 'time': _('Dom'), 'bold': False},
        {'name': 'Third Guy', 'message': '👍', 'time': _('Oct 9'), 'bold': False},
    ]
    return render(request, 'messages.html', {
        'message_rows': message_rows,
        'page_title': _('Mensajes'),
        'show_bottom_nav': True,
    })


def notifications_view(request):
    return render(request, 'notifications.html', {
        'page_title': _('Notificaciones'),
        'show_bottom_nav': True,
    })


def chat(request, user_id):
    return redirect('messages')


# Sección de administración
def admin_panel(request):
    return render(request, 'admin_panel.html')


def manage_users(request):
    return render(request, 'manage_users.html')


def manage_content(request):
    return render(request, 'manage_content.html')
