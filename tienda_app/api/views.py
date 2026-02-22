from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import status
from .serializers import OrdenInputSerializer
from tienda_app.services import CompraService
from tienda_app.infra.factories import PaymentFactory


# API endpoint para procesar compras vía JSON
# POST /api/v1/comprar/
# Payload: { "libro_id": 1, "direccion_envio": "Calle 123" }
class CompraAPIView(APIView):
    
    def post(self, request):
        # 1. Validar datos de entrada usando el serializer (Adapter Pattern)
        serializer = OrdenInputSerializer(data=request.data)
        if not serializer.is_valid():
            return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
        
        datos = serializer.validated_data
        
        try:
            # 2. Inyección de dependencias (Factory Pattern)
            gateway = PaymentFactory.get_processor()
            
            # 3. REUTILIZACIÓN del Service Layer existente
            # La vista HTML y la API usan el MISMO servicio
            servicio = CompraService(procesador_pago=gateway)
            
            # Llamamos al método personalizado que creamos en Tutorial 02
            orden = servicio.ejecutar_compra_personalizada(
                libro_id=datos['libro_id'],
                cantidad=1,
                usuario="Laura Sofia Aceros",  # En producción vendría de request.user
                direccion=datos['direccion_envio']
            )
            
            return Response({
                "estado": "exito",
                "mensaje": f"Orden {orden.id} creada exitosamente",
                "orden_id": orden.id,
                "total": float(orden.total)
            }, status=status.HTTP_201_CREATED)
            
        except ValueError as e:
            # Errores de negocio (ej: sin stock)
            return Response(
                {"error": str(e)},
                status=status.HTTP_409_CONFLICT
            )
        except Exception as e:
            # Errores inesperados
            return Response(
                {"error": "Error interno del servidor"},
                status=status.HTTP_500_INTERNAL_SERVER_ERROR
            )