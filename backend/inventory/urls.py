from django.urls import path
from . import views

urlpatterns = [
    path('fournisseurs/', views.liste_fournisseurs, name='liste_fournisseurs'),
    path('fournisseurs/ajouter/', views.ajouter_fournisseur, name='ajouter_fournisseur'),
    path('fournisseurs/<int:fournisseur_id>/modifier/', views.modifier_fournisseur, name='modifier_fournisseur'),
    path('fournisseurs/<int:fournisseur_id>/supprimer/', views.supprimer_fournisseur, name='supprimer_fournisseur'),
    path('approvisionnements/', views.liste_approvisionnements, name='liste_approvisionnements'),
    path('approvisionnements/ajouter/', views.ajouter_approvisionnement, name='ajouter_approvisionnement'),
]
