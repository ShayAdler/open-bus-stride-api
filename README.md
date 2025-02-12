# Open Bus Stride API

API For the Open Bus Stride project

See [our contributing docs](https://github.com/hasadna/open-bus-pipelines/blob/main/CONTRIBUTING.md) if you want to suggest changes to this repository.

## Development using the Docker Compose environment

This is the easiest option to start development, follow these instructions: https://github.com/hasadna/open-bus-pipelines/blob/main/README.md#stride-api

For local development, see the additional functionality section: `Develop stride-api from a local clone`

## Local Development

It's much easier to use the Docker Compose environment, but the following can be
refferd to for more details regarding the internal processes and for development
using your local Python interpreter. 

### Install

Create a virtualenv (using Python 3.8)

```
python3.8 -m venv venv
```

Update pip

```
venv/bin/pip install --upgrade pip
```

You should have a copy of open-bus-stride-db repository at ../open-bus-stride-db

Install dependencies

```
venv/bin/pip install -r requirements-dev.txt 
```

### Use

You need a DB to connect to, there are 2 options here:

* Start the stride-db from open-bus-pipelines docker-compose environment
* Connect to the production DB using the Redash read-only credentials
  * Create a `.env` file with the following, replacing the url to the production redash read-only url: `export SQLALCHEMY_URL=postgresql://postgres:123456@localhost`
  * Source the .env: `. .env`

Activate virtualenv

```
. venv/bin/activate
```

Start the FastAPI server with automatic reload on changes

```
uvicorn open_bus_stride_api.main:app --reload
```

See the API docs at http://localhost:8000/docs
