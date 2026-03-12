from django.test import TestCase
from django.urls import reverse
from django.db import IntegrityError, transaction
from django.contrib.auth.models import User
from .models import Profile
from .models import JobOffer, JobApplication


# Prueba unitaria para la vista perfil
class ProfileTemplateTests(TestCase):
    def setUp(self):
        # Configurar un usuario y perfil de prueba
        self.user = User.objects.create_user(
            username='testuser',
            password='testpassword123',
            first_name='First',
            last_name='Guy'
        )
        self.profile = Profile.objects.create(
            user=self.user,
            professional_summary='Java Technical Lead'
        )

    def test_profile_page_renders_correctly(self):
        # Prueba que la página de perfil carga, usa el template correcto
        # y contiene los elementos clave del HTML.

        # Iniciar sesión con el usuario de prueba
        self.client.login(username='testuser', password='testpassword123')

        # Hacer una petición GET a la vista del perfil
        response = self.client.get(reverse('profile'))

        # Verificar que la respuesta sea exitosa (HTTP 200)
        self.assertEqual(response.status_code, 200)

        # Verificar que se está usando el template
        self.assertTemplateUsed(response, 'profile.html')

        # Verificar que el HTML contiene IDs y textos específicos
        self.assertContains(response, 'id="banner-upload"')
        self.assertContains(response, 'id="avatar-upload"')
        self.assertContains(response, 'id="profile-edit-form"')
        self.assertContains(response, 'First Guy')


# Prueba unitaria para verificar que la restricción UNIQUE en JobApplication funciona correctamente
class JobApplicationUniqueConstraintTests(TestCase):
    def setUp(self):
        # Configurar un usuario empresa
        self.company = User.objects.create_user(
            username='company1',
            password='testpassword123',
            first_name='Company',
            last_name='Owner'
        )

        # Configurar un usuario postulante
        self.applicant = User.objects.create_user(
            username='applicant1',
            password='testpassword123',
            first_name='Applicant',
            last_name='User'
        )

        # Crear oferta laboral
        self.job_offer = JobOffer.objects.create(
            author=self.company,
            title='Python Developer',
            content='Post base content',
            job_description='Trabajo remoto, Django',
            salary='5000.00',
            position='Backend Developer',
            working_hours='40 horas semanales',
            requirements='Django, REST',
            industry='Software',
            offer_status='open',
        )

    def test_job_application_unique_together_prevents_duplicates(self):
        # Prueba que un mismo usuario NO puede postularse dos veces
        # a la misma oferta (unique_together: job_offer + applicant)

        JobApplication.objects.create(
            job_offer=self.job_offer,
            applicant=self.applicant,
            message='Me interesa la posición'
        )

        # Crear intento duplicado, que debe fallar por restricción UNIQUE
        with self.assertRaises(IntegrityError):
            with transaction.atomic():
                JobApplication.objects.create(
                    job_offer=self.job_offer,
                    applicant=self.applicant,
                    message='Intento duplicado'
                )

