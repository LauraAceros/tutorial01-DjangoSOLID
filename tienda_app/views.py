import datetime
from django.views import View
from django.shortcuts import render, get_object_or_404
from django.http import HttpResponse
from .models import Libro, Inventario, Orden
from .services import CompraService
from .infra.gateways import BancoNacionalProcesador


# ============================================================
# VISTA ORIGINAL DEL REPO BASE (arquitectura limpia)
# ============================================================
class CompraView(View):
    """
    CBV: Vista Basada en Clases.
    Actua como un "Portero": recibe la peticion y delega al servicio.
    """
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


# ============================================================
# PASO 1: FBV Spaghetti - "Compra Rapida"
# Esta funcion tiene TODAS las responsabilidades mezcladas.
# Los comentarios senalan cada violacion SOLID.
# ============================================================
def compra_rapida_fbv(request, libro_id):
    libro = get_object_or_404(Libro, id=libro_id)

    if request.method == 'POST':
        # VIOLACION SRP: Logica de inventario en la vista
        inventario = Inventario.objects.get(libro=libro)
        if inventario.cantidad > 0:
            # VIOLACION OCP: Calculo de negocio hardcoded
            total = float(libro.precio) * 1.19

            # VIOLACION DIP: Proceso de pago acoplado al filesystem
            with open("pagos_manuales.log", "a") as f:
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