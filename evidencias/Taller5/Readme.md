# Tutorial 05: Implementación de Proxy Inverso con Nginx y Gunicorn

Este repositorio contiene la implementación de una arquitectura de producción de tres capas para una aplicación Django, aplicando el **Strangler Pattern** (Patrón de Estrangulamiento) para facilitar la transición futura de monolito a microservicios.



## Arquitectura del Sistema

En este taller se eliminó la exposición directa del servidor de desarrollo de Django (`manage.py runserver`) y se implementó una infraestructura robusta:

1.  **Capa de Presentación (Proxy Inverso):** **Nginx** recibe todas las peticiones externas en el puerto **80**. Se encarga de la seguridad, el filtrado de cabeceras y el enrutamiento.
2.  **Capa de Aplicación (Servidor WSGI):** **Gunicorn** actúa como la interfaz entre Nginx y Django, manejando múltiples procesos de trabajo (workers) para mejorar el rendimiento.
3.  **Capa de Persistencia (Base de Datos):** Una instancia de **PostgreSQL** corriendo en un contenedor aislado, comunicándose internamente con Django.

## Tecnologías Utilizadas

* **Django 5.x**: Framework web principal.
* **Gunicorn**: Servidor de aplicaciones WSGI para producción.
* **Nginx**: Servidor web y proxy inverso.
* **Docker & Docker Compose**: Orquestación de contenedores.
* **PostgreSQL**: Sistema de gestión de base de datos relacional.

## Configuración y Despliegue

### Requisitos de Seguridad (SOLID & Arquitectura)
Para que el proxy inverso funcione correctamente, se ajustaron los `settings.py` de Django para confiar en las cabeceras enviadas por Nginx:

```python
# Tienda/settings.py
ALLOWED_HOSTS = [host.strip() for host in os.environ.get("ALLOWED_HOSTS", "*").split(",")]
USE_X_FORWARDED_HOST = True
SECURE_PROXY_SSL_HEADER = ('HTTP_X_FORWARDED_PROTO', 'https')
```

### Orquestación de Contenedores
El archivo `docker-compose.yml` define la interacción entre los servicios:
* **web**: Ejecuta Gunicorn en el puerto 8000 (no expuesto al exterior).
* **nginx**: Expone el puerto 80 y redirige el tráfico al servicio `web`.
* **db**: Persistencia de datos en red privada.

## Evidencias de Funcionamiento

Las evidencias del correcto funcionamiento se encuentran en la carpeta `/evidencias/Taller5/`:

1.  **Orquestación (`01_orquestacion_docker_ps.png`)**: Captura del comando `docker ps` mostrando los tres servicios en ejecución.
2.  **Enrutamiento (`02_enrutamiento_puerto_80.png`)**: Acceso exitoso a la API a través de la IP pública por el puerto 80 gestionado por Nginx.
3.  **Aislamiento (`03_aislamiento_puerto_8000.png`)**: Intento fallido de conexión directa al puerto 8000, demostrando el aislamiento de la aplicación Django.

---

### Nota sobre el Patrón de Estrangulamiento
Esta configuración es el primer paso para descomponer el monolito. Nginx permite que, en el futuro, podamos redirigir rutas específicas (ej. `/api/v2/`) a nuevos microservicios sin que el cliente note cambios en la URL base.

---

**Desarrollado por:** Laura Aceros  
**Curso:** TEIS - Django SOLID 2026