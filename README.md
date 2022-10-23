# Setup

## Install

```shell
$ python3 -m venv venv --upgrade-deps
$ . venv/bin/activate
(venv) $ pip install -r requirements.lock --no-binary pydantic --use-pep517 --no-cache --use-feature=no-binary-enable-wheel-cache
```

## Setup a database and create tables

```shell
(venv) $ docker run -d --name db \
  -e POSTGRES_PASSWORD=password \
  -e PGDATA=/var/lib/postgresql/data/pgdata \
  -v $(pwd)/pgdata:/var/lib/postgresql/data \
  -p 5432:5432 \
  postgres:14.4-alpine

(venv) $ DATABASE_URL=postgresql://postgres:password@localhost:5432 prisma db push
Prisma schema loaded from schema.prisma
Datasource "db": PostgreSQL database "postgres", schema "public" at "localhost:5432"

🚀  Your database is now in sync with your schema. Done in 638ms

✔ Generated Prisma Client Python (v0.7.0) to ./app/prisma in 135ms
```

# Run

```shell
(venv) $ DATABASE_URL=postgresql://postgres:password@localhost:5432 APP_CONFIG_FILE=local uvicorn app.main:app --reload-dir app
```

You can now access [localhost:8000/docs](http://localhost:8000/docs) to see the API documentation.


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
