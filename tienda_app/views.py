import datetime
from django.views import View
from django.shortcuts import render, get_object_or_404
from django.http import HttpResponse
from .models import Libro, Inventario, Orden
from .services import CompraService
from .infra.gateways import BancoNacionalProcesador


# Vista que venía en el repo original del profesor.
# Su trabajo es simple: recibir la petición y pasarla al servicio.
class CompraView(View):
    template_name = 'tienda_app/compra.html'

    def setup_service(self):
        gateway = BancoNacionalProcesador()
        return CompraService(procesador_pago=gateway)

    def get(self, request, libro_id):
        servicio = self.setup_service()
        contexto = servicio.obtener_detalle_producto(libro_id)
        return render(request, self.template_name, contexto)

    def post(self, request, libro_id):
        servicio = self.setup_service()
        try:
            total = servicio.ejecutar_compra(libro_id, cantidad=1)
            return render(request, self.template_name, {
                'mensaje_exito': f"Gracias por su compra! Total: ${total}",
                'total': total
            })
        except (ValueError, Exception) as e:
            return render(request, self.template_name, {
                'error': str(e)
            }, status=400)


# Paso 1: ejemplo de "cómo no hacer las cosas".
# Todo el peso cae acá: inventario, impuestos, escritura al log...
# La dejamos como referencia para comparar con la versión refactorizada.
def compra_rapida_fbv(request, libro_id):
    libro = get_object_or_404(Libro, id=libro_id)

    if request.method == 'POST':
        inventario = Inventario.objects.get(libro=libro)  # stock manejado acá, viola SRP
        if inventario.cantidad > 0:
            total = float(libro.precio) * 1.19  # IVA hardcodeado, viola OCP
            with open("pagos_manuales.log", "a") as f:  # escribe al archivo directamente, viola DIP
                f.write(f"[{datetime.datetime.now()}] Pago FBV: ${total}\n")
            inventario.cantidad -= 1
            inventario.save()
            Orden.objects.create(libro=libro, total=total)
            return HttpResponse(f"Compra exitosa: {libro.titulo}")
        else:
            return HttpResponse("Sin stock", status=400)

    total_estimado = float(libro.precio) * 1.19
    return render(request, 'tienda_app/compra_rapida.html', {
        'libro': libro,
        'total': total_estimado
    })


# Paso 2: mismo spaghetti de arriba, pero ahora como clase.
# El GET y el POST ya están separados, eso es un avance,
# pero la lógica de negocio sigue acá adentro sin cambios.
class CompraRapidaView(View):
    template_name = 'tienda_app/compra_rapida.html'

    def get(self, request, libro_id):
        libro = get_object_or_404(Libro, id=libro_id)
        total = float(libro.precio) * 1.19  # IVA hardcodeado, viola OCP
        return render(request, self.template_name, {
            'libro': libro,
            'total': total
        })

    def post(self, request, libro_id):
        libro = get_object_or_404(Libro, id=libro_id)
        inv = Inventario.objects.get(libro=libro)  # stock manejado acá, viola SRP
        if inv.cantidad > 0:
            total = float(libro.precio) * 1.19  # IVA hardcodeado, viola OCP
            with open("pagos_manuales.log", "a") as f:  # escribe al archivo directamente, viola DIP
                f.write(f"[{datetime.datetime.now()}] Pago CBV: ${total}\n")
            inv.cantidad -= 1
            inv.save()
            Orden.objects.create(libro=libro, total=total)
            return HttpResponse(f"Compra exitosa va CBV: {libro.titulo}")
        return HttpResponse("Sin stock", status=400)
