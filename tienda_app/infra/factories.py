import os
from .gateways import BancoNacionalProcesador


# Mock que simula un banco sin hacer transacciones reales.
# Útil para desarrollo y testing, solo imprime en consola.
class MockPaymentProcessor:
    def pagar(self, monto: float) -> bool:
        print(f"[DEBUG] Mock Payment: Procesando pago de ${monto} sin cargo real.")
        return True


# Fábrica que decide cuál procesador usar basándose en una variable de entorno.
# Si PAYMENT_PROVIDER='MOCK' → usa el mock (pruebas)
# Si PAYMENT_PROVIDER='BANCO' o no existe → usa BancoNacionalProcesador (producción)
# Ventaja: cambias el comportamiento sin tocar código, solo con una variable.
class PaymentFactory:
    
    @staticmethod
    def get_processor():
        provider = os.getenv('PAYMENT_PROVIDER', 'BANCO').strip()
        print(f"[DEBUG FACTORY] Variable leída: '{provider}'")  # debug para verificar lectura
        
        if provider == 'MOCK':
            return MockPaymentProcessor()  # modo desarrollo
        
        return BancoNacionalProcesador()  # modo producción (escribe en el log)