# Prueba unitaria para la creación de Ofertas Laborales (post_job)
class PostJobTests(TestCase):
    def setUp(self):
        # 1. Configurar un usuario de prueba que actuará como la empresa
        self.user = User.objects.create_user(
            username='company_tester',
            password='testpassword123',
            first_name='Tech',
            last_name='Company'
        )

    def test_post_job_get_renders_template(self):
        # Prueba que hacer una petición GET carga el HTML correcto
        self.client.login(username='company_tester', password='testpassword123')
        
        # Hacemos la petición a la vista
        response = self.client.get(reverse('post_job'))
        
        # Verificamos que cargue bien (200) y use el template correcto
        self.assertEqual(response.status_code, 200)
        self.assertTemplateUsed(response, 'post_job.html')

    def test_post_job_post_creates_offer(self):
        # Prueba que enviar el formulario por POST crea la oferta y redirige
        self.client.login(username='company_tester', password='testpassword123')
        
        # Diccionario simulando lo que el usuario escribe en el formulario HTML
        form_data = {
            'title': 'Desarrollador Backend Senior',
            'content': 'Únete a nuestro gran equipo de tecnología.',
            'position': 'Backend Engineer',
            'industry': 'it',
            'salary': '3500.50',
            'working_hours': '40 horas / Remoto',
            'job_description': 'Desarrollo y mantenimiento de APIs.',
            'requirements': 'Django, Python, PostgreSQL',
            'offer_status': 'open'
        }
        
        # Contamos cuántas ofertas hay antes del POST (debería ser 0)
        offers_count_before = JobOffer.objects.count()
        
        # Hacemos la petición POST enviando los datos
        response = self.client.post(reverse('post_job'), form_data)
        
        # 1. Verificamos que al terminar nos mande al muro (feed)
        self.assertRedirects(response, reverse('feed'))
        
        # 2. Verificamos que haya exactamente 1 oferta más en la base de datos
        self.assertEqual(JobOffer.objects.count(), offers_count_before + 1)
        
        # 3. Extraemos la oferta de la BD y verificamos que guardó bien al autor y los datos
        latest_offer = JobOffer.objects.latest('id')
        self.assertEqual(latest_offer.title, 'Desarrollador Backend Senior')
        self.assertEqual(latest_offer.author, self.user)
        self.assertEqual(float(latest_offer.salary), 3500.50) # Convertimos a float para comparar con el Decimal

    def test_post_job_empty_salary_is_saved_as_none(self):
        # Prueba la regla de validación: si el salario viene vacío, se guarda como NULL (None)
        self.client.login(username='company_tester', password='testpassword123')
        
        form_data = {
            'title': 'Diseñador UI/UX',
            'content': 'Buscamos talento creativo.',
            'position': 'UI Designer',
            'industry': 'it',
            'salary': '',  # <-- ¡Enviamos el salario vacío a propósito!
            'working_hours': 'Medio tiempo',
            'job_description': 'Diseño de interfaces.',
            'requirements': 'Figma, CSS',
            'offer_status': 'open'
        }
        
        self.client.post(reverse('post_job'), form_data)
        
        # Verificamos que la base de datos no explotó y guardó None
        latest_offer = JobOffer.objects.latest('id')
        self.assertIsNone(latest_offer.salary)


class SearchJobsTests(TestCase):
    def setUp(self):
        self.company = User.objects.create_user(
            username='company_search',
            password='testpassword123',
            first_name='Search',
            last_name='Company'
        )
        self.applicant = User.objects.create_user(
            username='applicant_search',
            password='testpassword123',
            first_name='Search',
            last_name='Applicant'
        )

        self.python_job = JobOffer.objects.create(
            author=self.company,
            title='Python Backend Developer',
            content='Buscamos developer backend.',
            job_description='Trabajo con Django y APIs REST.',
            salary='4000.00',
            position='Backend Engineer',
            working_hours='40 horas semanales',
            requirements='Python, Django, PostgreSQL',
            industry='Software',
            offer_status='open',
        )
        self.design_job = JobOffer.objects.create(
            author=self.company,
            title='UX Designer',
            content='Vacante para equipo de producto.',
            job_description='Diseno de interfaces y prototipos.',
            salary='3000.00',
            position='Product Designer',
            working_hours='40 horas semanales',
            requirements='Figma, research, prototipado',
            industry='Diseno',
            offer_status='open',
        )

    def login_applicant(self):
        self.client.login(username='applicant_search', password='testpassword123')

    def test_search_jobs_get_renders_template_with_all_jobs(self):
        self.login_applicant()
        response = self.client.get(reverse('search_jobs'))

        self.assertEqual(response.status_code, 200)
        self.assertTemplateUsed(response, 'search_jobs.html')
        self.assertQuerySetEqual(
            response.context['jobs'],
            JobOffer.objects.all().order_by('-created_at'),
            transform=lambda job: job,
        )
        self.assertEqual(response.context['search_query'], '')
        self.assertEqual(response.context['applied_job_ids'], set())

    def test_search_jobs_filters_results_using_trimmed_query(self):
        self.login_applicant()
        response = self.client.get(reverse('search_jobs'), {'q': '  python  '})

        self.assertEqual(response.status_code, 200)
        self.assertQuerySetEqual(
            response.context['jobs'],
            [self.python_job],
            transform=lambda job: job,
        )
        self.assertEqual(response.context['search_query'], 'python')

    def test_search_jobs_includes_applied_job_ids_for_authenticated_user(self):
        JobApplication.objects.create(
            job_offer=self.python_job,
            applicant=self.applicant,
            message='Me interesa esta oferta',
        )
        self.login_applicant()

        response = self.client.get(reverse('search_jobs'))

        self.assertEqual(response.status_code, 200)
        self.assertEqual(response.context['applied_job_ids'], {self.python_job.id})