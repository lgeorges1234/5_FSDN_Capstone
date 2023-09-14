# API Reference

## Getting Started
- Base URL: The backend app is hosted using Render hosting Web Sevice : https://render-deployment-flightcomp.onrender.com/. 
 

## Error Handling

Errors are returned as JSON objects in the following format:

```json
{
    "succes": False,
    "error": 400,
    "message": "bad request"
}
```
The API will return five error types when requests fail:
- 400: Invalid Request
- 403: Handles authentication failed error
- 404: Ressource not found
- 422: Not Processable
- 500: Internal Server Error


## Endpoints

### Airports Endpoints

#### `GET '/airports'`

- General:
    - Fetches a dictionary of airports
    - Permissions: None
    - Request Arguments: None
    - Returns: An object with two keys: success set to True and airports, that contains a dictionary of all airports presents in the airports relation.
      
- Sample: `curl https://render-deployment-flightcomp.onrender.com/airports`


```json
{
    "airports": [
        {
            "name": "Atlanta Hartsfield Jackson"
            "code": "ATL",
            "statecode": "GA",
            "countrycode": "US",
            "countryname": "United States",        
        }
        ...
        {
            "name": "Anaa"
            "code": "AAA",
            "statecode": NULL,
            "countrycode": "FR",
            "countryname": "French Polynesia",        
        }
    ],
    "success": true
}
```

---

#### `GET '/airports/${code}'`

- General:  
    - Fetches a particular airport specified by the code in the request argument
    - Permissions: None
    - Request Arguments: `code` - string
    - Returns: An object with two keys: success set to True and airports, that contains a dictionary containing the specific airport.

- Sample: `curl https://render-deployment-flightcomp.onrender.com/airports/ATL`

```json
{
    "airports": [
        {
            "name": "Atlanta Hartsfield Jackson"
            "code": "ATL",
            "statecode": "GA",
            "countrycode": "US",
            "countryname": "United States",        
        }
    ],
    "success": true
}
```

---

#### `POST '/airports-search'`

- General:  
    - Fetches airports given a search term
    - Permissions: None
    - Request Arguments: None
    - Request Body:
     ```json
     {
       "searchTerm": "Atlanta",
     }
     ```
    - Returns: An object with two keys: success set to True and airlines, that contains a dictionary of all airports's names or country's name, that matche the search term.
      
- Sample: `curl -X POST https://render-deployment-flightcomp.onrender.com/airlines-search -H "Content-Type: application/json" -d '{"searchTerm":"France"}'`

```json
{
    "countries": [
        {
            "name": "Atlanta Hartsfield Jackson"
            "code": "ATL",
            "statecode": "GA",
            "countrycode": "US",
            "countryname": "United States",        
        }
    ],
    "success": true
}
```

---

### Countries Endpoints

#### `GET '/coutries'`

- General:
    - Fetches a dictionary of countries
    - Permissions: None
    - Request Arguments: None
    - Returns: An object with two keys: success set to True and countries, that contains a dictionary of all countries presents in the countries table.
      
- Sample: `curl https://render-deployment-flightcomp.onrender.com/countries`


```json
{
    "countries": [
        {
            "code": "AF",
            "name": "Afghanistan"     
        }
      ...
        {
            "code": "ZW",
            "name": "Zimbabwe"     
        }
    ],
    "success": true
}
```

---

#### `GET '/countries/${code}'`

- General:  
    - Fetches a particular country specified by the code in the request argument.
    - Permissions: None
    - Request Arguments: `code` - string
    - Returns: An object with two keys: success set to True and airports, that contains a dictionary containing the specific airport.

- Sample: `curl https://render-deployment-flightcomp.onrender.com/countries/FR`

```json
{
    "countries": [
        {
            "code": "FR",
            "name": "France"     
        }
    ],
    "success": true
}
```

---

#### `POST '/countries'`

- General:  
    - Fetches airports given a search term
    - Permissions: None
    - Request Arguments: None
    - Request Body:
     ```json
     {
       "searchTerm": "France",
     }
     ```
    - Returns: An object with two keys: success set to True and countries, that contains a dictionary of all countries names, that matche the search term.
      
- Sample: `curl -X POST https://render-deployment-flightcomp.onrender.com/countries -H "Content-Type: application/json" -d '{"searchTerm":"France"}'`

```json
{
    "countries": [
        {
            "code": "FR",
            "name": "France"     
        }
    ],
    "success": true
}
```

---


### Airlines Endpoints

#### `GET '/airlines'`

- General:
    - Fetches a dictionary of airlines
    - Permissions: `get:airlines`
    - Request Arguments: None
    - Returns: An object with two keys: success set to True and airlines, that contains a dictionary of all airlines presents in the database.

- Sample: `curl -H "Authorization: Bearer XXXIAMBEARER" https://render-deployment-flightcomp.onrender.com/airlines`


