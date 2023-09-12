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
- Sample: `curl https://render-deployment-flightcomp.onrender.com/airlines`


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

- Sample: `curl http://127.0.0.1:5000/questions?page=3`

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
    - Request Arguments: `searchTerm` - string
    - Permissions: get:airlines
    - Returns: An object with two keys: success set to True and airlines, that contains a dictionary of all airlines name that matche the search term.
- Sample: `curl http://127.0.0.1:5000/categories/4/questions`

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
    'previous_questions': [1, 4, 20, 15]
    'quiz_category': 'current category'
 }
```

- Sample: `curl http://127.0.0.1:5000/quizzes -X POST -H "Content-Type: application/json" -d '{"previous_questions":[1, 4, 20, 15], "quiz_category":"current category"}'`

- Returns: a single new question object

```json
{
  "question": {
    "id": 1,
    "question": "This is a question",
    "answer": "This is an answer",
    "difficulty": 5,
    "category": 4
  }
}
```


### `DELETE '/questions/${id}'`
- General:  
    - Deletes a specified question using the id of the question
    - Request Arguments: `id` - integer
    - Returns: Does not need to return anything besides the appropriate HTTP status code. Optionally can return the id of the question. If you are able to modify the frontend, you can have it remove the question using the id instead of refetching the questions.
- Sample: `curl -X DELETE http://127.0.0.1:5000/questions/12`

---



---

### `POST '/questions'`
- General:      
    - Sends a post request in order to add a new question
    - Request Body:

```json
{
  "question": "Heres a new question string",
  "answer": "Heres a new answer string",
  "difficulty": 1,
  "category": 3
}
```
- Sample: `curl http://127.0.0.1:5000/questions -X POST -H "Content-Type: application/json" -d '{"question":"Heres a new question string", "answer":"Heres a new answer string", "difficulty":1,"category":3}'`

- Returns: Does not return any new data

---

### `POST '/questions'`
- General:  
    - Sends a post request in order to search for a specific question by search term
    - Request Body:

```json
{
  "searchTerm": "this is the term the user is looking for"
}
```
- Sample: `curl http://127.0.0.1:5000/questions -X POST -H "Content-Type: application/json" -d '{"searchTerm":"this is the term the user is looking for"}'`

- Returns: any array of questions, a number of totalQuestions that met the search term and the current category string

```json
{
  "questions": [
    {
      "id": 1,
      "question": "This is a question",
      "answer": "This is an answer",
      "difficulty": 5,
      "category": 5
    }
  ],
  "totalQuestions": 100,
  "currentCategory": "Entertainment"
}
```
