#  Django Clean Monolith: De Spaghetti a Grado Empresarial

**Estudiante:** Laura Sofía Aceros (lsacerosm@eafit.edu.co)  
**Repositorio:** [tutorial01-DjangoSOLID](https://github.com/LauraAceros/tutorial01-DjangoSOLID)  
**Curso:** TEIS / AdS 2026 - Prof. Nicolás Ramírez Vélez

Este proyecto es una guía práctica paso a paso para transformar una aplicación Django tradicional en un sistema con arquitectura de capas, siguiendo principios SOLID, patrones de diseño empresariales y arquitectura de APIs REST.

---

##  Tutoriales Completados

### Tutorial 01: Fundamentos SOLID y Service Layer
Transformación progresiva desde código spaghetti hasta arquitectura limpia con separación de capas.

### Tutorial 02: Patrones Creacionales
Implementación de Factory Method y Builder Pattern para desacoplar infraestructura y simplificar construcción de objetos complejos.

### Tutorial 03: API REST con Django Rest Framework
Creación de endpoints JSON que **reutilizan** el Service Layer existente, demostrando que la lógica de negocio sirve tanto a vistas HTML como a clientes API.

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

### Tutorial 03: API REST con DRF

| Rama | Descripción |
| :--- | :--- |
| `tutorial03-paso1-instalacion` | Instalación de Django Rest Framework y configuración en settings |
| `tutorial03-paso2-serializers` | Serializers (Adaptadores) para convertir modelos a JSON |
| `tutorial03-paso3-apiviews` | Endpoint POST `/api/v1/comprar/` reutilizando CompraService |
| `tutorial03-paso4-evidencia` | Screenshots de Postman/DRF + log + README actualizado |

---

##  Arquitectura Final

La arquitectura separa responsabilidades en 5 capas distintas y expone dos interfaces (HTML y JSON):

| Capa | Ubicación | Responsabilidad |
| :--- | :--- | :--- |
| **Presentación HTML** | `views.py` | Vistas tradicionales que renderizan templates |
| **Presentación API** | `api/views.py` | Endpoints REST que retornan JSON |
| **Servicio** | `services.py` | **Capa compartida** que orquesta toda la lógica de negocio |
| **Dominio** | `domain/` | Lógica pura (`CalculadorImpuestos`, `OrdenBuilder`) e interfaces (`ProcesadorPago`) |
| **Infraestructura** | `infra/` | Implementaciones técnicas: procesadores de pago, fábricas |
| **Datos** | `models.py` | Modelos ORM: `Libro`, `Inventario`, `Orden` |

**Diagrama conceptual:**
```
┌─────────────┐       ┌─────────────┐
│ Vista HTML  │       │  API REST   │
│ (Browser)   │       │  (JSON)     │
└──────┬──────┘       └──────┬──────┘
       │                     │
       └──────┬──────────────┘
              │
       ┌──────▼──────┐
       │   Service   │ ◄── Capa compartida
       │    Layer    │
       └──────┬──────┘
              │
    ┌─────────┼─────────┐
    │         │         │
┌───▼───┐ ┌──▼───┐ ┌──▼────┐
│Domain │ │Infra │ │ Data  │
└───────┘ └──────┘ └───────┘
```

---

##  Principios SOLID Aplicados

**S - Single Responsibility:** Cada clase tiene una única razón para cambiar. `CalculadorImpuestos` solo calcula IVA, `OrdenBuilder` solo construye órdenes, `CompraAPIView` solo valida JSON y delega al servicio.

**O - Open/Closed:** Abierto a extensión, cerrado a modificación. Nuevos procesadores de pago se agregan sin tocar el servicio. Nuevos endpoints (GraphQL, gRPC) pueden agregarse sin cambiar la lógica de negocio.

**L - Liskov Substitution:** `MockPaymentProcessor` y `BancoNacionalProcesador` son intercambiables sin romper el código.

**I - Interface Segregation:** `ProcesadorPago` define solo el método `pagar()`, nada más.

**D - Dependency Inversion:** `CompraService` depende de la abstracción `ProcesadorPago`, no de implementaciones concretas. La fábrica inyecta la dependencia. Las vistas (HTML y API) dependen del servicio, no de los detalles de infraestructura.

---

##  Patrones de Diseño Implementados

### 1. Service Layer Pattern
`CompraService` orquesta toda la lógica de negocio. **Las vistas HTML y la API REST comparten este servicio.**

### 2. Factory Method Pattern
`PaymentFactory.get_processor()` decide qué procesador usar según `PAYMENT_PROVIDER`:
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

### 4. Adapter Pattern (Serializers)
Los serializers de DRF convierten modelos Django a JSON y viceversa:
```python
class OrdenInputSerializer(serializers.Serializer):
    libro_id = serializers.IntegerField()
    direccion_envio = serializers.CharField(max_length=200)
```

### 5. Dependency Injection
El servicio recibe dependencias por constructor, permitiendo testing y flexibilidad.

### 6. Strategy Pattern
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
pip install django djangorestframework markdown django-filter
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

**Rutas disponibles:**
- Vista HTML: `http://127.0.0.1:8000/compra-rapida/0/`
- API REST: `http://127.0.0.1:8000/api/v1/comprar/`

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

---

##  Uso de la API REST

### Endpoint: POST /api/v1/comprar/

**Request:**
```bash
curl -X POST http://127.0.0.1:8000/api/v1/comprar/ \
  -H "Content-Type: application/json" \
  -d '{"libro_id": 0, "direccion_envio": "Cra 49 #7 Sur-50, Envigado"}'
```

**Response exitosa (201 Created):**
```json
{
    "estado": "exito",
    "mensaje": "Orden 1 creada exitosamente",
    "orden_id": 1,
    "total": 184.45
}
```

**Error sin stock (409 Conflict):**
```json
{
    "error": "No hay suficiente stock para completar la compra."
}
```

**Validación fallida (400 Bad Request):**
```json
{
    "libro_id": ["Este campo es requerido."]
}
```

### Interfaz Web de DRF

Podés probar la API directamente desde el navegador:
```
http://127.0.0.1:8000/api/v1/comprar/
```

DRF muestra una interfaz donde podés hacer el POST con un formulario.

---

##  Estructura de Archivos
```
tienda_app/
├── api/
│   ├── __init__.py
│   ├── serializers.py    # Adaptadores JSON (LibroSerializer, OrdenInputSerializer)
│   └── views.py          # CompraAPIView (endpoint REST)
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
├── services.py           # CompraService (orquestación compartida)
├── views.py              # CompraView, CompraRapidaView, compra_rapida_fbv
└── urls.py               # Rutas HTML + API
```

---

##  Evidencias de Entrega

### Tutorial 01
- **Archivo:** `pagos_locales_LAURA_SOFIA_ACEROS.log` (rama `paso4-evidencia`)
- **Contenido:** 3 transacciones registradas por `BancoNacionalProcesador`

### Tutorial 02
- **Carpeta:** `evidencias/`
  - `evidencia_paso1_factory.jpeg` - Screenshot Factory Method con MOCK activo
  - `evidencia_paso2.jpeg` - Screenshot Builder creando orden con usuario y dirección
  - `reflexion_builder.md` - Análisis del Builder Pattern
  - `RESUMEN_EVIDENCIAS.md` - Resumen completo Tutorial 02

### Tutorial 03
- **Carpeta:** `evidencias/`
  - `evidencia_api_post_exitoso.jpeg` - Screenshot de DRF mostrando POST 201 Created
  - `evidencia_api_log.jpeg` - Screenshot del log con transacción de la API
- **Archivo:** `pagos_locales_LAURA_SOFIA_ACEROS.log` - Log compartido entre HTML y API

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

### Tutorial 03 — API REST + Reutilización
- **Mismo Service Layer** para HTML y JSON
- Vista HTML y API REST comparten inventario y logs
- Zero duplicación de lógica de negocio

---

##  Ventajas de la Arquitectura Final

 **Testeable:** Cada capa se prueba independientemente  
 **Mantenible:** Cambios localizados, sin efecto dominó  
 **Escalable:** Nuevos procesadores/reglas/endpoints se agregan sin refactoring  
 **Docker-Ready:** Configuración por variables de entorno  
 **API-First:** Backend headless reutilizable para web, móvil, integraciones  
 **Legible:** Código autodocumentado con responsabilidades claras  
 **Zero Duplicación:** HTML y API comparten el 100% de la lógica de negocio  

---

**Laura Sofía Aceros**  
Systems Engineering Student - Universidad EAFIT  
TEIS / AdS 2026
