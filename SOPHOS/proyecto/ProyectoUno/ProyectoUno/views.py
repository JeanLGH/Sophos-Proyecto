from django.shortcuts import get_object_or_404, redirect, render
import uuid
from ProyectoUno.models import Cliente, Juego, Alquiler, Venta
from django.db.models import Count, Sum, Q
from datetime import  datetime
from django.http import HttpResponseBadRequest, HttpResponse
from reportlab.pdfgen import canvas
from io import BytesIO
from itertools import groupby
from datetime import timedelta

def pagina_inicio(request):
    return render(request, '../templates/inicio.html')
def lista_clientes(request):
    clientes = Cliente.objects.all()
    return render(request, 'lista_clientes.html', {'clientes': clientes})

def lista_juegos(request):
    juegos = Juego.objects.all()
    # Obtener los parámetros de búsqueda de la solicitud GET
    busqueda = request.GET.get('busqueda')
    ano = request.GET.get('ano')
    precio_min = request.GET.get('precio_min')
    precio_max = request.GET.get('precio_max')
    plataforma = request.GET.get('plataforma')
    

    if busqueda:
        juegos = juegos.filter(Q(nombre__icontains=busqueda) | Q(director__icontains=busqueda) | Q(protagonistas__icontains=busqueda) | Q(productor__icontains=busqueda))
    if ano:
         juegos = juegos.filter(ano=ano)
    if precio_min:
        juegos = juegos.filter(precio__gte=precio_min)
    if precio_max:
        juegos = juegos.filter(precio__lte=precio_max)
    if plataforma:
        juegos = juegos.filter(plataforma=plataforma)


    return render(request, 'lista_juegos.html', {'juegos': juegos})



def calcular_precio_alquiler(juego):
    precio_base = juego.precio
    if juego.plataforma == 'Xbox':
        precio_base += 2
    elif juego.plataforma == 'PlayStation' or juego.plataforma == 'PC' or juego.plataforma == 'Nintendo' :
        precio_base += 3  

    
    
    return precio_base




def ingresar_datos_cliente(request, juego_id):
    juego = get_object_or_404(Juego, id=juego_id)
    precio_alquiler = calcular_precio_alquiler(juego)
    fecha_alquiler = datetime.now()

    # Calcular la fecha de devolución (30 días después)
    fecha_devolucion = fecha_alquiler + timedelta(days=30)
    
    if request.method == 'POST':
        nombre_cliente = request.POST.get('nombre_cliente')
        email = request.POST.get('email')
        telefono_cliente = request.POST.get('telefono_cliente')
        edad_cliente = request.POST.get('edad_cliente')

        if not nombre_cliente or not email or not telefono_cliente or not edad_cliente:
            return HttpResponseBadRequest("Por favor, completa todos los campos del formulario.")

        # Generar un código de venta único por fecha de alquiler
        codigo_venta = f"{fecha_alquiler.strftime('%Y%m%d')}-{str(uuid.uuid4())}"

        # Crear un nuevo cliente
        cliente = Cliente.objects.create(nombre=nombre_cliente, email=email, telefono=telefono_cliente, edad=edad_cliente)
        if juego.stock > 0:
            alquiler = Alquiler.objects.create(cliente=cliente, fecha_alquiler=fecha_alquiler, juego=juego, precio=precio_alquiler, fecha_devolucion=fecha_devolucion)
            venta = Venta.objects.create(alquiler=alquiler, monto_total=precio_alquiler, fecha=fecha_alquiler, codigo_venta=codigo_venta)
            juego.stock -= 1
            juego.save()
            return redirect('pagina_confirmacion_alquiler')
        else:
            return HttpResponseBadRequest("Lo siento, no hay suficientes juegos en stock para alquilar.")

    return render(request, 'ingresar_datos_cliente.html', {'juego': juego, 'precio_alquiler': precio_alquiler})




def pagina_confirmacion_alquiler(request):
    return render(request, 'confirmacion_alquiler.html')
        




def informe_ventas(request):
    fecha_inicio = request.GET.get('fecha_inicio', None)
    fecha_fin = request.GET.get('fecha_fin', None) 
    codigo_venta = request.GET.get('codigo_venta', None)
    ventas = Venta.objects.all().order_by('-fecha')
    if fecha_inicio and fecha_fin:
        ventas = ventas.filter(fecha__range=[fecha_inicio, fecha_fin])
    if codigo_venta:
        ventas = ventas.filter(codigo_venta=codigo_venta)
    ventas_agrupadas = {}
    for (fecha, codigo_venta), group in groupby(ventas, key=lambda x: (x.fecha, x.codigo_venta)):
        ventas_agrupadas.setdefault(fecha, []).extend(list(group))

    # Calcular el total de todas las ventas
    total_ventas = Venta.objects.aggregate(Sum('monto_total'))['monto_total__sum'] or 0

    return render(request, 'informe_ventas.html', {'ventas_agrupadas': ventas_agrupadas, 'total_ventas': total_ventas})

