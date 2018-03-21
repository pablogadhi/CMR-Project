from django.urls import path
from . import views

urlpatterns = [
    path('', views.index, name='index'),
    path('propiedades/', views.PropiedadListView.as_view(), name='propiedades'),
    path('propiedad/<int:pk>', views.PropiedadDetailView.as_view(), name='propiedad-detail'),
]
