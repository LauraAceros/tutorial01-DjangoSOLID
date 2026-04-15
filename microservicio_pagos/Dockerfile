FROM python:3.11-alpine
WORKDIR /app
RUN pip install flask gunicorn [cite: 47]
COPY . .
EXPOSE 5000
CMD ["gunicorn", "app:app", "--bind", "0.0.0.0:5000"] [cite: 50]