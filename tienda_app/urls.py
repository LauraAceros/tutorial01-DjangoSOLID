from django.urls import path
from .views import CompraView, compra_rapida_fbv

urlpatterns = [
    path('compra/<int:libro_id>/', CompraView.as_view(), name='finalizar_compra'),
    # PASO 1: URL de la vista FBV spaghetti
    path('compra-rapida/<int:libro_id>/', compra_rapida_fbv, name='compra_rapida'),
]