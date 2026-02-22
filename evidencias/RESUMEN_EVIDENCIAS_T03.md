\#  Resumen de Evidencias - Tutorial 03: API REST



\*\*Estudiante:\*\* Laura Sofía Aceros  

\*\*Email:\*\* lsacerosm@eafit.edu.co  

\*\*Fecha:\*\* Febrero 2026



---



\##  Evidencias Entregadas



\### 1. Endpoint API POST /api/v1/comprar/ (Paso 3)



\*\*Archivo:\*\* `evidencia\_api\_post\_exitoso.jpeg`



\*\*Qué demuestra:\*\*

\- Interfaz web de Django Rest Framework mostrando el endpoint

\- Request JSON con `libro\_id: 0` y `direccion\_envio: "Cra 49 #7 Sur-50, Envigado"`

\- Response HTTP 201 Created con la orden creada exitosamente

\- Datos retornados: `estado: "exito"`, `orden\_id: 1`, `total: 184.45`



\*\*Conclusión:\*\* El endpoint API funciona correctamente y retorna JSON válido usando DRF.



---



\### 2. Log de Transacción por API (Paso 3)



\*\*Archivo:\*\* `evidencia\_api\_log.jpeg`



\*\*Qué demuestra:\*\*

\- Archivo `pagos\_locales\_LAURA\_SOFIA\_ACEROS.log` mostrando múltiples transacciones

\- La transacción más reciente `\[2026-02-22 01:18:11.896137]` corresponde a la compra vía API

\- Mismo formato de log que las vistas HTML



\*\*Conclusión:\*\* La API y las vistas HTML escriben en el \*\*mismo log\*\* porque usan el \*\*mismo Service Layer\*\* y el \*\*mismo gateway de pago\*\* (BancoNacionalProcesador).



---



\##  Demostración de Reutilización



\*\*Arquitectura probada:\*\*

```

┌─────────────┐       ┌─────────────┐

│ Vista HTML  │       │  API REST   │

│ CompraView  │       │CompraAPIView│

└──────┬──────┘       └──────┬──────┘

&nbsp;      │                     │

&nbsp;      └──────┬──────────────┘

&nbsp;             │

&nbsp;      ┌──────▼──────────┐

&nbsp;      │  CompraService  │ ◄── CAPA COMPARTIDA

&nbsp;      └──────┬──────────┘

&nbsp;             │

&nbsp;      ┌──────▼──────────┐

&nbsp;      │ BancoNacional   │

&nbsp;      │  Procesador     │

&nbsp;      └─────────────────┘

&nbsp;             │

&nbsp;      ┌──────▼──────────┐

&nbsp;      │  Log + DB       │

&nbsp;      └─────────────────┘

```



\*\*Resultado:\*\*

\- 1 servicio → 2 interfaces (HTML + JSON)

\- 1 log compartido → mismas transacciones

\- 1 inventario → descuento compartido

\- Zero duplicación de lógica



---



\##  Archivos de Código Entregados



\### api/serializers.py

\- `LibroSerializer`: Convierte modelo Libro a JSON

\- `OrdenInputSerializer`: Valida entrada JSON (DTO pattern)



\### api/views.py

\- `CompraAPIView`: Endpoint POST que reutiliza `CompraService.ejecutar\_compra\_personalizada()`

\- Manejo de errores: 400 (validación), 409 (sin stock), 500 (error interno)



\### urls.py

\- Nueva ruta: `path('api/v1/comprar/', CompraAPIView.as\_view())`



---



\##  Cumplimiento de Requisitos



| Requisito | Estado | Evidencia |

|:----------|:-------|:----------|

| Instalar Django Rest Framework | ok | `settings.py` actualizado con `'rest\_framework'` |

| Crear serializers (Adapter Pattern) | ok | `api/serializers.py` |

| Endpoint POST /api/v1/comprar/ | ok | `api/views.py` |

| Reutilización del Service Layer | ok | CompraAPIView llama a `CompraService` sin duplicar lógica |

| Log compartido HTML/API | ok | `evidencia\_api\_log.jpeg` |

| Screenshot de POST exitoso | ok | `evidencia\_api\_post\_exitoso.jpeg` |



---



\##  Ubicación en GitHub



\*\*Repositorio:\*\* https://github.com/LauraAceros/tutorial01-DjangoSOLID



\*\*Ramas del Tutorial 03:\*\*

\- `tutorial03-paso1-instalacion`

\- `tutorial03-paso2-serializers`

\- `tutorial03-paso3-apiviews`

\- `tutorial03-paso4-evidencia` (actual)



\*\*Carpeta de evidencias:\*\* `/evidencias/`



---



\*\*Laura Sofía Aceros\*\* - Tutorial 03 Completado

