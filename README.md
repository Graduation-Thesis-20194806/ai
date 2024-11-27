# Server Documentation

## Environment setup

Run Web Backend first: https://github.com/Graduation-Thesis-20194806/be.git

```
cp .env.example .env

#Then fill missing field in .env file
```
Edit .env file with your database information and other information. Ask other developers for secret information like AWS and OpenAI keys

Install [Poetry](https://python-poetry.org/docs/#installation)

Run Backend

```
docker compose -f docker-compose.db.yml
```

## Install dependencies

```
poetry install
```

## Run server

```
poetry run dev

poetry run start
```

### Job Queue

Run Job Queue

```
cd server
poetry run celery_worker
```

### Status code

```
https://fastapi.tiangolo.com/reference/status/
```
