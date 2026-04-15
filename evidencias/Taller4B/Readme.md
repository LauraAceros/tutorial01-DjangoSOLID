
# Tutorial 04B: Despliegue con AWS RDS (MySQL) y Puerto 80

Este taller consiste en la evolución del despliegue en la nube, migrando de una base de datos local en contenedor (PostgreSQL) a una base de datos administrada **AWS RDS (MySQL)** y configurando el acceso a la aplicación a través del puerto estándar **HTTP (80)**.

## Objetivos
* [cite_start]Migrar el motor de persistencia de PostgreSQL a **MySQL** [cite: 390-396].
* [cite_start]Configurar una base de datos administrada en **AWS RDS** bajo la capa gratuita [cite: 390-410].
* Ajustar el **Dockerfile** para soportar dependencias de compilación de MySQL en imágenes *slim*.
* [cite_start]Exponer la aplicación en el **puerto 80** para acceso directo mediante la IP pública del servidor EC2 [cite: 694-698].

## Tecnologías Utilizadas
* **Backend:** Django 5.2.10
* **Base de Datos:** AWS RDS (MySQL 8.0)
* **Contenedores:** Docker & Docker Engine
* **Infraestructura:** AWS EC2 (Amazon Linux 2023)

## Pasos Realizados

### 1. Configuración de Ramas
Se siguió una estructura lineal de ramas para mantener la integridad del repositorio:
* `tutorial04b-fase1-mysql-config`: Configuración de código y motor de base de datos.
* `tutorial04b-paso2-evidencia`: Rama final con el Dockerfile sincronizado y capturas de pantalla.

### 2. Modificaciones de Código
* **`requirements.txt`**: Se agregó la librería `mysqlclient==2.2.4` para la comunicación con RDS.
* **`Tienda/settings.py`**: Se cambió el motor de base de datos a `django.db.backends.mysql` y el puerto por defecto a `3306`.
* **`Dockerfile`**: Se agregaron paquetes de sistema (`pkg-config`, `default-libmysqlclient-dev`, `gcc`) necesarios para compilar el driver de MySQL en la imagen base de Python.

### 3. Infraestructura en AWS
* [cite_start]**RDS:** Se creó una instancia MySQL llamada `teis20251` con el usuario `admin` [cite: 411-421].
* [cite_start]**Seguridad:** Se actualizó el *Security Group* de la base de datos para permitir tráfico entrante en el puerto **3306** desde cualquier IP (`0.0.0.0/0`) para facilitar la conexión desde la EC2 [cite: 548-569].

### 4. Despliegue en EC2
1. Conexión SSH a la instancia EC2.
2. Actualización del repositorio y creación del archivo `.env` con el **Endpoint** de RDS.
3. Construcción de la imagen Docker: `docker build -t tienda-app .`.
4. [cite_start]Ejecución del contenedor mapeando el puerto **80:8000** [cite: 694-696].
5. Ejecución de migraciones remotas: `docker exec -it tienda-web python manage.py migrate`.

##  Evidencias
Las capturas de pantalla se encuentran en la carpeta `Evidencias/Taller4B/`:
1. [cite_start]`01_api_response_aws_rds_port80.png`: Muestra la API respondiendo en la IP pública sin necesidad de especificar puerto [cite: 697-720].
2. `02_rds_inbound_rules.png`: Muestra la regla de entrada para el puerto 3306 en AWS.

