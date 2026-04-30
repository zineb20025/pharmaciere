from django.shortcuts import render, redirect, get_object_or_404
from django.contrib import messages
from django.contrib.auth import get_user_model
from django.contrib.auth import views as auth_views
from django.db import models
from .decorators import admin_required, admin_or_pharmacien_required
from products.models import Medicament
from sales.models import Vente
from inventory.models import Fournisseur

Employe = get_user_model()


class RoleBasedLoginView(auth_views.LoginView):
    """Vue de connexion qui redirige selon le rôle de l'utilisateur."""
    def get_success_url(self):
        user = self.request.user
        if hasattr(user, 'role'):
            if user.role == Employe.ROLE_ADMIN:
                return '/comptes/admin-dashboard/'
            elif user.role == Employe.ROLE_PHARMACIEN:
                return '/'
            elif user.role == Employe.ROLE_CAISSIER:
                return '/'
        return super().get_success_url()


@admin_or_pharmacien_required
def admin_dashboard(request):
    total_employes = Employe.objects.count()
    chiffre_affaires_total = sum(v.total for v in Vente.objects.all())
    alertes_stock = Medicament.objects.filter(quantite_stock__lt=10).count()
    total_fournisseurs = Fournisseur.objects.count()

    context = {
        'total_employes': total_employes,
        'chiffre_affaires_total': chiffre_affaires_total,
        'alertes_stock': alertes_stock,
        'total_fournisseurs': total_fournisseurs,
    }
    return render(request, 'users/admin_dashboard.html', context)


@admin_or_pharmacien_required
def liste_employes(request):
    employes = Employe.objects.all().order_by('-date_joined')

    # Recherche
    q = request.GET.get('q', '')
    if q:
        employes = employes.filter(
            models.Q(username__icontains=q) |
            models.Q(first_name__icontains=q) |
            models.Q(last_name__icontains=q) |
            models.Q(email__icontains=q) |
            models.Q(telephone__icontains=q)
        )

    # Filtre par rôle
    role_filter = request.GET.get('role', '')
    if role_filter:
        employes = employes.filter(role=role_filter)

    # Filtre par statut
    statut_filter = request.GET.get('statut', '')
    if statut_filter == 'actif':
        employes = employes.filter(is_active=True)
    elif statut_filter == 'inactif':
        employes = employes.filter(is_active=False)

    context = {
        'employes': employes,
        'q': q,
        'role_filter': role_filter,
        'statut_filter': statut_filter,
        'roles': Employe.ROLES,
    }
    return render(request, 'users/liste_employes.html', context)


@admin_or_pharmacien_required
def ajouter_employe(request):
    if request.method == 'POST':
        username = request.POST.get('username')
        first_name = request.POST.get('first_name', '')
        last_name = request.POST.get('last_name', '')
        email = request.POST.get('email', '')
        password = request.POST.get('password')
        role = request.POST.get('role', Employe.ROLE_CAISSIER)
        telephone = request.POST.get('telephone', '')

        if not username or not password:
            messages.error(request, "Le nom d'utilisateur et le mot de passe sont obligatoires.")
            return render(request, 'users/form_employe.html')

        if Employe.objects.filter(username=username).exists():
            messages.error(request, f"Le nom d'utilisateur '{username}' existe déjà.")
            return render(request, 'users/form_employe.html')

        try:
            employe = Employe.objects.create_user(
                username=username,
                password=password,
                first_name=first_name,
                last_name=last_name,
                email=email,
                role=role,
                telephone=telephone,
            )
            messages.success(request, f"L'employé '{employe.username}' a été créé avec succès.")
            return redirect('liste_employes')
        except Exception as e:
            messages.error(request, f"Erreur lors de la création de l'employé : {str(e)}")

    return render(request, 'users/form_employe.html')


@admin_or_pharmacien_required
def modifier_employe(request, employe_id):
    employe = get_object_or_404(Employe, id=employe_id)

    if request.method == 'POST':
        employe.first_name = request.POST.get('first_name', '')
        employe.last_name = request.POST.get('last_name', '')
        employe.email = request.POST.get('email', '')
        employe.role = request.POST.get('role', employe.role)
        employe.telephone = request.POST.get('telephone', '')
        employe.is_active = request.POST.get('is_active') == 'on'

        password = request.POST.get('password')
        if password:
            employe.set_password(password)

        try:
            employe.save()
            messages.success(request, f"L'employé '{employe.username}' a été mis à jour avec succès.")
            return redirect('liste_employes')
        except Exception as e:
            messages.error(request, f"Erreur lors de la mise à jour : {str(e)}")

    context = {
        'employe': employe,
    }
    return render(request, 'users/form_employe.html', context)


@admin_required
def supprimer_employe(request, employe_id):
    employe = get_object_or_404(Employe, id=employe_id)

    if employe == request.user:
        messages.error(request, "Vous ne pouvez pas supprimer votre propre compte.")
        return redirect('liste_employes')

    if request.method == 'POST':
        try:
            username = employe.username
            employe.delete()
            messages.success(request, f"L'employé '{username}' a été supprimé avec succès.")
            return redirect('liste_employes')
        except Exception as e:
            messages.error(request, f"Erreur lors de la suppression : {str(e)}")

    context = {
        'employe': employe,
    }
    return render(request, 'users/supprimer_employe.html', context)


@admin_or_pharmacien_required
def toggle_statut_employe(request, employe_id):
    employe = get_object_or_404(Employe, id=employe_id)

    if employe == request.user:
        messages.error(request, "Vous ne pouvez pas désactiver votre propre compte.")
        return redirect('liste_employes')

    employe.is_active = not employe.is_active
    employe.save()
    statut = 'activé' if employe.is_active else 'désactivé'
    messages.success(request, f"L'employé '{employe.username}' a été {statut} avec succès.")
    return redirect('liste_employes')


@admin_or_pharmacien_required
def permissions_roles(request):
    roles_permissions = {
        Employe.ROLE_ADMIN: {
            'label': 'Administrateur',
            'icon': 'fa-shield-halved',
            'color': 'danger',
            'permissions': Employe(role=Employe.ROLE_ADMIN).get_permissions_list(),
        },
        Employe.ROLE_PHARMACIEN: {
            'label': 'Pharmacien',
            'icon': 'fa-user-doctor',
            'color': 'primary',
            'permissions': Employe(role=Employe.ROLE_PHARMACIEN).get_permissions_list(),
        },
        Employe.ROLE_CAISSIER: {
            'label': 'Caissier',
            'icon': 'fa-cash-register',
            'color': 'secondary',
            'permissions': Employe(role=Employe.ROLE_CAISSIER).get_permissions_list(),
        },
    }
    context = {
        'roles_permissions': roles_permissions,
    }
    return render(request, 'users/permissions_roles.html', context)


