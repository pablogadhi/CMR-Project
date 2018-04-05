from django.urls import path
from . import views

urlpatterns = [
    path('', views.index, name='index'),
    path('propiedades/', views.PropiedadListView.as_view(), name='propiedades'),
    path('compradores/', views.CompradorListView.as_view(), name='compradores'),
    path('intermediarios/', views.IntermediarioListView.as_view(), name='intermediarios'),
    path('propietarios/', views.PropetarioListView.as_view(), name='propietarios'),

    path('visitas/', views.VisitaListView.as_view(), name='visitas'),
    path('administracion/', views.AdministraListView.as_view(), name='administraciones'),
    path('tweets/', views.TweetListView.as_view(), name='tweets'),

    path('propiedad/<int:pk>', views.PropiedadDetailView.as_view(), name='propiedad-detail'),
    path('dummy/', views.dummy, name='dummy'),
    path('reset/', views.reset, name='reset')
]
