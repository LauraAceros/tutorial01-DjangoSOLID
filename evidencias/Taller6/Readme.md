# Tutorial 06: El Primer Estrangulamiento (Strangler Pattern)

En este taller se implementó con éxito la migración parcial de una funcionalidad del monolito hacia un microservicio independiente, siguiendo el **Patrón de Estrangulamiento**.

## Implementación
* [cite_start]**Capa Legacy (v1):** Se mantiene el servicio de Django para rutas previas en `/api/v1/`[cite: 121].
* [cite_start]**Capa Nueva (v2):** Se extrajo la lógica de compras a un microservicio en **Flask** que responde en `/api/v2/comprar`[cite: 24, 126].
* [cite_start]**Proxy Inverso:** Nginx actúa como fachada (Facade) para redirigir el tráfico según la versión de la API[cite: 102, 103].

## Evidencias de Validación
1. **Coexistencia v1:** Acceso exitoso a Django a través del Proxy.
2. [cite_start]**Estrangulamiento v2:** El microservicio Flask procesa peticiones de compra de forma independiente[cite: 144].
3. [cite_start]**Logs de Nginx:** Registro de ruteo bidireccional hacia ambos backends[cite: 145].

---
**Desarrollado por:** Laura Aceros  
**Arquitectura de Software 2026**