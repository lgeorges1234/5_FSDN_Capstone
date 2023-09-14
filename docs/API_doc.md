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

### `GET '/airlines'`

- General:
    - Fetches a dictionary of airlines
    - Request Arguments: None
    - Permissions: get:airlines
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

### `GET '/airlines/${id}'`

- General:  
    - Fetches a particular airline specified by the id in the request argument.
    - Request Arguments: `id` - integer
    - Permissions: get:airlines
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

### `POST '/airlines-search'`

- General:  
    - Fetches airlines given a search term 
    - Request Body:
```json
{
  "searchTerm": "France",
}
```
    - Permissions: get:airlines
    - Returns: An object with two keys: success set to True and airlines, that contains a dictionary of all airlines name that matche the search term.
- Sample: `curl https://render-deployment-flightcomp.onrender.com/airlines-search -X POST -H "Content-Type: application/json" -H "Authorization: Bearer XXXIAMBEARER" -d '{"searchTerm":"France"}'`

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

### `POST '/airlines'`
- General:  
    - Sends a post request in order to create a new airline
    - Request Body:

```json
{
  "name": "Lufthansa",
  "country_code": "DE",
}
```
- Permissions: post:airlines
- Sample: `curl -X POST https://render-deployment-flightcomp.onrender.com/airlines-search -H "Content-Type: application/json" -H "Authorization: Bearer XXXIAMBEARER" -d '{"name": "Lufthansa","country_code": "DE"}'`

- Returns: a single new airline object

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


### `DELETE '/airlines/${id}'`
- General:  
    - Deletes a specified airline using its id
    - Request Arguments: `id` - integer
    - Sample: `curl -X DELETE https://render-deployment-flightcomp.onrender.com/airlines/2 -H "Authorization: Bearer    
    XXXIAMBEARER"`
    - Returns: the airline id that has been deleted

```json
{
    "deleted":2,
    "success": true
}

```
---
### `PATCH '/airlines/${id}'`
- General:  
    - Update a specified airline using its id
    - Request Arguments: `id` - integer
    - Request Body: one of the airline's parameters or both

```json
{
  "name": "Lufthansa",
  "country_code": "DE",
}
```
    - Sample: `curl -X PATCH https://render-deployment-flightcomp.onrender.com/airlines/2 -H "Authorization: Bearer    
    XXXIAMBEARER"`
    - Returns: a single airline object

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

---


