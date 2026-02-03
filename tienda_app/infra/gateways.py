import datetime
from ..domain.interfaces import ProcesadorPago


# Implementación concreta del gateway de pagos.
# En producción esto hablaría con un banco real por API,
# acá lo simulamos escribiendo en un archivo de log.
class BancoNacionalProcesador(ProcesadorPago):

    def pagar(self, monto: float) -> bool:
        archivo_log = "pagos_locales_LAURA_SOFIA_ACEROS.log"  # evidencia de entrega del estudiante
        with open(archivo_log, "a") as f:
            f.write(f"[{datetime.datetime.now()}] Transaccion exitosa por: ${monto}\n")
        return True  # en una versión real, retornaría False si el banco rechazara el pago
