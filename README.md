
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
POSTGRES_USER=ADMIN
POSTGRES_PASSWORD=PASSWORD
POSTGRES_DB=imagify
 
# Django
DJANGO_SECRET_KEY="@(&t2h4zg+0o)m4q^wh4o0&tw4h_960u@s4y5c5e=mbg+s(k&c"

# Redis
REDIS_LOCATION="redis://localhost:6379/0"
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