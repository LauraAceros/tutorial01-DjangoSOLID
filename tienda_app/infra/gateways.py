import datetime
from ..domain.interfaces import ProcesadorPago

class BancoNacionalProcesador(ProcesadorPago):
    """
    Implementacion concreta de la infraestructura.
    Simula un banco local escribiendo en un log.
    """
    def pagar(self, monto: float) -> bool:
        # Nombre del archivo con identidad del estudiante (evidencia de entrega)
        archivo_log = "pagos_locales_LAURA_SOFIA_ACEROS.log"
        with open(archivo_log, "a") as f:
            f.write(f"[{datetime.datetime.now()}] Transaccion exitosa por: ${monto}\n")
        return True