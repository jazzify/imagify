
# imagify

## Run everywhere

#### Previous requirements:

-  Python 3.11+
-  Docker 23.0.5+

Clone the project

```bash
  git clone https://github.com/jazzify/imagify.git
```

Go to the project directory

```bash
  cd imagify_backend
```

Create a `.env` file with the following variables:

```bash
# Postgres
POSTGRES_USER=POSTGRES_USER
POSTGRES_PASSWORD=POSTGRES_PASSWORD
POSTGRES_DB=POSTGRES_DB_NAME
 
# Django
DJANGO_SECRET_KEY="A_DJANGO_SECRET_KEY"

# Redis
REDIS_LOCATION="REDIS_LOCATION" # use redis://localhost:6379/0 by default
```

Build and run the docker image

```bash
  docker compose up --build
```
