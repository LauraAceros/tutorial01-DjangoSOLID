from django.shortcuts import get_object_or_404
from .models import Libro, Inventario, Orden
from .domain.logic import CalculadorImpuestos
from .domain.builders import OrdenBuilder


class CompraService:
    """
    SERVICE LAYER: Orquesta la interacción entre el dominio, 
    la infraestructura y la base de datos.
    """
    def __init__(self, procesador_pago):
        # Inyectamos la dependencia (DIP)
        self.procesador_pago = procesador_pago
        self.builder = OrdenBuilder()  # inicializamos el builder

    def obtener_detalle_producto(self, libro_id):
        libro = get_object_or_404(Libro, id=libro_id)
        total = CalculadorImpuestos.obtener_total_con_iva(libro.precio)
        return {"libro": libro, "total": total}

    def ejecutar_compra(self, libro_id, cantidad):
        # 1. Obtener datos
        libro = get_object_or_404(Libro, id=libro_id)
        inv = get_object_or_404(Inventario, libro=libro)

        # 2. Validar Reglas de Negocio
        if inv.cantidad < cantidad:
            raise ValueError("No hay suficiente stock para completar la compra.")

        total = CalculadorImpuestos.obtener_total_con_iva(libro.precio)

        # 3. Procesar Infraestructura (Pago)
        pago_exitoso = self.procesador_pago.pagar(total)
        
        if not pago_exitoso:
            raise Exception("La transacción fue rechazada por el banco.")

        # 4. Persistencia usando el Builder
        inv.cantidad -= cantidad
        inv.save()
        
        # Uso del Builder: construcción semántica y validada
        orden = (self.builder
                 .con_usuario("Laura Sofia Aceros")  # usuario por defecto
                 .con_libro(libro)
                 .para_envio("Dirección no especificada")
                 .build())
        
        return total
    
    def ejecutar_compra_personalizada(self, libro_id, cantidad, usuario, direccion):
        """
        Versión del flujo de compra que permite personalizar usuario y dirección.
        Demuestra la flexibilidad del Builder Pattern.
        """
        # 1. Obtener datos
        libro = get_object_or_404(Libro, id=libro_id)
        inv = get_object_or_404(Inventario, libro=libro)

        # 2. Validar stock
        if inv.cantidad < cantidad:
            raise ValueError("No hay suficiente stock para completar la compra.")

        total = CalculadorImpuestos.obtener_total_con_iva(libro.precio)

        # 3. Procesar pago
        pago_exitoso = self.procesador_pago.pagar(total)
        
        if not pago_exitoso:
            raise Exception("La transacción fue rechazada por el banco.")

        # 4. Actualizar inventario
        inv.cantidad -= cantidad
        inv.save()
        
        # 5. Construcción de orden con datos personalizados usando Builder
        orden = (self.builder
                 .con_usuario(usuario)
                 .con_libro(libro)
                 .para_envio(direccion)
                 .build())
        
        return orden