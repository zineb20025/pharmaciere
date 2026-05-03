from django.urls import path
from . import views

urlpatterns = [
    path('supprimer/', views.redirect_to_dashboard, name='supprimer'),
    path('supprimer/<int:medicament_id>/', views.supprimer_medicament, name='supprimer_medicament'),
]