def generar_pdf(request, fecha):
    ventas_en_fecha = Venta.objects.filter(fecha=fecha)
    total_ventas_fecha = ventas_en_fecha.aggregate(Sum('monto_total'))['monto_total__sum'] or 0
    response = HttpResponse(content_type='application/pdf')
    response['Content-Disposition'] = f'attachment; filename="informe_ventas_{fecha}.pdf"'
    buffer = BytesIO()
    p = canvas.Canvas(buffer)
    p.drawString(100, 800, f'Informe de Ventas para el {fecha}')
    p.drawString(100, 780, f'Total de Ventas: {total_ventas_fecha}')

    # tabla
    tabla = [["Id Venta", "Cliente", "Juego Alquilado", "Fecha de Venta", "Total Pagado"]]
    for venta in ventas_en_fecha:
        # Truncar nombre
        nombre_juego = (venta.alquiler.juego.nombre[:15] + '...') if len(venta.alquiler.juego.nombre) > 15 else venta.alquiler.juego.nombre
        tabla.append([venta.id, venta.alquiler.cliente.nombre, nombre_juego, venta.fecha, venta.monto_total])
    width = [50, 80, 110, 90, 90]  # Anchos de las columnas
    height = 20
    for row_index, row in enumerate(tabla):
        for col_index, (value, col_width) in enumerate(zip(row, width)):
            p.drawString(100 + sum(width[:col_index]), 780 - height * (row_index + 2), str(value)[:col_width])
    p.showPage()
    p.save()
    buffer.seek(0)
    response.write(buffer.getvalue())
    buffer.close()

    return response

def juegos_alquilados_por_clientes(request):
    if 'cliente_busqueda' in request.GET:
        cliente_busqueda = request.GET['cliente_busqueda']
        clientes = Cliente.objects.filter(nombre__icontains=cliente_busqueda)
    else:
        clientes = Cliente.objects.all()

    edad_min = request.GET.get('edad_min', None)
    edad_max = request.GET.get('edad_max', None)
    ordenar_clientes = request.GET.get('ordenar_clientes', None)
    juegos_frecuencia = Juego.objects.annotate(num_alquileres=Count('alquiler'))
    if edad_min and edad_max:
        clientes = clientes.filter(edad__gte=edad_min, edad__lte=edad_max)
        if ordenar_clientes:
            order_by_field = 'num_alquileres' if ordenar_clientes == 'desc' else '-num_alquileres'
            clientes = clientes.annotate(num_alquileres=Count('alquiler')).order_by(order_by_field)

    juegos_por_cliente = {}
    for cliente in clientes:
        alquileres = Alquiler.objects.filter(cliente=cliente)
        juegos_alquilados = [alquiler.juego for alquiler in alquileres]
        juegos_por_cliente[cliente] = {'edad': cliente.edad, 'juegos_alquilados': juegos_alquilados}

    return render(request, 'juegos_alquilados_por_clientes.html', {'juegos_por_cliente': juegos_por_cliente, 'juegos_frecuencia': juegos_frecuencia})

def consultar_balance_cliente(request):
    if request.method == 'POST':
        email_cliente = request.POST.get('email_cliente')
        
        # Verificar si el cliente existe
        cliente = Cliente.objects.filter(email=email_cliente).first()
        
        if not cliente:
            return render(request, 'consulta_balance.html', {'cliente_no_existe': True})
        
        # Obtener todos los alquileres del cliente
        alquileres = Alquiler.objects.filter(cliente=cliente)
        
        # Crear una lista para almacenar la información de alquiler
        datos_alquiler = []
        
        for alquiler in alquileres:
            # Obtener las fechas de devolución
            fecha_devolucion = alquiler.fecha_devolucion.strftime('%Y-%m-%d') if alquiler.fecha_devolucion else "N/A"
            fecha_alquiler = alquiler.fecha_alquiler.strftime('%Y-%m-%d') if alquiler.fecha_alquiler else "N/A"
            
            # Agregar información a la lista
            datos_alquiler.append({
                'fecha_alquiler': fecha_alquiler,
                'fecha_devolucion': fecha_devolucion,
                'nombre_juego': alquiler.juego.nombre,
            })
        
        return render(request, 'consulta_balance.html', {'cliente': cliente, 'datos_alquiler': datos_alquiler})
    
    return render(request, 'consulta_balance.html')









    
    