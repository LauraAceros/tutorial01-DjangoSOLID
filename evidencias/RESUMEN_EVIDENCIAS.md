# Resumen de Evidencias - Tutorial 02

**Estudiante:** Laura Sofía Aceros  
**Email:** lsacerosm@eafit.edu.co  
**Fecha:** Febrero 2026

---

##  Evidencias Entregadas

### 1. Factory Method Pattern (Paso 1)

**Archivo:** `evidencia_paso1_factory.jpeg`

**Qué demuestra:**
- Ejecución del servidor con variable de entorno `PAYMENT_PROVIDER=MOCK`
- Mensaje en consola: `[DEBUG FACTORY] Variable leída: 'MOCK'`
- Mensaje en consola: `[DEBUG] Mock Payment: Procesando pago de $184.45 sin cargo real.`

**Conclusión:** El Factory Method permite cambiar el procesador de pago sin modificar código, solo ajustando la variable de entorno.

---

### 2. Builder Pattern (Paso 2)

**Archivo:** `evidencia_paso2.jpeg`

**Qué demuestra:**
- Consulta en Django shell mostrando orden creada con el Builder
- Campos poblados: `Usuario: Laura Sofia Aceros`, `Dirección: Dirección no especificada`
- Total calculado automáticamente: `$184.45`

**Conclusión:** El Builder centraliza validaciones y cálculos, eliminando la posibilidad de crear órdenes incompletas o con totales incorrectos.

---

### 3. Reflexión Técnica (Paso 3)

**Archivo:** `reflexion_builder.md`

**Contenido:**
- Análisis de 3 ventajas del Builder vs construcción directa
- Validación centralizada
- Separación de responsabilidades
- Interfaz fluida y legible

**Conclusión:** El Builder actúa como "guardia" que garantiza órdenes válidas, quitando esa responsabilidad de la capa de presentación.

---

##  Archivos de Código Entregados

### infra/factories.py
- `PaymentFactory`: Fábrica que lee `PAYMENT_PROVIDER` del entorno
- `MockPaymentProcessor`: Implementación para pruebas sin cargo real

### domain/builders.py
- `OrdenBuilder`: Constructor fluido con validaciones y cálculo de IVA integrado

### services.py
- `ejecutar_compra()`: Usa Builder con valores por defecto
- `ejecutar_compra_personalizada()`: Usa Builder con parámetros dinámicos

---

## 🎯 Cumplimiento de Requisitos

| Requisito | Estado | Evidencia |
|:----------|:-------|:----------|
| Captura de consola con `[DEBUG] Mock Payment...` |ok | `evidencia_paso1_factory.jpeg` |
| Código fuente de `infra/factories.py` |ok | Rama `tutorial02-paso1-factory` |
| Código fuente de `domain/builders.py` |ok | Rama `tutorial02-paso2-builder` |
| Reflexión sobre Builder Pattern |ok  | `reflexion_builder.md` |

---

## Ubicación en GitHub

**Repositorio:** https://github.com/LauraAceros/tutorial01-DjangoSOLID

**Ramas del Tutorial 02:**
- `tutorial02-paso1-factory`
- `tutorial02-paso2-builder`
- `tutorial02-paso3-integracion`
- `tutorial02-paso4-evidencia` (actual)

**Carpeta de evidencias:** `/evidencias/`

---

**Laura Sofía Aceros** - Tutorial 02 Completado