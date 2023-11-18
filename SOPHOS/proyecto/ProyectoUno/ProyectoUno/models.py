from django.db import models

class Cliente(models.Model):
    nombre = models.CharField(max_length=100)    
    email = models.EmailField(unique=True)
    edad = models.PositiveIntegerField()
    telefono = models.CharField(max_length=10)
    
    def __str__(self):
        return self.nombre

class Juego(models.Model):
    PLATAFORMA_CHOICES = [
        ('Xbox', 'Xbox'),
        ('PlayStation', 'PlayStation'),
        ('Nintendo', 'Nintendo'),
        ('PC', 'PC'),
    ]
    nombre = models.CharField(max_length=100)
    ano = models.IntegerField()
    protagonistas = models.CharField(max_length=255)
    director = models.CharField(max_length=100)
    productor = models.CharField(max_length=100)
    plataforma = models.CharField(max_length=20, choices=PLATAFORMA_CHOICES)
    precio = models.DecimalField(max_digits=10, decimal_places=2)
    stock = models.PositiveIntegerField(default=0)

    def __str__(self):
        return self.nombre

class Alquiler(models.Model):

    ESTADO_ALQUILER_CHOICES = (
        ('Disponible', 'Disponible'),
        ('En alquiler', 'En alquiler'),
        ('En proceso de entrega', 'En proceso de entrega'),
        ('Devuelto', 'Devuelto'),
        ('Perdido', 'Perdido'),
        ('Dañado', 'Dañado'),
    )
    cliente = models.ForeignKey(Cliente, on_delete=models.CASCADE)
    juego = models.ForeignKey(Juego, on_delete=models.CASCADE)
    fecha_alquiler = models.DateTimeField(auto_now_add=True)
    fecha_devolucion = models.DateTimeField(null=True, blank=True)
    precio = models.DecimalField(max_digits=10, decimal_places=2)
    estado = models.CharField(max_length=50, choices=ESTADO_ALQUILER_CHOICES, default='Disponible')

    def __str__(self):
        return f"{self.cliente.nombre} - {self.juego.nombre}"

class Venta(models.Model):
    alquiler = models.ForeignKey(Alquiler, on_delete=models.CASCADE)
    fecha = models.DateField(auto_now_add=True)
    codigo_venta = models.CharField(max_length=20) 
    monto_total = models.DecimalField(max_digits=10, decimal_places=2)

    def __str__(self):
        return f"Venta # - {self.id} - {self.fecha} "

