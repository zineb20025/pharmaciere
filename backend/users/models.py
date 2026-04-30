from django.contrib.auth.models import AbstractUser
from django.db import models

class Employe(AbstractUser):
    ROLE_ADMIN = 'admin'
    ROLE_PHARMACIEN = 'pharmacien'
    ROLE_CAISSIER = 'caissier'

    ROLES = (
        (ROLE_ADMIN, 'Admin'),
        (ROLE_PHARMACIEN, 'Pharmacien'),
        (ROLE_CAISSIER, 'Caissier'),
    )
    role = models.CharField(max_length=20, choices=ROLES, default=ROLE_CAISSIER)
    telephone = models.CharField(max_length=15, blank=True)

    def __str__(self):
        return f"{self.username} ({self.get_role_display()})"

    @property
    def statut(self):
        return 'Actif' if self.is_active else 'Inactif'

    def get_permissions_list(self):
        permissions = {
            self.ROLE_ADMIN: [
                'Accès complet à l\'administration',
                'Gestion des employés (CRUD)',
                'Gestion des fournisseurs',
                'Gestion des approvisionnements',
                'Gestion des prix et stocks',
                'Consultation et création des ventes',
                'Accès au tableau de bord global',
            ],
            self.ROLE_PHARMACIEN: [
                'Consultation du tableau de bord',
                'Gestion des prix et stocks',
                'Gestion des fournisseurs',
                'Gestion des approvisionnements',
                'Consultation et création des ventes',
            ],
            self.ROLE_CAISSIER: [
                'Consultation du stock (lecture seule)',
            ],
        }
        return permissions.get(self.role, [])
