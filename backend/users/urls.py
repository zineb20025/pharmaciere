from django.urls import path
from django.contrib.auth import views as auth_views
from . import views

urlpatterns = [
    path('login/', views.RoleBasedLoginView.as_view(), name='login'),
    path('logout/', auth_views.LogoutView.as_view(next_page='/comptes/login/'), name='logout'),
    
    # Admin interface
    path('admin-dashboard/', views.admin_dashboard, name='admin_dashboard'),
    path('employes/', views.liste_employes, name='liste_employes'),
    path('employes/ajouter/', views.ajouter_employe, name='ajouter_employe'),
    path('employes/<int:employe_id>/modifier/', views.modifier_employe, name='modifier_employe'),
    path('employes/<int:employe_id>/supprimer/', views.supprimer_employe, name='supprimer_employe'),
    path('employes/<int:employe_id>/toggle-statut/', views.toggle_statut_employe, name='toggle_statut_employe'),
    path('permissions/', views.permissions_roles, name='permissions_roles'),
]

