## Tutorial 04: Dockerización y Despliegue en AWS

### Objetivos
- Empaquetar la aplicación en contenedores Docker
- Desplegar en instancia EC2 de AWS Academy
- Configurar variables de entorno para producción

### Archivos creados
- `requirements.txt` - Dependencias Python
- `Dockerfile` - Imagen Docker para Django
- `docker-compose.yml` - Orquestación local (Django + PostgreSQL)
- `.env.example` - Referencia de variables de entorno

### Pasos
1. `tutorial04-paso1-requirements` - Crear requirements.txt
2. `tutorial04-paso2-dockerfile` - Crear Dockerfile
3. `tutorial04-paso3-compose-local` - Crear docker-compose.yml
4. `tutorial04-paso4-settings-env` - Refactorizar settings.py
5. `tutorial04-paso5-evidencia` - Deploy en AWS EC2 + evidencias

### Deploy en AWS
API accesible en: `http://52.90.249.219:8000/api/v1/comprar/`