from django.shortcuts import render, redirect, get_object_or_404
from django.contrib import messages
from users.decorators import admin_or_pharmacien_required
from .models import Fournisseur, Approvisionnement
from products.models import Medicament


@admin_or_pharmacien_required
def liste_fournisseurs(request):
    fournisseurs = Fournisseur.objects.all().order_by('nom')
    context = {
        'fournisseurs': fournisseurs,
    }
    return render(request, 'inventory/liste_fournisseurs.html', context)


@admin_or_pharmacien_required
def ajouter_fournisseur(request):
    if request.method == 'POST':
        nom = request.POST.get('nom')
        contact = request.POST.get('contact', '')
        telephone = request.POST.get('telephone', '')

        if not nom:
            messages.error(request, "Le nom du fournisseur est obligatoire.")
            return render(request, 'inventory/form_fournisseur.html')

        try:
            fournisseur = Fournisseur.objects.create(
                nom=nom,
                contact=contact,
                telephone=telephone,
            )
            messages.success(request, f"Le fournisseur '{fournisseur.nom}' a été ajouté avec succès.")
            return redirect('liste_fournisseurs')
        except Exception as e:
            messages.error(request, f"Erreur lors de l'ajout : {str(e)}")

    return render(request, 'inventory/form_fournisseur.html')


@admin_or_pharmacien_required
def modifier_fournisseur(request, fournisseur_id):
    fournisseur = get_object_or_404(Fournisseur, id=fournisseur_id)

    if request.method == 'POST':
        fournisseur.nom = request.POST.get('nom', fournisseur.nom)
        fournisseur.contact = request.POST.get('contact', fournisseur.contact)
        fournisseur.telephone = request.POST.get('telephone', fournisseur.telephone)

        try:
            fournisseur.save()
            messages.success(request, f"Le fournisseur '{fournisseur.nom}' a été mis à jour avec succès.")
            return redirect('liste_fournisseurs')
        except Exception as e:
            messages.error(request, f"Erreur lors de la mise à jour : {str(e)}")

    context = {
        'fournisseur': fournisseur,
    }
    return render(request, 'inventory/form_fournisseur.html', context)


@admin_or_pharmacien_required
def supprimer_fournisseur(request, fournisseur_id):
    fournisseur = get_object_or_404(Fournisseur, id=fournisseur_id)

    if request.method == 'POST':
        try:
            nom = fournisseur.nom
            fournisseur.delete()
            messages.success(request, f"Le fournisseur '{nom}' a été supprimé avec succès.")
            return redirect('liste_fournisseurs')
        except Exception as e:
            messages.error(request, f"Erreur lors de la suppression : {str(e)}")

    context = {
        'fournisseur': fournisseur,
    }
    return render(request, 'inventory/supprimer_fournisseur.html', context)


@admin_or_pharmacien_required
def liste_approvisionnements(request):
    approvisionnements = Approvisionnement.objects.select_related('medicament', 'fournisseur').order_by('-date_reception')
    context = {
        'approvisionnements': approvisionnements,
    }
    return render(request, 'inventory/liste_approvisionnements.html', context)


@admin_or_pharmacien_required
def ajouter_approvisionnement(request):
    medicaments = Medicament.objects.all().order_by('nom')
    fournisseurs = Fournisseur.objects.all().order_by('nom')

    if request.method == 'POST':
        medicament_id = request.POST.get('medicament')
        fournisseur_id = request.POST.get('fournisseur')
        quantite_recue = request.POST.get('quantite_recue')

        if not medicament_id or not quantite_recue:
            messages.error(request, "Le médicament et la quantité reçue sont obligatoires.")
            context = {
                'medicaments': medicaments,
                'fournisseurs': fournisseurs,
            }
            return render(request, 'inventory/form_approvisionnement.html', context)

        try:
            medicament = Medicament.objects.get(id=medicament_id)
            fournisseur = Fournisseur.objects.get(id=fournisseur_id) if fournisseur_id else None
            quantite = int(quantite_recue)

            if quantite <= 0:
                messages.error(request, "La quantité reçue doit être supérieure à 0.")
                context = {
                    'medicaments': medicaments,
                    'fournisseurs': fournisseurs,
                }
                return render(request, 'inventory/form_approvisionnement.html', context)

            appro = Approvisionnement.objects.create(
                medicament=medicament,
                fournisseur=fournisseur,
                quantite_recue=quantite,
            )
            messages.success(request, f"Approvisionnement de {quantite} unités de '{medicament.nom}' enregistré. Stock actuel : {medicament.quantite_stock}")
            return redirect('liste_approvisionnements')
        except Medicament.DoesNotExist:
            messages.error(request, "Médicament introuvable.")
        except Fournisseur.DoesNotExist:
            messages.error(request, "Fournisseur introuvable.")
        except ValueError:
            messages.error(request, "La quantité doit être un nombre entier valide.")
        except Exception as e:
            messages.error(request, f"Erreur lors de l'enregistrement : {str(e)}")

    context = {
        'medicaments': medicaments,
        'fournisseurs': fournisseurs,
    }
    return render(request, 'inventory/form_approvisionnement.html', context)
