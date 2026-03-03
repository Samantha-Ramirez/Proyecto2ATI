from django.db import models
from django.contrib.auth.models import User 
# Create your models here.

class Propuesta(models.Model):
    TIPO_CHOICES = [
        ('publicacion', 'Publicación Normal'),
        ('oferta', 'Oferta Laboral'),
    ]

    ESTADO_CHOICES = [
        ('abierta', 'Abierta / Recibiendo CVs'),
        ('cerrada', 'Cerrada / Finalizada'),
    ]

    # ==========================
    # Campos generales (Para ambos tipos)
    # ==========================
    autor = models.ForeignKey(User, on_delete=models.CASCADE, related_name='propuestas')
    titulo = models.CharField(max_length=255)
    contenido = models.TextField()
    imagen = models.ImageField(upload_to='propuestas_imgs/', null=True, blank=True)
    fecha_creacion = models.DateTimeField(auto_now_add=True)
    tipo = models.CharField(max_length=20, choices=TIPO_CHOICES, default='publicacion')

    # ==========================
    # Campos para ofertaLaboral
    # (Tienen null=True y blank=True para que no sean obligatorios)
    # =========================
    descripcion_puesto = models.TextField(null=True, blank=True)
    salario = models.DecimalField(max_digits=10, decimal_places=2, null=True, blank=True)
    puesto = models.CharField(max_length=150, null=True, blank=True)
    horas_laborales = models.CharField(max_length=50, null=True, blank=True, help_text="Ej: 40 horas semanales")
    requerimientos = models.TextField(null=True, blank=True)
    sector = models.CharField(max_length=100, null=True, blank=True)
    estado_oferta = models.CharField(max_length=20, choices=ESTADO_CHOICES, default='abierta', null=True, blank=True)

    def __str__(self):
        return f"{self.titulo} ({self.get_tipo_display()})"