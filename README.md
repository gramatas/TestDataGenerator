# inDataGen
Create on-demand test data

### Tech stack
- Python 
  - Django
  - Celery
  - Bonobo  
- Docker
  - Docker compose
- PostgreSQL
- NGINX
  
### Environments

There are two environments set up: local and production. Each environment uses its own environment variables, which are 
located under the `.envs` directory.

Production environment uses NGINX server and runs django using gunicorn, while the local one runs Django development server 
directly.

### Building the project

In order to build the project with docker compose use the following commands.

- Local:

`docker-compose build`

- Production:

`docker-compose -f docker-compose.prod.yml build`

### Running the project

In order to run the project with docker compose use the following commands.

Run the Migration to load seed data.

```
docker-compose run --rm django python manage.py makemigrations
docker-compose run --rm django python manage.py migrate
```

- Local:

`docker-compose up`

- Production:

`docker-compose -f docker-compose.prod.yml up`

## Test ETL

The first ETL was developed with no interface.

In order to test de etl, you can perform a POST request to localhost:8000/test-etl

The operations that are currently supported are:
- API to CSV
- API to Postgres
- Postgres to CSV
- Postgres to Postgres

The documentation of how the body request should be, can be found at `https://documenter.getpostman.com/view/2422851/TzCFfqGW`

## Transformations

The system currently support the following transformations:
- Hash: Transform field to a hash using sha1 algorithm.
- Fake: User faker library to create a synthetic value. A faker function should be specified to generate the value.
- Passthrough: Do nothing to the value.
- Random: Generates a random value. It can be defined if it should be an integer or float.
- Options: Select a random value from a series of options.

The transformations must be specified as part of the request json. An example can be found below:
The API2CSV example on the Postman documentation was updated to use transformations. 

```
"transformation_schema":{
        "ZIP": {
            "name": "Fake",
            "type": "postcode" 
        },
        "CBSA": {
            "name": "Fake",
            "type": "company" 
        },
        "ID": {
            "name": "Hash"
        },
        "DATEUPDT": {
            "name": "Fake",
            "type": "date",
            "faker_params": "%m/%d/%Y"
        },
        "DEPDOM": {
            "name": "Random",
            "type": "integer"
        },
        "ACTIVE":{
            "name": "Options",
            "options": [2, 3, 4]
        }
    }
```
