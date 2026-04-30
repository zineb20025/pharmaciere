from django.urls import path
from . import views

urlpatterns = [
    path('', views.liste_ventes, name='liste_ventes'),
    path('nouvelle/', views.nouvelle_vente, name='nouvelle_vente'),
    path('<int:vente_id>/', views.detail_vente, name='detail_vente'),
    path('<int:vente_id>/facture/', views.facture_vente, name='facture_vente'),
    path('<int:vente_id>/supprimer/', views.supprimer_vente, name='supprimer_vente'),
]

