from django.db import models
from products.models import Medicament

class Fournisseur(models.Model):
    nom = models.CharField(max_length=100)
    contact = models.CharField(max_length=100)
    telephone = models.CharField(max_length=15)

    def __str__(self):
        return self.nom

class Approvisionnement(models.Model):
    medicament = models.ForeignKey(Medicament, on_delete=models.CASCADE)
    fournisseur = models.ForeignKey(Fournisseur, on_delete=models.SET_NULL, null=True)
    quantite_recue = models.PositiveIntegerField()
    date_reception = models.DateTimeField(auto_now_add=True)

    def save(self, *args, **kwargs):
        # Logique intelligente : on augmente le stock automatiquement
        # uniquement lors de la création pour éviter les doublons en cas de modification
        if self._state.adding:
            self.medicament.quantite_stock += self.quantite_recue
            self.medicament.save()
        super().save(*args, **kwargs)
