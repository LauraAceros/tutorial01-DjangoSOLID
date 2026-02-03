#  Django Clean Monolith: De Spaghetti a Grado Empresarial

**Estudiante:** Laura Sofía Aceros (lsacerosm@eafit.edu.co)
**Repositorio:** [tutorial01-DjangoSOLID](https://github.com/LauraAceros/tutorial01-DjangoSOLID)

---

##  Progresión del Tutorial por Ramas

Cada rama representa una etapa del refactoring. Así se puede ver la evolución del código desde el peor escenario hasta la versión final limpia.

| Rama | Qué se hizo |
| :--- | :--- |
| `master` | Repo base del profesor con la arquitectura limpia ya implementada (`CompraView`, `CompraService`, etc.) |
| `paso1-fbv-spaghetti` | Se agregó una función `compra_rapida_fbv` con violaciones SOLID intencionales: SRP, OCP y DIP rotas en una sola función. |
| `paso2-cbv-migracion` | Se migró esa misma lógica spaghetti a una `CompraRapidaView` (CBV). El GET y POST ya están separados, pero las violaciones siguen ahí. |
| `paso3-service-layer` | La `CompraRapidaView` se conectó al `CompraService` existente. La vista dejó de saber sobre inventario, impuestos y pagos. El gateway escribe en el log con nombre de la estudiante. |
| `paso4-evidencia` | Se subió el archivo de log `pagos_locales_LAURA_SOFIA_ACEROS.log` con las 3 transacciones como evidencia de entrega. |

---

##  Evidencia de Entrega

El archivo de evidencia se encuentra en la rama `paso4-evidencia`:

**Archivo:** `pagos_locales_LAURA_SOFIA_ACEROS.log`
```
[2026-02-02 18:43:17.496419] Transaccion exitosa por: $157.07999999999998
[2026-02-02 18:43:22.043897] Transaccion exitosa por: $157.07999999999998
[2026-02-02 18:44:21.590395] Transaccion exitosa por: $178.5
```

