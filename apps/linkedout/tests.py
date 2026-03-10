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
