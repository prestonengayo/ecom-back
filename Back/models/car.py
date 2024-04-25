from django.db import models

class Car(models.Model):
    # Définition des choix possibles pour la boîte de vitesse
    GEARBOX_CHOICES = (
        ('manual', 'Manual'),
        ('automatic', 'Automatic'),
    )

    # Définition des choix possibles pour le type de moteur
    ENGINE_TYPE_CHOICES = (
        ('electric', 'Electric'),
        ('mechanical', 'Mechanical'),
        ('hybrid', 'Hybrid'),
    )

    # Attributs du modèle
    name = models.CharField(max_length=100)
    brand = models.CharField(max_length=100)
    description = models.TextField()
    color = models.CharField(max_length=50)
    gearbox = models.CharField(max_length=10, choices=GEARBOX_CHOICES, default='manual')
    engine_type = models.CharField(max_length=10, choices=ENGINE_TYPE_CHOICES, default='mechanical')

    def __str__(self):
        return f"{self.brand} {self.name} ({self.color})"

