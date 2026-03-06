from django.contrib.auth import authenticate, login as auth_login
from django.contrib.auth import logout as auth_logout
from django.contrib.auth.decorators import login_required
from django.shortcuts import get_object_or_404, redirect, render
from django.utils.translation import gettext_lazy as _
from django.db.models import Q  # Para búsquedas más complicadas

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
    # Tomamos el termino de búsqueda
    query = request.GET.get('q', '').strip()

    # Nos traemos todas las ofertas base ordenadas por fecha
    jobs = JobOffer.objects.all().order_by('-created_at')

    # Filtramos por lo que puso el usuario
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
        'search_query': query,  # Pasamos el término de vuelta al template
        # Agregamos placeholder variable
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

    return redirect('search_jobs')


def create_post(request):
    if request.method == "POST":
        content = request.POST.get("content", "").strip()
        title = (request.POST.get("title") or "").strip()
        image = request.FILES.get("image")

        if not content and not image:
            # messages.error(request, _("Debes escribir un texto o adjuntar una imagen."))
            return redirect("create_post")

        Post.objects.create(
            author=request.user,
            title=title,
            content=content or _("(Sin texto)"),
            image=image,
        )

        # messages.success(request, _("Publicación creada correctamente."))
        return redirect("feed")

    # GET
    return render(request, "create_post.html", {
        "page_title": _("Crear publicación"),
        "show_bottom_nav": True,
        "desktop_search": True,
        "show_search_menu": True,
        "show_menu": True,
    })


def post_job(request):
    if request.method == 'POST':

        # 1. Extraemos todos los textos del formulario
        # usando el atributo 'name' del HTML
        title = request.POST.get('title')
        content = request.POST.get('content')
        position = request.POST.get('position')
        industry = request.POST.get('industry')
        salary = request.POST.get('salary')
        working_hours = request.POST.get('working_hours')
        job_description = request.POST.get('job_description')
        requirements = request.POST.get('requirements')

        # Extraemos los campos ocultos (hidden)
        opportunity_type = request.POST.get('opportunity_type', 'job_offer')
        offer_status = request.POST.get('offer_status', 'open')
        image = request.FILES.get('image')

        # Pequeña validación de seguridad:
        # Si el campo salario llega vacío, lo volvemos None
        # para que la base de datos (que espera un Decimal) no lance un error.
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

        # 3. Exito, redirigimos al usuario al feed
        # para que vea su nueva publicación
        return redirect('feed')

    return render(request, 'post_job.html')


def search_staff(request):
    # Obtenemos los parámetros de búsqueda desde el método GET
    q_summary = request.GET.get('summary', '')
    q_education = request.GET.get('education', '')
    q_experience = request.GET.get('experience', '')

    # Iniciamos consultando solo a los usuarios de tipo 'Profesional'
    profesionales = Profile.objects.filter(user_type=Profile.PROFESSIONAL)

    # Flujo A1: Validar si se enviaron filtros (si el botón 'Filtrar' fue presionado)
    if 'search_btn' in request.GET:
        if not any([q_summary, q_education, q_experience]):
            # Solicitamos al menos un criterio (RNF-02: internacionalización)
            messages.warning(request, _('Por favor, introduzca al menos un criterio de búsqueda.'))
        else:
            # Aplicamos filtros acumulativos (icontains para ignorar mayúsculas/minúsculas)
            if q_summary:
                profesionales = profesionales.filter(professional_summary__icontains=q_summary)
            if q_education:
                profesionales = profesionales.filter(education__icontains=q_education)
            if q_experience:
                profesionales = profesionales.filter(experience__icontains=q_experience)

    return render(request, 'search_staff.html', {
        'page_title': _('Buscar Personal'),
        'profesionales': profesionales,
        'show_bottom_nav': True,
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
    posts = Post.objects.select_related("author", "joboffer").all().order_by("-created_at")

    applied_job_ids = set()
    if request.user.is_authenticated:
        applied_job_ids = set(
            JobApplication.objects.filter(applicant=request.user).values_list('job_offer_id', flat=True)
        )

    context = {
        'desktop_search': True,
        'page_title': '',
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
    return render(request, 'post.html', context)


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
