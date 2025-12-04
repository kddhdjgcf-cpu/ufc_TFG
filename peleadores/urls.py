from django.urls import path
from . import views

urlpatterns = [
    path('', views.index, name='inicio'),
    path('peleadores/', views.lista_peleadores, name='lista_peleadores'),
    path('peleadores/<int:id>/', views.detalle_peleador, name='detalle_peleador'),
    path('comparar_peleadores/', views.comparar_peleadores, name='comparar_peleadores'),
    path('noticias/', views.ufc_noticias, name='ufc_noticias'),
    path('estadisticas/', views.estadisticas, name='estadisticas'),
    path("eventos/", views.ufc_eventos, name="eventos"),
]