from django.contrib import admin
from .models import Fournisseur, Approvisionnement

@admin.register(Fournisseur)
class FournisseurAdmin(admin.ModelAdmin):
    list_display = ('nom', 'telephone', 'contact')
    search_fields = ('nom',)

@admin.register(Approvisionnement)
class ApprovisionnementAdmin(admin.ModelAdmin):
    list_display = ('medicament', 'fournisseur', 'quantite_recue', 'date_reception')
    list_filter = ('date_reception', 'fournisseur')