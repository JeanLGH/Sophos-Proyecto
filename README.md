# Sophos-project
Proyecto final del curso de SOPHOS ACADEMY

Proyecto de Tienda de Videojuegos
  Este es un proyecto de una tienda de videojuegos desarrollado con Django, un marco de desarrollo web de alto nivel en Python.

Características
  Clientes: Gestión de información sobre los clientes, incluyendo nombre, correo electrónico, edad y teléfono.
  Juegos: Registro y seguimiento de detalles de los juegos disponibles, como el nombre, año de lanzamiento, protagonistas, director, productor, plataforma, precio y stock.
  Alquileres: Manejo de alquileres de juegos, incluyendo fechas de alquiler y devolución, precio, estado del alquiler y detalles del cliente y juego asociados.
  Ventas: Registro de ventas generadas a partir de alquileres, con información sobre la fecha de venta, un código único de venta y el monto total.
Estructura del Proyecto
  ProyectoUno: Carpeta principal del proyecto Django.
  settings.py: Configuración principal del proyecto.
  urls.py: Definición de las rutas URL del proyecto.
  ProyectoUno/app: Carpeta de la aplicación principal del proyecto.
  models.py: Definición de modelos de base de datos.
  views.py: Lógica de vistas para renderizar páginas web.
  templates: Plantillas HTML para las páginas web.
  static: Archivos estáticos como CSS, JavaScript, imágenes, etc.


Requisitos del Sistema
  Python 3.11.5
  Django 4.2.5


Instalación
Clona este repositorio en tu máquina local.
  git clone https://url-de-tu-repositorio.git
Crea y activa un entorno virtual.
  python -m venv venv
  source venv/bin/activate  # Para sistemas basados en Unix
Instala las dependencias.
    pip install -r requirements.txt
Aplica las migraciones.
    python manage.py migrate
Inicia el servidor de desarrollo.
    python manage.py runserver
    Visita http://localhost:8000 en tu navegador para ver la aplicación.
