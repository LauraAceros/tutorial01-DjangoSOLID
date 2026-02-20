from ..models import Orden, Libro
from .logic import CalculadorImpuestos


# Builder para ensamblar una Orden paso a paso con validaciones incluidas.
# Evita constructores gigantes y centraliza la lógica de cálculo de totales.
class OrdenBuilder:
    
    def __init__(self):
        self.reset()
    
    def reset(self):
        """Limpia el estado interno para construir una nueva orden"""
        self._usuario = None
        self._libro = None
        self._direccion = ""
    
    def con_usuario(self, usuario):
        """Define quién hace la compra"""
        self._usuario = usuario
        return self  # permite encadenar métodos
    
    def con_libro(self, libro):
        """Define qué libro se está comprando"""
        self._libro = libro
        return self
    
    def para_envio(self, direccion):
        """Define dónde se envía la orden"""
        self._direccion = direccion
        return self
    
    def build(self) -> Orden:
        """Ensambla la orden final con todas las validaciones y cálculos"""
        if not self._usuario or not self._libro:
            raise ValueError("Datos insuficientes: se requiere usuario y libro.")
        
        # Calcula el total usando la lógica del dominio
        calculadora = CalculadorImpuestos()
        total_con_iva = calculadora.obtener_total_con_iva(float(self._libro.precio))
        
        # Crea la orden en la base de datos
        orden = Orden.objects.create(
            usuario=self._usuario,
            libro=self._libro,
            total=total_con_iva,
            direccion_envio=self._direccion
        )
        
        self.reset()  # limpia para la próxima construcción
        return orden