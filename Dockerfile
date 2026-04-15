# Imagen base Python 3.11
FROM python:3.11-slim

# Variables de entorno
ENV PYTHONDONTWRITEBYTECODE=1
ENV PYTHONUNBUFFERED=1

# Directorio de trabajo
WORKDIR /app

# Instalar dependencias
COPY requirements.txt /app/
RUN pip install --no-cache-dir -r requirements.txt

# Copiar código
COPY . /app/

# Puerto
EXPOSE 8000

# Comando por defecto
CMD ["python", "manage.py", "runserver", "0.0.0.0:8000"]