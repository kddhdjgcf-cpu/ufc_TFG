from django.urls import path
from . import views
from django.contrib.auth import views as auth_views

urlpatterns = [
    path('', views.index, name='inicio'),
    path('peleadores/', views.lista_peleadores, name='lista_peleadores'),
    path('peleadores/<int:id>/', views.detalle_peleador, name='detalle_peleador'),
    path('comparar_peleadores/', views.comparar_peleadores, name='comparar_peleadores'),
    path('noticias/', views.ufc_noticias, name='ufc_noticias'),
    path('estadisticas/', views.estadisticas, name='estadisticas'),
    path("eventos/", views.ufc_eventos, name="eventos"),
    path("crear/", views.crear_peleador, name="crear_peleador"),
    path("editar/<int:id>/", views.editar_peleador, name="editar_peleador"),
    path("eliminar/<int:id>/", views.eliminar_peleador, name="eliminar_peleador"),
    path("login/", auth_views.LoginView.as_view(template_name="login.html"), name="login"),
    path("logout/", auth_views.LogoutView.as_view(), name="logout"),

]