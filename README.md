#  Django Clean Monolith: De Spaghetti a Grado Empresarial

**Estudiante:** Laura Sofía Aceros (lsacerosm@eafit.edu.co)  
**Repositorio:** [tutorial01-DjangoSOLID](https://github.com/LauraAceros/tutorial01-DjangoSOLID)  
**Curso:** TEIS / AdS 2026 - Prof. Nicolás Ramírez Vélez

Este proyecto es una guía práctica paso a paso para transformar una aplicación Django tradicional en un sistema con arquitectura de capas, siguiendo principios SOLID y patrones de diseño empresariales.

---

##  Tutoriales Completados

### Tutorial 01: Fundamentos SOLID y Service Layer
Transformación progresiva desde código spaghetti hasta arquitectura limpia con separación de capas.

### Tutorial 02: Patrones Creacionales
Implementación de Factory Method y Builder Pattern para desacoplar infraestructura y simplificar construcción de objetos complejos.

---

##  Progresión por Ramas

### Tutorial 01: SOLID + Service Layer

| Rama | Descripción |
| :--- | :--- |
| `master` | Repo base del profesor con arquitectura limpia implementada |
| `paso1-fbv-spaghetti` | Function-Based View con violaciones SOLID intencionales (SRP, OCP, DIP) |
| `paso2-cbv-migracion` | Class-Based View manteniendo la lógica spaghetti, pero con GET/POST separados |
| `paso3-service-layer` | CBV conectada al Service Layer, eliminando lógica de negocio de la vista |
| `paso4-evidencia` | Log `pagos_locales_LAURA_SOFIA_ACEROS.log` con 3 transacciones como evidencia |

### Tutorial 02: Factory Method + Builder Pattern

| Rama | Descripción |
| :--- | :--- |
| `tutorial02-paso1-factory` | Factory Method para seleccionar procesador de pago según variable de entorno |
| `tutorial02-paso2-builder` | Builder Pattern para construcción validada de órdenes con IVA calculado |
| `tutorial02-paso3-integracion` | Método personalizado `ejecutar_compra_personalizada()` y reflexión escrita |
| `tutorial02-paso4-evidencia` | README actualizado y resumen de evidencias completo |

---

##  Arquitectura Final

La arquitectura separa responsabilidades en 5 capas distintas:

| Capa | Ubicación | Responsabilidad |
| :--- | :--- | :--- |
| **Presentación** | `views.py` | Recibir requests HTTP, delegar al servicio, retornar responses. Sin lógica de negocio. |
| **Servicio** | `services.py` | Orquestar flujo de negocio: validar stock, calcular impuestos, procesar pago, crear orden. |
| **Dominio** | `domain/` | Lógica pura (`CalculadorImpuestos`, `OrdenBuilder`) e interfaces (`ProcesadorPago`). |
| **Infraestructura** | `infra/` | Implementaciones técnicas: `BancoNacionalProcesador`, `MockPaymentProcessor`, `PaymentFactory`. |
| **Datos** | `models.py` | Modelos ORM: `Libro`, `Inventario`, `Orden`. |

---

##  Principios SOLID Aplicados

**S - Single Responsibility:** Cada clase tiene una única razón para cambiar. `CalculadorImpuestos` solo calcula IVA, `OrdenBuilder` solo construye órdenes.

**O - Open/Closed:** Abierto a extensión, cerrado a modificación. Nuevos procesadores de pago se agregan sin tocar el servicio.

**L - Liskov Substitution:** `MockPaymentProcessor` y `BancoNacionalProcesador` son intercambiables sin romper el código.

**I - Interface Segregation:** `ProcesadorPago` define solo el método `pagar()`, nada más.

**D - Dependency Inversion:** `CompraService` depende de la abstracción `ProcesadorPago`, no de implementaciones concretas. La fábrica inyecta la dependencia.

---

##  Patrones de Diseño Implementados

### 1. Service Layer Pattern
`CompraService` orquesta toda la lógica de negocio entre dominio, infraestructura y datos.

### 2. Factory Method Pattern
`PaymentFactory.get_processor()` decide qué procesador usar según la variable de entorno `PAYMENT_PROVIDER`:
- `MOCK` → `MockPaymentProcessor` (pruebas, sin cargo real)
- `BANCO` → `BancoNacionalProcesador` (producción, escribe en log)

### 3. Builder Pattern
`OrdenBuilder` construye órdenes paso a paso con validaciones centralizadas:
```python
orden = (builder
         .con_usuario("Laura Sofia Aceros")
         .con_libro(libro)
         .para_envio("Cra 49 #7 Sur-50")
         .build())
```

### 4. Dependency Injection
El servicio recibe dependencias por constructor, no las crea internamente.

### 5. Strategy Pattern
`ProcesadorPago` como interfaz permite intercambiar algoritmos de pago en tiempo de ejecución.

---

##  Instalación y Configuración

### 1. Clonar y preparar entorno
```bash
git clone https://github.com/LauraAceros/tutorial01-DjangoSOLID.git
cd tutorial01-DjangoSOLID
python -m venv venv
venv\Scripts\activate          # Windows
# source venv/bin/activate     # Linux/Mac
pip install django
```

### 2. Migraciones
```bash
python manage.py migrate
```

### 3. Crear datos de prueba
```bash
python manage.py shell
```
```python
from tienda_app.models import Libro, Inventario
l1 = Libro.objects.create(titulo="Cien años de Soledad", precio=155.0)
Inventario.objects.create(libro=l1, cantidad=10)
l2 = Libro.objects.create(titulo="Clean Code en Python", precio=150.0)
Inventario.objects.create(libro=l2, cantidad=5)
exit()
```

### 4. Ejecutar en modo producción
```bash
python manage.py runserver
```

Visitar: `http://127.0.0.1:8000/compra-rapida/0/`

### 5. Ejecutar en modo desarrollo (MOCK)

**Windows CMD:**
```cmd
set PAYMENT_PROVIDER=MOCK && python manage.py runserver
```

**Windows PowerShell:**
```powershell
$env:PAYMENT_PROVIDER="MOCK"; python manage.py runserver
```

**Linux/Mac:**
```bash
PAYMENT_PROVIDER=MOCK python manage.py runserver
```

Al realizar una compra en modo MOCK, verás en la consola:
```
[DEBUG FACTORY] Variable leída: 'MOCK'
[DEBUG] Mock Payment: Procesando pago de $184.45 sin cargo real.
```

---

##  Estructura de Archivos
```
tienda_app/
├── domain/
│   ├── logic.py          # CalculadorImpuestos (SRP: solo calcula IVA)
│   ├── interfaces.py     # ProcesadorPago (DIP: contrato de pago)
│   └── builders.py       # OrdenBuilder (construcción validada)
├── infra/
│   ├── gateways.py       # BancoNacionalProcesador (escribe log)
│   └── factories.py      # PaymentFactory (inyecta dependencias según entorno)
├── migrations/
│   ├── 0001_initial.py
│   └── 0002_orden_direccion_envio_orden_usuario.py
├── templates/
│   └── tienda_app/
│       ├── compra.html
│       └── compra_rapida.html
├── models.py             # Libro, Inventario, Orden
├── services.py           # CompraService (orquestación)
├── views.py              # CompraView, CompraRapidaView, compra_rapida_fbv
└── urls.py
```

---

## Evidencias de Entrega

### Tutorial 01
- **Archivo:** `pagos_locales_LAURA_SOFIA_ACEROS.log` (rama `paso4-evidencia`)
- **Contenido:** 3 transacciones registradas por `BancoNacionalProcesador`

### Tutorial 02
- **Carpeta:** `evidencias/`
  - `evidencia_paso1_factory.jpeg` - Screenshot de Factory Method con MOCK activo
  - `evidencia_paso2.jpeg` - Screenshot de Builder creando orden con usuario y dirección
  - `reflexion_builder.md` - Análisis del Builder Pattern

---

##  Comparación: Evolución del Código

### Paso 1 — FBV Spaghetti
Una función hace todo: stock, IVA hardcodeado, escritura directa al log, creación de orden. 3 principios SOLID violados en 15 líneas.

### Paso 2 — CBV sin refactoring
Misma lógica, pero separada en `get()` y `post()`. Estructura mejorada, violaciones intactas.

### Paso 3 — CBV + Service Layer
La vista solo llama `servicio.ejecutar_compra()`. Todo el resto (stock, impuestos, pago, orden) lo resuelve el Service Layer.

### Tutorial 02 — Factory + Builder
- Vista 100% agnóstica del procesador de pago usado
- Orden construida con validaciones automáticas
- Cambio de comportamiento sin modificar código (solo variable de entorno)

---

## Ventajas de la Arquitectura Final

 **Testeable:** Cada capa se prueba independientemente  
 **Mantenible:** Cambios localizados, sin efecto dominó  
 **Escalable:** Nuevos procesadores/reglas se agregan sin refactoring  
 **Docker-Ready:** Configuración por variables de entorno  
 **Legible:** Código autodocumentado con responsabilidades claras  

---

**Laura Sofía Aceros**  
Sistemas Engineering Student - Universidad EAFIT  
TEIS / AdS 2026