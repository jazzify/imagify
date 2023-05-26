
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

Remove the docker image when done playing

```bash
  docker compose down
```

### Connect to backend bash in docker

To run the tests follow the next instructions

```bash
  docker ps
```

Grab the `IMAGE ID` for `imagify_backend-web` docker image

```bash
  docker exec -it <IMAGE ID> bash
```


### Once connected
#### Testing

```bash
  pipenv run pytest
```

#### Appling migrations

```bash
  python manage.py migrate
```