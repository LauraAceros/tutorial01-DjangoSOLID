from django.urls import path
from .views import CompraView, compra_rapida_fbv, CompraRapidaView

urlpatterns = [
    path('compra/<int:libro_id>/', CompraView.as_view(), name='finalizar_compra'),
    # PASO 1: FBV spaghetti (se mantiene como referencia)
    path('compra-rapida-fbv/<int:libro_id>/', compra_rapida_fbv, name='compra_rapida_fbv'),
    # PASO 2: CBV - misma logica, mejor estructura
    path('compra-rapida/<int:libro_id>/', CompraRapidaView.as_view(), name='compra_rapida'),
]
