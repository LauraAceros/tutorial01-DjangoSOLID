# Reflexión: Builder Pattern en la Construcción de Órdenes

El patrón Builder reduce significativamente el riesgo de errores en comparación con crear la orden directamente en la vista por tres razones fundamentales:

## 1. Validación centralizada

El Builder concentra todas las validaciones (usuario requerido, libro requerido) en un solo lugar. Si intentáramos crear la orden directamente con `Orden.objects.create()` desde la vista, cada desarrollador tendría que recordar validar manualmente estos campos, lo cual es propenso a olvidos.

## 2. Separación de responsabilidades

La vista ya no necesita saber cómo se calcula el total con IVA ni qué campos son obligatorios para una orden válida. Solo usa el Builder como una interfaz limpia. Esto cumple con el principio de Single Responsibility: la vista orquesta, el Builder construye.

## 3. Interfaz fluida y legible

El código `builder.con_usuario(X).con_libro(Y).para_envio(Z).build()` es autoexplicativo y previene errores de orden de parámetros. Si usáramos un constructor tradicional como `Orden(usuario=X, libro=Y, direccion=Z, total=?)`, el orden de los parámetros podría confundirse, y olvidar calcular el total correctamente es un error común.

---

**Conclusión:** El Builder actúa como un "guardia" que garantiza que solo se creen órdenes válidas, eliminando toda esa responsabilidad de la capa de presentación.

---

**Laura Sofía Aceros** - Tutorial 02 Django SOLID