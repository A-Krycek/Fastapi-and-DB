# FastAPI + AWS EC2 + PostgreSQL RDS

Backend REST para administrar usuarios y libros. Incluye CRUD completo,
documentación Swagger y configuración de `systemd` para Ubuntu en EC2.

## Preparación

```bash
python3 -m venv .venv
source .venv/bin/activate
pip install -r requirements.txt
cp .env.example .env
```

Edita `.env` y coloca las credenciales y el endpoint reales de Amazon RDS.
No subas el archivo `.env` al repositorio.

## Ejecución local o en EC2

```bash
uvicorn main:app --host 0.0.0.0 --port 8000 --reload
```

Abre `http://IP_DEL_SERVIDOR:8000/docs` para usar Swagger UI.

## Rutas principales

- `GET /`: estado general de la API.
- `GET /health`: comprobación rápida del servicio.
- `/users/`: crear, consultar, actualizar y eliminar usuarios.
- `/books/`: crear, consultar, actualizar y eliminar libros.

## Ejemplos para Swagger

Usuario:

```json
{
  "name": "Carlos Gomez",
  "email": "carlos@example.com"
}
```

Libro:

```json
{
  "title": "Clean Architecture",
  "author": "Robert C. Martin",
  "published_year": 2017,
  "user_id": 1
}
```

## Activar el servicio en EC2

Después de colocar el proyecto en `/home/ubuntu/fastapi-aws-project`:

```bash
sudo cp deploy/fastapi.service /etc/systemd/system/fastapi.service
sudo systemctl daemon-reload
sudo systemctl enable --now fastapi
sudo systemctl status fastapi
```

En AWS, permite el puerto 8000 en el grupo de seguridad de EC2. En el grupo
de RDS, permite PostgreSQL 5432 únicamente desde el grupo de seguridad de EC2.
