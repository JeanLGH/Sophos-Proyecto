"""
URL configuration for ProyectoUno project.

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/4.2/topics/http/urls/
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
from django.urls import path
from ProyectoUno import views

urlpatterns = [
    path('admin/', admin.site.urls),
    path('', views.pagina_inicio, name='pagina_inicio'),
    path('clientes/', views.lista_clientes, name='lista_clientes'),
    path('juegos/', views.lista_juegos, name='lista_juegos'),
    path('juegos/ingresar_datos_cliente/<int:juego_id>/', views.ingresar_datos_cliente, name='ingresar_datos_cliente'),
    path('pagina-confirmacion-alquiler/', views.pagina_confirmacion_alquiler, name='pagina_confirmacion_alquiler'),
    path('juegos_alquilados/', views.juegos_alquilados_por_clientes, name='juegos_alquilados'),
    path('informe_ventas/', views.informe_ventas, name='informe_ventas'),
    path('generar_pdf/<str:fecha>/', views.generar_pdf, name='generar_pdf'),
     path('consultar_balance/', views.consultar_balance_cliente, name='consultar_balance'),

]
