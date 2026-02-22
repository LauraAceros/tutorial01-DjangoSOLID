from rest_framework import serializers
from tienda_app.models import Libro, Orden


# Serializer para convertir el modelo Libro a JSON
class LibroSerializer(serializers.ModelSerializer):
    class Meta:
        model = Libro
        fields = ['id', 'titulo', 'precio']


# Serializer para validar la entrada cuando se hace una compra vía API
# Actúa como DTO (Data Transfer Object) - no está ligado a un modelo
class OrdenInputSerializer(serializers.Serializer):
    libro_id = serializers.IntegerField()
    direccion_envio = serializers.CharField(max_length=200)
    
    # Validación extra: el libro_id debe ser positivo
    def validate_libro_id(self, value):
        if value < 0:
            raise serializers.ValidationError("El ID del libro debe ser un número positivo.")
        return value