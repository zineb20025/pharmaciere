from django.contrib import admin
from .models import Vente, LigneVente

class LigneVenteInline(admin.TabularInline):
    model = LigneVente
    extra = 1  # Nombre de lignes vides affichées par défaut

@admin.register(Vente)
class VenteAdmin(admin.ModelAdmin):
    list_display = ('id', 'employe', 'date_vente', 'total')
    list_filter = ('date_vente', 'employe')
    inlines = [LigneVenteInline]
    
    # On définit l'employé connecté par défaut lors d'une vente
    def save_model(self, request, obj, form, change):
        if not obj.pk:
            obj.employe = request.user
        super().save_model(request, obj, form, change)