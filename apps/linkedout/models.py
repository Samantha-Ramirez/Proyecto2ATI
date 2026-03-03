from django.db import models
from django.contrib.auth.models import User

class JobOpportunity(models.Model):
    TYPE_CHOICES = [
        ('post', 'Publicación Normal'),
        ('job_offer', 'Oferta Laboral'),
    ]

    STATUS_CHOICES = [
        ('open', 'Abierta / Recibiendo CVs'),
        ('closed', 'Cerrada / Finalizada'),
    ]

    author = models.ForeignKey(User, on_delete=models.CASCADE, related_name='job_opportunities')
    title = models.CharField(max_length=255)
    content = models.TextField()
    image = models.ImageField(upload_to='job_opportunities_imgs/', null=True, blank=True)
    created_at = models.DateTimeField(auto_now_add=True)
    opportunity_type = models.CharField(max_length=20, choices=TYPE_CHOICES, default='post')

    job_description = models.TextField(null=True, blank=True)
    salary = models.DecimalField(max_digits=10, decimal_places=2, null=True, blank=True)
    position = models.CharField(max_length=150, null=True, blank=True)
    working_hours = models.CharField(max_length=50, null=True, blank=True, help_text="Ej: 40 horas semanales")
    requirements = models.TextField(null=True, blank=True)
    industry = models.CharField(max_length=100, null=True, blank=True)
    offer_status = models.CharField(max_length=20, choices=STATUS_CHOICES, default='open', null=True, blank=True)

    def __str__(self):
        return f"{self.title} ({self.get_opportunity_type_display()})"