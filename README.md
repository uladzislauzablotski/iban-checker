```
  _____  _                       ___  _                  _                
  \_   \| |__    __ _  _ __     / __\| |__    ___   ___ | | __  ___  _ __ 
   / /\/| '_ \  / _` || '_ \   / /   | '_ \  / _ \ / __|| |/ / / _ \| '__|
/\/ /_  | |_) || (_| || | | | / /___ | | | ||  __/| (__ |   < |  __/| |   
\____/  |_.__/  \__,_||_| |_| \____/ |_| |_| \___| \___||_|\_\ \___||_|   
                                                                                                                                   
```
Fast API backend of iban check app


## Getting Started

Install poetry:
```shell
$ make install-poetry
```

Install dependencies: 
```shell
$ make install-packages
```

Run the build:

```shell
$ make docker-build
```

Restart containers:

```shell
$ make docker-down
$ make docker-up
```

To run tests:

```shell
$ make tests
```

To run linters:

```shell
$ make lint
```


Check Swagger docs:
[http://0.0.0.0:8000/docs](http://0.0.0.0:8000/docs)

## Alembic work

Merge alembic migrations:

```shell

$ make alembic-merge-heads

```

Make migrations:

```shell

$ make migrations
```

Apply migrations:

```shell

$ make migrate
```