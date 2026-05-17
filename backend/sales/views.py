from django.shortcuts import render, redirect, get_object_or_404
from django.contrib.auth.decorators import login_required
from django.contrib import messages
from django.db import transaction
from .models import Vente, LigneVente
from products.models import Medicament
from django.http import HttpResponse

@login_required
def liste_ventes(request):
    """Liste toutes les ventes, filtrées par employé connecté si souhaité"""
    ventes = Vente.objects.select_related('employe').prefetch_related('lignes__medicament').order_by('-date_vente')
    return render(request, 'sales/liste_ventes.html', {'ventes': ventes})

@login_required
def nouvelle_vente(request):
    """Crée une nouvelle vente - version originale simple (1 médicament)"""
    categories = list(Medicament.objects.values_list('categorie', flat=True).distinct())
    if request.method == 'POST':
        nom_client = request.POST.get('nom_client', '')
        categorie = request.POST.get('categorie', '')
        medicament_id = request.POST.get('medicament_id')
        quantite = int(request.POST.get('quantite', 0))
        prix_unitaire = float(request.POST.get('prix_unitaire', 0))

        try:
            medicament = get_object_or_404(Medicament, id=medicament_id)

            if medicament.necessite_ordonnance:
                ordonnance_file = request.FILES.get('ordonnance_file')
                if not ordonnance_file:
                    messages.error(request, 'Ce médicament nécessite une ordonnance valide.')
                    return render(request, 'sales/nouvelle_vente.html', {
                        'medicaments': Medicament.objects.filter(quantite_stock__gt=0),
                        'categories': categories
                    }, status=422)
                if not ordonnance_file.name.lower().endswith(('.pdf', '.jpg', '.jpeg', '.png', '.gif')):
                    messages.error(request, 'Format de fichier d\'ordonnance invalide. Utilisez PDF ou image.')
                    return render(request, 'sales/nouvelle_vente.html', {
                        'medicaments': Medicament.objects.filter(quantite_stock__gt=0),
                        'categories': categories
                    }, status=422)

            with transaction.atomic():
                vente = Vente.objects.create(employe=request.user, nom_client=nom_client)
                LigneVente.objects.create(
                    vente=vente,
                    medicament=medicament,
                    quantite=quantite,
                    prix_unitaire=prix_unitaire
                )
                messages.success(request, f'Vente #{vente.id} créée avec succès!')
                return redirect('facture_vente', vente_id=vente.id)
        except Exception as e:
            messages.error(request, f'Erreur: {str(e)}')

    medicaments = Medicament.objects.filter(quantite_stock__gt=0)
    return render(request, 'sales/nouvelle_vente.html', {
        'medicaments': medicaments,
        'categories': categories
    })

@login_required
def facture_vente(request, vente_id):
    """Affiche la facture PDF imprimable d'une vente"""
    vente = get_object_or_404(Vente, id=vente_id, employe=request.user)
    return render(request, 'sales/facture.html', {'vente': vente})

@login_required
def detail_vente(request, vente_id):
    """Détails d'une vente avec ses lignes"""
    vente = get_object_or_404(Vente, id=vente_id)
    return render(request, 'sales/detail_vente.html', {'vente': vente})

@login_required
def supprimer_vente(request, vente_id):
    """Supprime une vente après confirmation"""
    vente = get_object_or_404(Vente, id=vente_id)
    if request.method == 'POST':
        # Les lignes restaurent déjà le stock via delete()
        vente.delete()
        messages.success(request, 'Vente supprimée avec succès!')
        return redirect('liste_ventes')
    return render(request, 'sales/supprimer_vente.html', {'vente': vente})

