"""
URL configuration for backend project.

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/6.0/topics/http/urls/
Examples:
Function views
    1. Add an import:  from my_app import views
    2. Add a URL to urlpatterns:  path('', views.home, name='home')
Class-based views
    1. Add an import:  from other_app.views import Home
    2. Add a URL to urlpatterns:  path('', Home.as_view(), name='home')
Including another URLconf
    1. Import the include() function: from django.urls import include, path
    2. Add a URL to urlpatterns:  path('blog/', include('blog.urls'))
"""
from django.contrib import admin
from django.urls import path, include
from products.views import dashboard, modifier_prix, gestion_prix, update_prix, modifier_medicament, ajouter_medicament




urlpatterns = [
    path('admin/', admin.site.urls),
    path('', dashboard, name='dashboard'),
path('modifier-prix/<int:medicament_id>/', modifier_prix, name='modifier_prix'),
    path('modifier-medicament/<int:medicament_id>/', modifier_medicament, name='modifier_medicament'),
    path('ajouter-medicament/', ajouter_medicament, name='ajouter_medicament'),
    path('gestion-prix/', gestion_prix, name='gestion_prix'),
    path('api/update-prix/<int:medicament_id>/', update_prix, name='update_prix'),
    path('ventes/', include('sales.urls')),
    path('comptes/', include('users.urls')),
    path('inventory/', include('inventory.urls')),
]
