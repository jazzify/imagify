
# imagify

## Run everywhere

### Previous requirements:

-  Git
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
```

Build the docker image and run all the containers (`CTRL + C` to stop them)
```bash
  docker compose up --build
```

Remove the docker containers when done playing :)
```bash
  docker compose down
```


## Connect to the backend bash in docker web instance (the one running Django)
On you local terminal:

You can either run:
  ```bash
  docker exec -it imagify_backend-web-1 bash
  ```

or, run this to get all the containers:
```bash
  docker ps
```

And, grab the `IMAGE ID` for `imagify_backend-web` docker container

```bash
  docker exec -it <IMAGE ID> bash
```


### Once connected

On the docker container bash:

<details>
  <summary>Testing</summary>
  
  ```bash
    pipenv run pytest
  ```
</details>

<details>
  <summary>Appling migrations</summary>

  Note: Migrations are applied automatically while using the `docker compose up` command via the `docker-entrypoint.sh` file
  
  ```bash
    python manage.py migrate
  ```
</details>
