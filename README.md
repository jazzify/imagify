
# imagify

## Run everywhere

This project is currently using:
- `django==4.2.7`
- `python==3.11`

Take a look at the following files to learn more about the project dependencies:
- Pipfile
- Dockerfile
- docker-compose.yml

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
Build the docker image and run all the containers
```bash
docker compose build --no-cache
```
Start the containers with:
```bash
docker compose up -d
```
(remove the `-d` option to attach to docker console)

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
On you local terminal, you can run:
```bash
docker exec -it imagify-web-1 bash
```

Or in two steps: 
1. Get all the containers:
```bash
docker ps
```

2. grab the `IMAGE ID` for `web-image` docker container and execute:
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
