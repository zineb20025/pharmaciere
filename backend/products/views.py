from django.shortcuts import render, redirect, get_object_or_404
from django.contrib import messages
from django.contrib.auth.decorators import login_required
from django.http import JsonResponse
import json
from .models import Medicament
from sales.models import Vente, LigneVente
from users.decorators import admin_or_pharmacien_required


def redirect_to_dashboard(request):
    """Redirect /products/supprimer/ to dashboard"""
    return redirect('dashboard')


@login_required
def dashboard(request):
    total_medicaments = Medicament.objects.count()
    alertes_stock = Medicament.objects.filter(quantite_stock__lt=10).count()
    total_ventes = Vente.objects.count()

    # On récupère tous les médicaments pour les afficher
    liste_medicaments = Medicament.objects.all()

    # Calcul de la valeur totale du stock et de la marge moyenne
    valeur_totale_stock = sum(m.valeur_stock for m in Medicament.objects.all())
    marges = [m.marge_percent for m in Medicament.objects.all()]
    marge_moyenne = round(sum(marges) / len(marges), 2) if marges else 0

    # Chiffre d'affaires et dernières ventes
    chiffre_affaires = sum(v.total for v in Vente.objects.all())
    dernieres_ventes = Vente.objects.prefetch_related("lignes__medicament").order_by("-date_vente")[:5]

    context = {
        "total_medicaments": total_medicaments,
        "alertes_stock": alertes_stock,
        "total_ventes": total_ventes,
        "liste_medicaments": liste_medicaments,
        "valeur_totale_stock": valeur_totale_stock,
        "marge_moyenne": marge_moyenne,
        "chiffre_affaires": chiffre_affaires,
        "dernieres_ventes": dernieres_ventes,
    }
    return render(request, "products/dashboard.html", context)


def api_medicaments(request):
    """Retour JSON pour la page /stock (frontend React)."""
    total_medicaments = Medicament.objects.count()
    medicaments = Medicament.objects.all().order_by("nom")

    return JsonResponse(
        {
            "total_medicaments": total_medicaments,
            "medicaments": [
                {
                    "id": m.id,
                    "nom": m.nom,
                    "categorie": m.categorie,
                    "quantite_stock": m.quantite_stock,
                    "prix_achat": float(m.prix_achat),
                    "prix_vente": float(m.prix_vente),
                    "date_expiration": m.date_expiration.isoformat() if m.date_expiration else None,
                }
                for m in medicaments
            ],
        }
    )



@admin_or_pharmacien_required
def modifier_prix(request, medicament_id):
    medicament = get_object_or_404(Medicament, id=medicament_id)
    if request.method == 'POST':
        nouveau_prix = request.POST.get('prix_unitaire')
        try:
            prix = float(nouveau_prix)
            if prix > 0:
                medicament.prix_vente = prix
                medicament.save()
                messages.success(request, f'Le prix de {medicament.nom} a été mis à jour à {prix} DH.')
            else:
                messages.error(request, 'Le prix doit être supérieur à 0.')
        except ValueError:
            messages.error(request, 'Veuillez entrer un prix valide.')
    return redirect('dashboard')


@admin_or_pharmacien_required
def ajouter_medicament(request):
    if request.method == 'POST':
        nom = request.POST.get('nom')
        categorie = request.POST.get('categorie')
        description = request.POST.get('description')
        
        try:
            prix_achat = float(request.POST.get('prix_achat'))
            prix_vente = float(request.POST.get('prix_vente'))
            quantite_stock = int(request.POST.get('quantite_stock'))
            
            if nom and categorie and prix_achat > 0 and prix_vente > 0 and quantite_stock >= 0:
                date_expiration = request.POST.get('date_expiration')
                medicament = Medicament.objects.create(
                    nom=nom,
                    categorie=categorie,
                    description=description,
                    prix_achat=prix_achat,
                    prix_vente=prix_vente,
                    quantite_stock=quantite_stock,
                    date_expiration=date_expiration or None
                )
                messages.success(request, f"Le médicament '{medicament.nom}' a été ajouté avec succès.")
                return redirect('dashboard')
            else:
                messages.error(request, 'Veuillez entrer des valeurs valides. Les prix doivent être supérieurs à 0 et la quantité doit être positive.')
        except ValueError:
            messages.error(request, 'Veuillez entrer des valeurs numériques valides.')
    
    # GET request : afficher le formulaire vide
    return render(request, 'products/form_medicament.html', {})


