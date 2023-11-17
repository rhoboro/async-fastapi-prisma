# Async Web API with FastAPI + Prisma + GraphQL

This is a sample project of Async Web API with FastAPI + Prisma.

If you want to use sqlalchemy instead of prisma, see [rhoboro/async-fastapi-sqlalchemy](https://github.com/rhoboro/async-fastapi-sqlalchemy).

# Setup

## Install

```shell
$ python3 -m venv venv --upgrade-deps
$ . venv/bin/activate
(venv) $ pip install -r requirements.lock
```

## Setup a database and create tables

```shell
(venv) $ docker run -d --name db \
  -e POSTGRES_PASSWORD=password \
  -e PGDATA=/var/lib/postgresql/data/pgdata \
  -v $(pwd)/pgdata:/var/lib/postgresql/data \
  -p 5432:5432 \
  postgres:16.0-alpine

(venv) $ DATABASE_URL=postgresql://postgres:password@localhost:5432 prisma db push
Prisma schema loaded from schema.prisma
Datasource "db": PostgreSQL database "postgres", schema "public" at "localhost:5432"

🚀  Your database is now in sync with your Prisma schema. Done in 69ms

✔ Generated Prisma Client Python (v0.11.0) to ./app/prisma in 98ms
```

# Run

```shell
(venv) $ APP_CONFIG_FILE=local uvicorn app.main:app --reload-dir app
```

You can now access [localhost:8000/docs](http://localhost:8000/docs) to see the API documentation.

## GraphQL

This application has additional endpoint /graphql.
If installed graphene, you can also access [localhost:8000/graphql](localhost:8000/graphql).

```shell
(venv) $ pip install graphene
(venv) $ APP_CONFIG_FILE=local uvicorn app.main:app --reload-dir app
```

```shell
$ curl -X POST localhost:8000/graphql -H 'content-type=application/json' --data '{"query": "query { notebook(id:1) { id title notes { title notebookId }}}"}'
{
  "notebook": {
    "id": "1",
    "title": "string",
    "notes": [
      {
        "title": "string",
        "notebookId": 1
      }
    ]
  }
}
```


# Test

```shell
(venv) $ pip install -r requirements_test.txt
(venv) $ black app
(venv) $ isort app
(venv) $ pytest app
(venv) $ mypy app
(venv) $ pyright
```

# Prisma Commands

See [https://www.prisma.io/docs/reference/api-reference/command-reference](https://www.prisma.io/docs/reference/api-reference/command-reference)

# TODOs

- [ ] Add Unit tests
- [ ] Setup a temporary db for unit test
