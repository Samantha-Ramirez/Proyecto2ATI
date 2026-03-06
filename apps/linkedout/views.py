from django.contrib.auth import authenticate, login as auth_login
from django.contrib.auth import logout as auth_logout
from django.contrib.auth.decorators import login_required
from django.contrib import messages as msg
from django.shortcuts import get_object_or_404, redirect, render
from django.utils.translation import gettext_lazy as _
from django.db.models import Q

from .models import JobApplication, JobOffer, Post, Profile


# Sección de perfil y autenticación
def login(request):
    if request.method == 'POST':
        u = request.POST.get('username')
        p = request.POST.get('password')

        user = authenticate(request, username=u, password=p)

        if user is not None:
            auth_login(request, user)
            return redirect('feed')

        msg.warning(request, _("Usuario o contraseña incorrectos."))

    context = {
        'page_title': _('Iniciar sesión'),
    }

    return render(request, 'login.html', context)


def logout(request):
    auth_logout(request)
    return redirect('login')


def register(request):
    context = {
        'page_title': _('Registrarse'),
    }
    return render(request, 'register.html', context)


def profile(request):
    context = {
        'page_title': _('Perfil'),
        'show_bottom_nav': True,
        'desktop_search': True,
        'show_search_menu': True,
        'show_menu': True,

        'profile_post': {
            'author': None,
            'joboffer': None,
            'title': None,
            'content': None,
            'image': None,
            'created_at': None,
        },
    }

    return render(request, 'profile.html', context)


def manage_profile(request):
    context = {
        'page_title': _('Gestionar perfil'),
        'show_search_menu': True,
        'desktop_search': True,
        'show_bottom_nav': True,
    }

    return render(request, 'manage_profile.html', context)


# Sección laboral
def search_jobs(request):
    query = request.GET.get('q', '').strip()
    jobs = JobOffer.objects.all().order_by('-created_at')

    if query:
        jobs = jobs.filter(
            Q(title__icontains=query) |
            Q(position__icontains=query) |
            Q(industry__icontains=query) |
            Q(job_description__icontains=query) |
            Q(requirements__icontains=query)
        )

    applied_job_ids = set()
    if request.user.is_authenticated:
        applied_job_ids = set(
            JobApplication.objects.filter(applicant=request.user).values_list('job_offer_id', flat=True)
        )

    context = {
        'page_title': _('Zona laboral'),
        'show_bottom_nav': True,
        'desktop_search': True,
        'show_search_menu': True,
        'jobs': jobs,
        'applied_job_ids': applied_job_ids,
        'search_query': query,
        'search_placeholder': _('Buscar oferta laboral'),
    }

    return render(request, 'search_jobs.html', context)


def apply_job(request, job_id):
    job = get_object_or_404(JobOffer, pk=job_id)

    if request.method != "POST":
        return redirect('search_jobs')

    application, created = JobApplication.objects.get_or_create(
        job_offer=job,
        applicant=request.user,
    )

    if created:
        msg.success(request, _("Te postulaste correctamente."))
    else:
        msg.info(request, _("Ya estabas postulado."))

    return redirect('search_jobs')


def post(request):
    if request.method == "POST":
        content = request.POST.get("content", "").strip()
        title = (request.POST.get("title") or "").strip()
        image = request.FILES.get("image")

        if not content and not image:
            msg.warning(request, _("Escribe un texto o adjunta una imagen."))
            return redirect("post")

        Post.objects.create(
            author=request.user,
            title=title,
            content=content or _("(Sin texto)"),
            image=image,
        )

        msg.success(request, _("Publicación creada correctamente."))
        return redirect("feed")

    context = {
        "page_title": _("Hacer publicación"),
        "show_bottom_nav": True,
        "desktop_search": True,
        "show_search_menu": True,
        "show_menu": True,
    }

    return render(request, "post.html", context)


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

        msg.success(request, _("Oferta laboral publicada correctamente."))
        return redirect('feed')

    context = {
        'page_title': _('Publicar oferta laboral'),
    }

    return render(request, 'post_job.html', context)


def search_professionals(request):
    summary = request.GET.get('summary', '')
    education = request.GET.get('education', '')
    experience = request.GET.get('experience', '')

    professionals = Profile.objects.filter(user_type=Profile.PROFESSIONAL)

    if 'search_btn' in request.GET:
        if not any([summary, education, experience]):
            msg.warning(request, _('Introduce al menos un criterio de búsqueda.'))
        else:
            if summary:
                professionals = professionals.filter(professional_summary__icontains=summary)
            if education:
                professionals = professionals.filter(education__icontains=education)
            if experience:
                professionals = professionals.filter(experience__icontains=experience)

    context = {
        'page_title': _('Zona laboral'),
        'professionals': professionals,
        'show_bottom_nav': True,
    }

    return render(request, 'search_professionals.html', context)


def professional_profile(request, pk):
    context = {
        'page_title': _('Perfil del profesional'),
        'candidato_id': pk,
    }

    return render(request, 'professional_profile.html', context)


def manage_professionals(request):
    context = {
        'page_title': _('Gestionar profesionales'),
    }

    return render(request, 'manage_professionals.html', context)


# Sección de muro y mensajería
def feed(request):
    posts = Post.objects.select_related("author", "joboffer").all().order_by("-created_at")

    applied_job_ids = set()
    if request.user.is_authenticated:
        applied_job_ids = set(
            JobApplication.objects.filter(applicant=request.user).values_list('job_offer_id', flat=True)
        )

    context = {
        'desktop_search': True,
        'page_title': _('Inicio'),
        'show_bottom_nav': True,
        'posts': posts,
        'applied_job_ids': applied_job_ids,
    }

    return render(request, 'feed.html', context)


def follow_user(request, user_id):
    pass


def comment_post(request, post_id):
    context = {
        'desktop_search': True,
        'page_title': '',
    }
    return render(request, 'comment_post.html', context)


def messages(request):
    message_rows = [
        {'name': 'Samantha Ramirez', 'message': _('Por supuesto'),
         'time': '10:07 AM', 'bold': True},
        {'name': 'Gustavo Berne', 'message': _('Tu: OK'),
         'time': _('Lun'), 'bold': False},
        {'name': 'Jose Campos', 'message': _('Tu: Creo que deberia cambiarse'),
         'time': _('Vie'), 'bold': False},
        {'name': 'Luisdavid Colina', 'message': _('Tu: Luego lo revisare'),
         'time': _('Mie'), 'bold': False},
        {'name': 'Gabriel Padilla', 'message': _('Hola, tengo una sugerencia'),
         'time': _('Mar'), 'bold': False},
        {'name': 'First Guy', 'message': _('LinkedOut es lo maximo'),
         'time': _('Dom'), 'bold': False},
        {'name': 'Second Guy', 'message': _('Tu: OK'),
         'time': _('Dom'), 'bold': False},
        {'name': 'Third Guy', 'message': '👍',
         'time': _('Oct 9'), 'bold': False},
    ]

    context = {
        'message_rows': message_rows,
        'page_title': _('Mensajes'),
        'show_bottom_nav': True,
    }

    return render(request, 'messages.html', context)


def notifications(request):
    context = {
        'page_title': _('Notificaciones'),
        'show_bottom_nav': True,
    }

    return render(request, 'notifications.html', context)


def chat(request, user_id):
    return redirect('messages')


# Sección de administración
def admin_panel(request):
    return render(request, 'admin_panel.html')


def manage_users(request):
    return render(request, 'manage_users.html')


def manage_content(request):
    return render(request, 'manage_content.html')
