from django.db import models
from products.models import Medicament
from django.conf import settings


class Vente(models.Model):
    employe = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE)
    nom_client = models.CharField(max_length=200, blank=True, default='')
    date_vente = models.DateTimeField(auto_now_add=True)
    total = models.DecimalField(max_digits=10, decimal_places=2, default=0)

    def __str__(self):
        return f"Vente #{self.id} - {self.date_vente.strftime('%d/%m/%Y')}"

    def calculer_total(self):
        total = sum(ligne.quantite * ligne.prix_unitaire for ligne in self.lignes.all())
        self.total = total
        self.save(update_fields=['total'])


class LigneVente(models.Model):
    vente = models.ForeignKey(Vente, related_name='lignes', on_delete=models.CASCADE)
    medicament = models.ForeignKey(Medicament, on_delete=models.PROTECT)
    quantite = models.PositiveIntegerField()
    prix_unitaire = models.DecimalField(max_digits=10, decimal_places=2)

    @property
    def sous_total(self):
        return self.quantite * self.prix_unitaire

    def save(self, *args, **kwargs):
        if not self._state.adding:
            # Mise à jour : récupérer l'ancienne quantité pour ajuster le stock
            try:
                ancienne = LigneVente.objects.get(pk=self.pk)
                difference = self.quantite - ancienne.quantite
                if self.medicament.quantite_stock >= difference:
                    self.medicament.quantite_stock -= difference
                    self.medicament.save()
                else:
                    raise ValueError("Stock insuffisant pour ce médicament !")
            except LigneVente.DoesNotExist:
                pass
        else:
            # Création
            if self.medicament.quantite_stock >= self.quantite:
                self.medicament.quantite_stock -= self.quantite
                self.medicament.save()
            else:
                raise ValueError("Stock insuffisant pour ce médicament !")
        super().save(*args, **kwargs)
        self.vente.calculer_total()

    def delete(self, *args, **kwargs):
        # Restaurer le stock lors de la suppression d'une ligne de vente
        vente = self.vente
        self.medicament.quantite_stock += self.quantite
        self.medicament.save()
        super().delete(*args, **kwargs)
        # Ne pas recalculer si la vente entière est en cours de suppression
        if Vente.objects.filter(pk=vente.pk).exists():
            vente.calculer_total()

