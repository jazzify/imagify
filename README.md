
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

### Build the image
Build the docker image and run all the containers (remove the `-d` option to attach to docker console)
```bash
docker compose build --no-cache
```
Start the containers with
```bash
docker compose up -d
```
  
#### Collect the static files to serve in public
```bash
docker exec -it imagify-web-1 python3 manage.py collectstatic --noinput --clear
```
    
#### Run the database initial migration
```bash
docker exec -it imagify-web-1 python3 manage.py migrate
```

### Remove the docker containers when done playing :)
```bash
docker compose down
```

## Connect to the backend bash in docker web instance (the one running Django)
On you local terminal:

You can either run:
  ```bash
  docker exec -it imagify-web-1 bash
  ```

or, run this to get all the containers:
```bash
  docker ps
```

and, grab the `IMAGE ID` for `imagify_backend-web` docker container

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
