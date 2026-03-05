from django.db import models
from django.contrib.auth.models import User


class Post(models.Model):
    author = models.ForeignKey(User, on_delete=models.CASCADE, related_name="posts")
    title = models.CharField(max_length=255, blank=True)
    content = models.TextField()
    image = models.ImageField(upload_to="posts_imgs/", null=True, blank=True)
    created_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f"Post #{self.id} by {self.author}"


class JobOffer(Post):
    STATUS_CHOICES = [
        ("open", "Abierta / Recibiendo CVs"),
        ("closed", "Cerrada / Finalizada"),
    ]

    job_description = models.TextField()
    salary = models.DecimalField(max_digits=10, decimal_places=2, null=True, blank=True)
    position = models.CharField(max_length=150)
    working_hours = models.CharField(max_length=50, help_text="Ej: 40 horas semanales")
    requirements = models.TextField()
    industry = models.CharField(max_length=150)
    offer_status = models.CharField(max_length=20, choices=STATUS_CHOICES, default="open")

    def __str__(self):
        return f"{self.title} (Oferta)"


class JobApplication(models.Model):
    job_offer = models.ForeignKey(JobOffer, on_delete=models.CASCADE, related_name="applications")
    applicant = models.ForeignKey(User, on_delete=models.CASCADE, related_name="job_applications")
    created_at = models.DateTimeField(auto_now_add=True)
    message = models.TextField(blank=True)

    class Meta:
        unique_together = [("job_offer", "applicant")]