@admin_or_pharmacien_required
def modifier_medicament(request, medicament_id):
    medicament = get_object_or_404(Medicament, id=medicament_id)
    if request.method == 'POST':
        medicament.nom = request.POST.get('nom', medicament.nom)
        medicament.categorie = request.POST.get('categorie', medicament.categorie)
        medicament.description = request.POST.get('description', medicament.description)
        
        try:
            prix_achat = float(request.POST.get('prix_achat', medicament.prix_achat))
            prix_vente = float(request.POST.get('prix_vente', medicament.prix_vente))
            quantite_stock = int(request.POST.get('quantite_stock', medicament.quantite_stock))
            
            if prix_achat > 0 and prix_vente > 0 and quantite_stock >= 0:
                medicament.prix_achat = prix_achat
                medicament.prix_vente = prix_vente
                medicament.quantite_stock = quantite_stock
                
                date_expiration = request.POST.get('date_expiration')
                if date_expiration:
                    medicament.date_expiration = date_expiration
                
                medicament.save()
                messages.success(request, f"Le médicament '{medicament.nom}' a été mis à jour avec succès.")
                return redirect('dashboard')
            else:
                messages.error(request, 'Les prix doivent être supérieurs à 0 et la quantité doit être positive.')
        except ValueError:
            messages.error(request, 'Veuillez entrer des valeurs numériques valides.')
    
    context = {
        'medicament': medicament,
    }
    return render(request, 'products/form_medicament.html', context)


@admin_or_pharmacien_required
def gestion_prix(request):
    categorie_filter = request.GET.get('categorie', '')
    categories = Medicament.objects.values_list('categorie', flat=True).distinct().order_by('categorie')
    
    medicaments = Medicament.objects.all()
    if categorie_filter:
        medicaments = medicaments.filter(categorie=categorie_filter)
    
    context = {
        'medicaments': medicaments,
        'categories': categories,
        'categorie_filter': categorie_filter,
    }
    return render(request, 'products/gestion_prix.html', context)


@admin_or_pharmacien_required
def update_prix(request, medicament_id):
    if request.method == 'POST':
        medicament = get_object_or_404(Medicament, id=medicament_id)
        try:
            data = json.loads(request.body)
            prix_achat = data.get('prix_achat')
            prix_vente = data.get('prix_vente')
            
            if prix_achat is not None:
                prix_achat = float(prix_achat)
                if prix_achat > 0:
                    medicament.prix_achat = prix_achat
                else:
                    return JsonResponse({'success': False, 'error': 'Le prix d\'achat doit être supérieur à 0.'})
            
            if prix_vente is not None:
                prix_vente = float(prix_vente)
                if prix_vente > 0:
                    medicament.prix_vente = prix_vente
                else:
                    return JsonResponse({'success': False, 'error': 'Le prix de vente doit être supérieur à 0.'})
            
            medicament.save()
            return JsonResponse({
                'success': True,
                'marge_percent': medicament.marge_percent,
                'valeur_stock': float(medicament.valeur_stock),
            })
        except (ValueError, json.JSONDecodeError) as e:
            return JsonResponse({'success': False, 'error': str(e)})
    return JsonResponse({'success': False, 'error': 'Méthode non autorisée.'})


@admin_or_pharmacien_required
def supprimer_medicament(request, medicament_id):
    """Supprime un médicament après confirmation"""
    medicament = get_object_or_404(Medicament, id=medicament_id)
    
    # Vérifier si le médicament est référencé dans des ventes
    if LigneVente.objects.filter(medicament=medicament).exists():
        messages.error(request, f'Impossible de supprimer "{medicament.nom}". Ce médicament est référencé dans l\'historique des ventes.')
        return redirect('dashboard')
    
    if request.method == 'POST':
        medicament.delete()
        messages.success(request, f'Médicament "{medicament.nom}" supprimé avec succès!')
        return redirect('dashboard')
    
    context = {
        'medicament': medicament,
        'has_sales': LigneVente.objects.filter(medicament=medicament).exists()
    }
    return render(request, 'products/supprimer_medicament.html', context)

