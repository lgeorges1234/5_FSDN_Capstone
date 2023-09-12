# Backend - FlightCompany API

## Introduction to FlightCompany API

FlightCompany API is a capstone project for Udacity Fullstack Developper Nanodegree. This API place a user as being a passenger that want to book a flight or an airline manger that can create, delete or update airlines (and later on flight).
Three other tables are initialized at the creation of the database. 
- airports : lists all main airports in the world
- countries : lists all countries
- flightstatus : relates actual status of the flight. When the flight is created, the default status is 0 - unknown.

### Database relation

![Database Relationship](./docs/FlightSurety_Comp_Backend_Data.jpeg)

=======

## Setting up the Backend

### Install Dependencies

1. **Python 3.7** - Follow instructions to install the latest version of python for your platform in the [python docs](https://docs.python.org/3/using/unix.html#getting-and-installing-the-latest-version-of-python)
 
2. **Virtual Environment** - We recommend working within a virtual environment whenever using Python for projects. This keeps your dependencies for each project separate and organized. Instructions for setting up a virual environment for your platform can be found in the [python docs](https://packaging.python.org/guides/installing-using-pip-and-virtual-environments/)

3. **PIP Dependencies** - Once your virtual environment is setup and running, install the required dependencies by navigating to the `/backend` directory and running:

```bash
pip install -r requirements.txt
```

#### Key Pip Dependencies

- [Flask](http://flask.pocoo.org/) is a lightweight backend microservices framework. Flask is required to handle requests and responses.

- [SQLAlchemy](https://www.sqlalchemy.org/) is the Python SQL toolkit and ORM we'll use to handle the lightweight SQL database. You'll primarily work in `app.py`and can reference `models.py`.

- [Flask-CORS](https://flask-cors.readthedocs.io/en/latest/#) is the extension we'll use to handle cross-origin requests from our frontend server.

### Set up the Database

#### Create a local database using docker

Create a Postgres database using the docker-compose :

The creation of a Postgres Docker instance requires the use of a .env file containing all database information :

```bash
POSTGRES_HOST=127.0.0.1
POSTGRES_PASSWORD=ssdddsdfw-fasfasfsda-gfdsgfs
PORT_DEV=5432
POSTGRES_DB_DEV=fsdn
POSTGRES_USER_DEV=fsdn_user
POSTGRES_PASSWORD_DEV=password123
POSTGRES_DB_TEST=fsdn_test
POSTGRES_USER_TEST=fsdn_user_test
POSTGRES_PASSWORD_TEST=password123_test
ENV=dev
```

```bash
docker-compose up
su - postgres
```
#### Live deployment server 

In order for the project to be submitted, a Render Web Service has been created and deployed. The service can be reached at the following url:

https://render-deployment-flightcomp.onrender.com/


### Run the Server

From within the `./src` directory first ensure you are working using your created virtual environment.

To run the server, execute:

```bash
flask run --reload
```

The `--reload` flag will detect file changes and restart the server automatically.

## Setup Auth0 Roles and Users

1. Create a new Auth0 Account
2. Select a unique tenant domain
3. Create a new, single page web application
4. Create a new API
   - in API Settings:
     - Enable RBAC
     - Enable Add Permissions in the Access Token
5. Create new API permissions:
   - `get:airlines` `post:airlines` `patch:airlines` `delete:airlines`
   - `get:flights` `post:flights` `update:flights`
6. Create new roles for:
   - Passenger
     - can `get:airlines`
     - can `post:flights`
     - User: passenger@airflight.com
     - Password: asdfafbghbter#$%%76
     - JWT `eyJhbGciOiJSUzI1NiIsInR5cCI6IkpXVCIsImtpZCI6Inh1NS1ucGNtVVNuWW1ncXNZQjhVSSJ9.eyJpc3MiOiJodHRwczovL2Rldi1oNmNjNzhyNzNrdXNudHloLnVzLmF1dGgwLmNvbS8iLCJzdWIiOiJhdXRoMHw2NGY1OTZkYTBmMTQxMzUxOWE2YmIwMjAiLCJhdWQiOiJhaXJsaW5lcyIsImlhdCI6MTY5MzkwODY4OSwiZXhwIjoxNjk2NTAwNjg5LCJhenAiOiIzY2JqSDZjZmd4UWxyRnhmUVp2VXdtbEdYNjZrZEhuUyIsImd0eSI6InBhc3N3b3JkIiwicGVybWlzc2lvbnMiOlsiZ2V0OmFpcmxpbmVzIiwicG9zdDpmbGlnaHRzIl19.d0NgG3HBxi0YxUe3OCy9s2AAK7nhoHlmQVkhhPM9vqRk040UekRn503U6DDCedzkoL9V4Ds2FDPbtoE-l2Xb6DaNmp1sLbhNkx_pGAcBxjhU5K2JJ3E46aVvJf0DhN3PvfBLffZP8It0girXhN0uFfdyGgdnzXYsLhAHcylnY-wYJJG9gbm67A-pI9dL-zymyHMgHw6sL_ijI5D7irV80qRFwki6ajZ_PVv3Ga1H6VQP2XTOqIu7f2E1LZ8b2yFqeyx1V19s7tla2cgw8qAJotIbEzj7q-3ElKMGhUVmW8Bqj4wBNb3xcRjDj7cs2Z6K4mrIbgrBIQA9k7xSvK6CLw`
   - Airline Manager
     - can `get:airlines` `post:airlines` `patch:airlines` `delete:airlines`
     - can `get:flights` `update:flights` 
     - User: airline-manager@airflight.com
     - Password: vk_!trREUH!4jN5
     - JWT `eyJhbGciOiJSUzI1NiIsInR5cCI6IkpXVCIsImtpZCI6Inh1NS1ucGNtVVNuWW1ncXNZQjhVSSJ9.eyJpc3MiOiJodHRwczovL2Rldi1oNmNjNzhyNzNrdXNudHloLnVzLmF1dGgwLmNvbS8iLCJzdWIiOiJhdXRoMHw2NGY1OTdhYWQ5NDgwYjM1YjFmNDBiNjciLCJhdWQiOiJhaXJsaW5lcyIsImlhdCI6MTY5NDExMjM3NywiZXhwIjoxNjk2NzA0Mzc3LCJhenAiOiIzY2JqSDZjZmd4UWxyRnhmUVp2VXdtbEdYNjZrZEhuUyIsImd0eSI6InBhc3N3b3JkIiwicGVybWlzc2lvbnMiOlsiZGVsZXRlOmFpcmxpbmVzIiwiZ2V0OmFpcmxpbmVzIiwiZ2V0OmZsaWdodHMiLCJwYXRjaDphaXJsaW5lcyIsInBvc3Q6YWlybGluZXMiLCJ1cGRhdGU6ZmxpZ2h0cyJdfQ.Qp9Na15knNbM58TQKm3bgDyDCtEHFaRAzqWjlAeBsC-ayK0YZOSmqD1sgxcJe9zL-8EP_yvaPGawIf3qYxRsoTmRK3JATyX5lAHkBkqlVoiVshxc-RinqvFlgZHnNQp99yFkg1UroTY4e5JE5S2mIgWvxCe49oNQgpB78s8iWxTXlMema8wCGfuWZNK-Ul4YQx9mpT2Pprd_8eio6Uw-MBwFtxrRacgnD9zyIVXI45pFs687Pmg98DWFycHcisCaGaQ7_RUtU9O2buG2l1CVaf39MjSIGyORcCTN-PllI-jGVQQsJ5-GFov0H37w4SI8fwwS8azlggn7UJsNAb8uTw`


## Endpoint Documentation

[API Documentation](docs/API_doc.md)



## Testing

Two environment variables need to be added to the .env file for the tests to run:

MANAGER_TOKEN=eyJhbGciOiJSUzI1NiIsInR5cCI6IkpXVCIsImtpZCI6Inh1NS1ucGNtVVNuWW1ncXNZQjhVSSJ9.eyJpc3MiOiJodHRwczovL2Rldi1oNmNjNzhyNzNrdXNudHloLnVzLmF1dGgwLmNvbS8iLCJzdWIiOiJhdXRoMHw2NGY1OTdhYWQ5NDgwYjM1YjFmNDBiNjciLCJhdWQiOiJhaXJsaW5lcyIsImlhdCI6MTY5NDExMjM3NywiZXhwIjoxNjk2NzA0Mzc3LCJhenAiOiIzY2JqSDZjZmd4UWxyRnhmUVp2VXdtbEdYNjZrZEhuUyIsImd0eSI6InBhc3N3b3JkIiwicGVybWlzc2lvbnMiOlsiZGVsZXRlOmFpcmxpbmVzIiwiZ2V0OmFpcmxpbmVzIiwiZ2V0OmZsaWdodHMiLCJwYXRjaDphaXJsaW5lcyIsInBvc3Q6YWlybGluZXMiLCJ1cGRhdGU6ZmxpZ2h0cyJdfQ.Qp9Na15knNbM58TQKm3bgDyDCtEHFaRAzqWjlAeBsC-ayK0YZOSmqD1sgxcJe9zL-8EP_yvaPGawIf3qYxRsoTmRK3JATyX5lAHkBkqlVoiVshxc-RinqvFlgZHnNQp99yFkg1UroTY4e5JE5S2mIgWvxCe49oNQgpB78s8iWxTXlMema8wCGfuWZNK-Ul4YQx9mpT2Pprd_8eio6Uw-MBwFtxrRacgnD9zyIVXI45pFs687Pmg98DWFycHcisCaGaQ7_RUtU9O2buG2l1CVaf39MjSIGyORcCTN-PllI-jGVQQsJ5-GFov0H37w4SI8fwwS8azlggn7UJsNAb8uTw
PASSENGER_TOKEN=eyJhbGciOiJSUzI1NiIsInR5cCI6IkpXVCIsImtpZCI6Inh1NS1ucGNtVVNuWW1ncXNZQjhVSSJ9.eyJpc3MiOiJodHRwczovL2Rldi1oNmNjNzhyNzNrdXNudHloLnVzLmF1dGgwLmNvbS8iLCJzdWIiOiJhdXRoMHw2NGY1OTZkYTBmMTQxMzUxOWE2YmIwMjAiLCJhdWQiOiJhaXJsaW5lcyIsImlhdCI6MTY5MzkwODY4OSwiZXhwIjoxNjk2NTAwNjg5LCJhenAiOiIzY2JqSDZjZmd4UWxyRnhmUVp2VXdtbEdYNjZrZEhuUyIsImd0eSI6InBhc3N3b3JkIiwicGVybWlzc2lvbnMiOlsiZ2V0OmFpcmxpbmVzIiwicG9zdDpmbGlnaHRzIl19.d0NgG3HBxi0YxUe3OCy9s2AAK7nhoHlmQVkhhPM9vqRk040UekRn503U6DDCedzkoL9V4Ds2FDPbtoE-l2Xb6DaNmp1sLbhNkx_pGAcBxjhU5K2JJ3E46aVvJf0DhN3PvfBLffZP8It0girXhN0uFfdyGgdnzXYsLhAHcylnY-wYJJG9gbm67A-pI9dL-zymyHMgHw6sL_ijI5D7irV80qRFwki6ajZ_PVv3Ga1H6VQP2XTOqIu7f2E1LZ8b2yFqeyx1V19s7tla2cgw8qAJotIbEzj7q-3ElKMGhUVmW8Bqj4wBNb3xcRjDj7cs2Z6K4mrIbgrBIQA9k7xSvK6CLw

In order to run tests navigate to the backend folder and run the following commands: 

To deploy the tests, run

```bash
python test_flaskr.py
```

All tests are kept in that file and should be maintained as updates are made to app functionality.
