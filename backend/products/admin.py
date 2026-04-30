from django.contrib import admin
from .models import Medicament


@admin.register(Medicament)
class MedicamentAdmin(admin.ModelAdmin):
    list_display = ('nom', 'categorie', 'prix_achat', 'prix_vente', 'marge_percent', 'quantite_stock_coloree')
    list_editable = ('prix_achat', 'prix_vente')
    list_filter = ('categorie',)
    search_fields = ('nom', 'categorie')
    ordering = ('nom',)

    @admin.display(description='Quantité en Stock')
    def quantite_stock_coloree(self, obj):
        from django.utils.html import format_html
        if obj.quantite_stock < 10:
            return format_html(
                '<span style="color: #dc3545; font-weight: bold;">⚠️ {} unités</span>',
                obj.quantite_stock
            )
        return format_html(
            '<span style="color: #198754; font-weight: bold;">{} unités</span>',
            obj.quantite_stock
        )