```json
{
    "airlines": [
        {
            "country_code": "FR",
            "id": 1,
            "name": "Airfrance"
        }
    ],
    "success": true
}
```

---

#### `GET '/airlines/${id}'`

- General:  
    - Fetches a particular airline specified by the id in the request argument.
    - Permissions: `get:airlines`
    - Request Arguments: `id` - integer
    - Returns: An object with two keys: success set to True and airlines, that contains a dictionary containing the specific airline.

- Sample: `curl -H "Authorization: Bearer XXXIAMBEARER" https://render-deployment-flightcomp.onrender.com/airlines/1`

```json
{
    "airlines": [
        {
            "country_code": "FR",
            "id": 1,
            "name": "Airfrance"
        }
    ],
    "success": true
}
```


---

#### `POST '/airlines-search'`

- General:  
    - Fetches airlines given a search term.
    - Permissions: `get:airlines`
    - Request Arguments: None
    - Request Body:
     ```json
     {
       "searchTerm": "France",
     }
     ```
    - Returns: An object with two keys: success set to True and airlines, that contains a dictionary of all airline's names that matche the search term.
      
- Sample: `curl -X POST https://render-deployment-flightcomp.onrender.com/airlines-search -H "Content-Type: application/json" -H "Authorization: Bearer XXXIAMBEARER" -d '{"searchTerm":"France"}'`

```json
{
    "airlines": [
        {
            "country_code": "FR",
            "id": 1,
            "name": "Airfrance"
        }
    ],
    "success": true
}
```
---

#### `POST '/airlines'`
- General:  
    - Sends a post request in order to create a new airline.
    - Permissions: `post:airlines`
    - Request Arguments: None
    - Request Body:
    ```json
    {
      "name": "Lufthansa",
      "country_code": "DE",
    }
    ```
   - Returns: a single new airline object
     
- Sample: `curl -X POST https://render-deployment-flightcomp.onrender.com/airlines-search -H "Content-Type: application/json" -H "Authorization: Bearer XXXIAMBEARER" -d '{"name": "Lufthansa","country_code": "DE"}'`

```json
{
    "airlines": [
        {
            "country_code": "DE",
            "id": 2,
            "name": "Lufthansa"
        }
    ],
    "success": true
}

```

#### `DELETE '/airlines/${id}'`
- General:  
    - Deletes a specified airline using its id
    - Permissions: `delete:airlines`
    - Request Arguments: `id` - integer
    - Returns: the airline id that has been deleted

- Sample: `curl -X DELETE https://render-deployment-flightcomp.onrender.com/airlines/2 -H "Authorization: Bearer    
    XXXIAMBEARER"`

```json
{
    "deleted":2,
    "success": true
}

```
---

#### `PATCH '/airlines/${id}'`
- General:  
    - Update a specified airline using its id
    - Permissions: `patch:airlines`
    - Request Arguments: `id` - integer
    - Request Body: one of the airline's parameters or both
    ```json
    {
      "name": "Lufthansa",
      "country_code": "DE",
    }
    ```
    - Returns: a single airline object
     
- Sample: `curl -X PATCH https://render-deployment-flightcomp.onrender.com/airlines/2 -H "Authorization: Bearer    
    XXXIAMBEARER"`


```json
{
    "airlines": [
        {
            "country_code": "DE",
            "id": 1,
            "name": "Lufthansa"
        }
    ],
    "success": true
}

```

---

### Flights Endpoints

#### `GET '/flights'`

- General:
    - Fetches a dictionary of airlines
    - Permissions: `get:flights`
    - Request Arguments: None
    - Returns: An object with two keys: success set to True and flights, that contains a dictionary of all flights presents in the database.

- Sample: `curl -H "Authorization: Bearer XXXIAMBEARER" https://render-deployment-flightcomp.onrender.com/flights`

```json
{
    "flights": [
        {
            "country_code": "FR",
            "id": 1,
            "name": "Airfrance"
        }
    ],
    "success": true
}
```

---


#### `POST '/flights'`
- General:  
    - Sends a post request in order to create a new flights
    - Permissions: `post:flights`
    - Request Arguments: None
    - Request Body:
    ```json
    {
      "flightname": "DF706",
      "departure_code": "AHC",
      "arrival_code": "AGH",
      "status": "0",
      "airline_id": 1,
    }
    ```
   - Permissions: post:airlines
   - Returns: a single new airline object
     
- Sample: `curl -X POST https://render-deployment-flightcomp.onrender.com/airlines-search -H "Content-Type: application/json" -H "Authorization: Bearer XXXIAMBEARER" -d '{"name": "Lufthansa","country_code": "DE"}'`

```json
{
    "airlines": [
        {
          "airline_id": 1,
          "arrival_code": "AGH",
          "date": "Wed, 13 Sep 2023 23:00:00 GMT",
          "departure_code": "AHC",
          "flightname": "DF706",
          "id": 1
          "status": "0",
        }
    ],
    "success": true
}

```
---
