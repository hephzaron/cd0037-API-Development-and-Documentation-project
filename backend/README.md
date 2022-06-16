# Trivia API

Trivia API is an online web application where a user can create question alongside with the answer. It also has a quiz section where a user can answer questions displayed at random and get his/her score immediately.

## Table of Contents

* [Setting Up and Installing Dependencies](#setting-up-and-installing-dependencies)
* [Error Handling](#error-handling)
* [API Documentation](#api-documentation)
* [Endpoint Testing](#endpoint-testing)
* [Author](#author)

## Setting Up and Installing Dependencies
1. **Python 3.7** - Follow instructions to install the latest version of python for your platform in the [python docs](https://docs.python.org/3/using/unix.html#getting-and-installing-the-latest-version-of-python)

2. **Virtual Environment** - It is advisable to work within a virtual environment when executing any project in python. This keeps your dependencies for each project separate and organized. Instructions for setting up a virual environment for your platform can be found in the [python docs](https://packaging.python.org/guides/installing-using-pip-and-virtual-environments/)

3. **PIP Dependencies** - Once your virtual environment is setup and running, install the required dependencies by navigating to the `/backend` directory and running:

```bash
pip install -r requirements.txt
```
### Key Pip Dependencies

- [Flask](http://flask.pocoo.org/) is a lightweight backend microservices framework. Flask is required to handle requests and responses.

- [SQLAlchemy](https://www.sqlalchemy.org/) is the Python SQL toolkit and ORM we'll use to handle the lightweight SQL database. You'll primarily work in `app.py`and can reference `models.py`.

- [Flask-CORS](https://flask-cors.readthedocs.io/en/latest/#) is the extension we'll use to handle cross-origin requests from our frontend server.

### Set up the Database

With Postgres running, create a `trivia` database:

```bash
createdb trivia
```

Populate the database using the `trivia.psql` file provided. From the `backend` folder in terminal run:

```bash
psql trivia < trivia.psql
```

### Run the Server

From within the `./backend` within the created virtual environment

To run the server, execute:

```bash
flask run --reload
```
The `--reload` flag will detect file changes and restart the server automatically.
## Error Handling
Errors are returned in the following JSON formats
```
{
    "success": False,
    "error": 404,
    "message": "Resource not found"
}
```
The API will return three error types when requests fail:
- 400: Bad request
- 404: Resource not found
- 422: Unprocessable entity
- 500: Server error

## API Documentation
### `GET /categories`

- Fetches a dictionary of categories in which the keys are the ids and the value is the corresponding string of the category
- Request Arguments: None
- Returns: An object with two keys, `success`, a boolean value that returns true on successful request and `categories`, that contains an object of `id: category_string` key: value pairs.
- Sample: `curl http://127.0.0.1:5000/categories`
- Response:
```json
{
    "success": True,
    "categories": {
        "1": "Science",
        "2": "Art",
        "3": "Geography",
        "4": "History",
        "5": "Entertainment",
        "6": "Sports"
        }
}
```

### `GET /questions`

- Fetches a dictionary that contains a success status, an array of questions, total questions contained in the array and a dictionary of category
- Request Arguments: `page <int>`
- Returns: An object with four keys, `success`: a boolean value that returns true on successful request, `questions`: a list of questions, `total_questions`: an integer that depict the total number of questions returned from the database and `categories`: that contains an object of `id: category_string` key: value pairs
- Sample: `curl http://127.0.0.1:5000/questions?page=1`
- Response:
```json
{
    "success": True,
    "questions": [
        {
            "id": 1,
            "question": "Nigeria is in which continent ?",
            "answer": "Africa",
            "category": 3,
            "difficulty": 1
        },
        {
            "id": 2,
            "question": "In what year did Nigeria gain independence ?",
            "answer": 1960,
            "category": 4,
            "difficulty": 1
        }
        ...
    ],
    "total_questions": 2,
    "categories": {
        "1": "Science",
        "2": "Art",
        "3": "Geography",
        "4": "History",
        "5": "Entertainment",
        "6": "Sports"
        }
}
```

### `DELETE /questions/{question_id}`

- Deletes a question object
- Request Arguments: `question_id <int>`
- Returns: An object with three keys, `success`: a boolean value that returns true on successful request, `id`: id of deleted question, and `message`: that contains a feedback to users
- Sample: `curl -X DELETE http://127.0.0.1:5000/questions/1`
- Response:
```json
    {
        "success": True,
        "id": 1,
        "message": "Question ID: 1 deleted successfully"
    }
```

### `POST /questions`
- Creates a new question using the `question`, `answer`, `category` and `difficulty`.
- Returns a success value and message as a user feedback.
- Sample: `curl http://127.0.0.1:5000/questions -X POST -H "Content-Type: application/json" -d '{"question":"Nigeria is in which continent ?", "answer":"Africa", "category":"3", "difficulty":"1"}'`
- Response:
```json
{
    "success": True,
    "message": "Question was successfully created"
}
```
#### `POST /questions`
- Searches for a question using the `searchTerm` if contained in the body request.
- Returns an object of key-value pairs where the keys are the `category_id` of found items. Items found are grouped by categories. For each `category_id` in the dictionary, a list of `questions` with the term are returned for the category, the total questions contained in that list as `total_questions` and the category they belong to as `current_category`
- Sample: `curl http://127.0.0.1:5000/questions -X POST -H "Content-Type: application/json" -d '{"searchTerm":"Nigeria"}'`
- Response:
```json
{
    "3":{
        "questions":[
            {
                "id": 1,
                "question": "Nigeria is in which continent ?",
                "answer": "Africa",
                "category": 3,
                "difficulty": 1
            },
            ...
        ],
        "total_questions": 1,
        "current_category": 3
    },
    "4":{
        "questions":[
            {
                "id": 2,
                "question": "In what year did Nigeria gain independence ?",
                "answer": 1960,
                "category": 4,
                "difficulty": 1
            },
            ...
        ],
        "total_questions": 1,
        "current_category": 4
    },
    ...
}
```

### `GET /categories/{category_id}/questions`

- Fetches a dictionary that contains a success status, an array of questions, total questions contained in the array and the category
- Request Arguments: `category_id <int>`
- Returns: An object with four keys, `success`: a boolean value that returns true on successful request, `questions`: a list of questions, `total_questions`: an integer that depict the total number of questions returned from the database and `current_category`
- Sample: `curl http://127.0.0.1:5000/categories/3/questions`
- Response:
```json
    {
        "success": True,
        "questions": [
            {
                "id": 1,
                "question": "Nigeria is in which continent ?",
                "answer": "Africa",
                "category": 3,
                "difficulty": 1
            },
            ...
        ],
        "total_questions": 1,
        "current_category": 3
    }
```

### `POST /quizzes`
- Enables user to answer questions from a fetched list of available questions.
- Request: The request object is a dictionary with two keys: `previous_questions`: An array of previous questions id already answered by the user, `quiz_category`: The category where question is been selected from at random. When a user does not specify any category, the questions are picked at random from all available categories.
- Returns a success value and a question object
- Sample: `curl http://127.0.0.1:5000/quizzes -X POST -H "Content-Type: application/json" -d '{"previous_questions":"[1, 4]", "quiz_category":"1"}'`
- Response:
```json
{
    "success": True,
    "question": {
        "id": 1,
        "question": "Nigeria is in which continent ?",
        "answer": "Africa",
        "category": 3,
        "difficulty": 1
    }
}
```
## Endpoint Testing
**Route test**
Ensure you are in the `\backend` directory. The test runs in a sequential order and you might have to persist the mock data again as shown below if you intend to run the tests more than once
run:
```bash
dropdb trivia_test
createdb trivia_test
psql trivia_test < trivia.psql
python test_flaskr.py
```
## Author
**Udacity ALX Transform** An udacity nanodegree programme in collaboration with ALX-T to develop and train fullstack developers
**Daramola Tobi** (tobi_daramola@yahoo.com)is an aspiring developer passionate about building real apps to enhance his learning and sharpen his programming skills.


