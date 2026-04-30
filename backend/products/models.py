from django.db import models

class Medicament(models.Model):
    # Attributs issus de votre diagramme de classe
    nom = models.CharField(max_length=100)
    description = models.TextField()
    prix_achat = models.DecimalField(max_digits=10, decimal_places=2)
    prix_vente = models.DecimalField(max_digits=10, decimal_places=2)
    date_expiration = models.DateField()
    categorie = models.CharField(max_length=50)
    quantite_stock = models.IntegerField(default=0)

    # Pour afficher le nom du médicament dans l'interface admin
    def __str__(self):
        return self.nom

    @property
    def marge_percent(self):
        """Calcule la marge bénéficiaire en pourcentage."""
        if self.prix_achat and self.prix_achat > 0:
            return round(((self.prix_vente - self.prix_achat) / self.prix_achat) * 100, 2)
        return 0

    @property
    def valeur_stock(self):
        """Calcule la valeur totale du stock à l'achat."""
        return round(self.prix_achat * self.quantite_stock, 2)
