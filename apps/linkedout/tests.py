from django.test import TestCase
from django.urls import reverse
from django.contrib.auth.models import User
from .models import Profile


class ProfileTemplateTests(TestCase):
    def setUp(self):
        # Configuramos un usuario y perfil de prueba antes de cada test
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
        """
        Prueba que la página de perfil carga, usa el template correcto
        y contiene los elementos clave del HTML.
        """
        # 1. Iniciar sesión con el usuario de prueba
        self.client.login(username='testuser', password='testpassword123')

        # 2. Hacer una petición GET a la vista del perfil
        response = self.client.get(reverse('profile'))

        # 3. Verificar que la respuesta sea exitosa (HTTP 200)
        self.assertEqual(response.status_code, 200)

        # 4. Verificar que se está usando el template
        self.assertTemplateUsed(response, 'profile.html')

        # 5. Verificar que el HTML contiene IDs y textos específicos
        self.assertContains(response, 'id="banner-upload"')
        self.assertContains(response, 'id="avatar-upload"')
        self.assertContains(response, 'id="profile-edit-form"')
        self.assertContains(response, 'First Guy')
