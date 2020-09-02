# Full Stack Trivia API Backend

## Getting Started

### Installing Dependencies

#### Python 3.7

Follow instructions to install the latest version of python for your platform in the [python docs](https://docs.python.org/3/using/unix.html#getting-and-installing-the-latest-version-of-python)

#### Virtual Enviornment

We recommend working within a virtual environment whenever using Python for projects. This keeps your dependencies for each project separate and organaized. Instructions for setting up a virual enviornment for your platform can be found in the [python docs](https://packaging.python.org/guides/installing-using-pip-and-virtual-environments/)

#### PIP Dependencies

Once you have your virtual environment setup and running, install dependencies by naviging to the `/backend` directory and running:

```bash
pip install -r requirements.txt
```

This will install all of the required packages we selected within the `requirements.txt` file.

##### Key Dependencies

- [Flask](http://flask.pocoo.org/)  is a lightweight backend microservices framework. Flask is required to handle requests and responses.

- [SQLAlchemy](https://www.sqlalchemy.org/) is the Python SQL toolkit and ORM we'll use handle the lightweight sqlite database. You'll primarily work in app.py and can reference models.py. 

- [Flask-CORS](https://flask-cors.readthedocs.io/en/latest/#) is the extension we'll use to handle cross origin requests from our frontend server. 

## Database Setup
With Postgres running, restore a database using the trivia.psql file provided. From the backend folder in terminal run:
```bash
psql trivia < trivia.psql
```

## Running the server

From within the `backend` directory first ensure you are working using your created virtual environment.

To run the server, execute:

```bash
export FLASK_APP=flaskr
export FLASK_ENV=development
flask run
```

Setting the `FLASK_ENV` variable to `development` will detect file changes and restart the server automatically.

Setting the `FLASK_APP` variable to `flaskr` directs flask to use the `flaskr` directory and the `__init__.py` file to find the application. 

## Tasks

One note before you delve into your tasks: for each endpoint you are expected to define the endpoint and response data. The frontend will be a plentiful resource because it is set up to expect certain endpoints and response data formats already. You should feel free to specify endpoints in your own way; if you do so, make sure to update the frontend or you will get some unexpected behavior. 

1. Use Flask-CORS to enable cross-domain requests and set response headers. 
2. Create an endpoint to handle GET requests for questions, including pagination (every 10 questions). This endpoint should return a list of questions, number of total questions, current category, categories. 
3. Create an endpoint to handle GET requests for all available categories. 
4. Create an endpoint to DELETE question using a question ID. 
5. Create an endpoint to POST a new question, which will require the question and answer text, category, and difficulty score. 
6. Create a POST endpoint to get questions based on category. 
7. Create a POST endpoint to get questions based on a search term. It should return any questions for whom the search term is a substring of the question. 
8. Create a POST endpoint to get questions to play the quiz. This endpoint should take category and previous question parameters and return a random questions within the given category, if provided, and that is not one of the previous questions. 
9. Create error handlers for all expected errors including 400, 404, 422 and 500. 

API END POINTS
GET '/categories'

Fetches a dictionary of categories in which the keys are the ids and the value is the corresponding string of the category
Request Argument: None
Returns: An object with a strig key, categories, that contains an object of id: category_string key:value pairs.
```
{
{'1' : "Science",
'2' : "Art",
'3' : "Geography",
'4' : "History",
'5' : "Entertainment",
'6' : "Sports"}

}

```

**GET /questions?page=<page_number>**

Fetches a dictionary of questions in which the keys are the answer, category, difficulty, id and question.
Request Arguments: Page Number
Returns: List of questions, number of total questions, current category and categories.
example Response: 
   
   ```
   { 
       "categories": 
            [ 
                { "id": 1, "type": "Science" }, 
                { "id": 2, "type": "Art" }, 
                { "id": 3, "type": "Geography" },
                 { "id": 4, "type": "History" }, 
                 { "id": 5, "type": "Entertainment" },
                  { "id": 6, "type": "Sports" } 
            ], 
        "current_category": null, 
        "questions": 
            [ 
                { "answer": "Agra", "category": 3, "difficulty": 2, "id": 15, "question": "The Taj Mahal is located in which Indian city?" },
                { "answer": "Escher", "category": 2, "difficulty": 1, "id": 16, "question": "Which Dutch graphic artist\u2013initials M C was a creator of optical illusions?" },
                { "answer": "Mona Lisa", "category": 2, "difficulty": 3, "id": 17, "question": "La Giaconda is better known as what?" },
                { "answer": "One", "category": 2, "difficulty": 4, "id": 18, "question": "How many paintings did Van Gogh sell in his lifetime?" },
                { "answer": "Jackson Pollock", "category": 2, "difficulty": 2, "id": 19, "question": "Which American artist was a pioneer of Abstract Expressionism, and a leading exponent of action painting?" },
                { "answer": "The Liver", "category": 1, "difficulty": 4, "id": 20, "question": "What is the heaviest organ in the human body?" },
                { "answer": "Alexander Fleming", "category": 1, "difficulty": 3, "id": 21, "question": "Who discovered penicillin?" },
                { "answer": "Blood", "category": 1, "difficulty": 4, "id": 22, "question": "Hematology is a branch of medicine involving the study of what?" },
                { "answer": "Scarab", "category": 4, "difficulty": 4, "id": 23, "question": "Which dung beetle was worshipped by the ancient Egyptians?" }, 
                { "answer": "Yaounde", "category": 3, "difficulty": 1, "id": 28, "question": "What is the capital of Cameroon" } ], 
        "success": true, 
        "total_questions": 20 
    }
   
   ```
   
    

**DELETE /questions/<question_id>**

Delete question from the questions list.
Request Arguments: Question Id
Returns: true if successfully deleted.
```
 Example Response 
 {"success":true}

```

 
 
**POST /questions**

Create a new question
Request Body: question, answer, difficulty and category.
Returns: true if successfully created.
```
Example Request Payload {"question":"test question","answer":"test answer","difficulty":"3","category":1}
Example Response 
{"success":true}

```


**POST /questions/search**

Searches for the questions
Request Arguments: Page Number
Request Body: search_data
Returns: List of questions, number of total questions and current category.

```
Example Request Payload 
    { "searchTerm":"what" } 
Example Response 
{
    "questions": [
        {
            "answer": "Cameroon",
            "category": "Soccer",
            "difficulty": 2,
            "id": 24,
            "question": "Which is the only team to play in every soccer World Cup tournament"
        }
    ],
    "success": true,
    "total_questions": 1
}
```

**GET /categories/<int:category_id>/questions**

To get questions based on category
Request Arguments: Category Id and Page Number.
Returns: List of questions, number of total questions, current category and categories.

```

Sample response
{
    "categories": [
        {
            "id": 1,
            "type": "Science"
        },
        {
            "id": 2,
            "type": "Art"
        },
        {
            "id": 3,
            "type": "Geography"
        },
        {
            "id": 4,
            "type": "History"
        },
        {
            "id": 5,
            "type": "Entertainment"
        },
        {
            "id": 6,
            "type": "Sports"
        }
    ],
    "current_category": {
        "id": 1,
        "type": "Science"
    },
    "questions": [
        {
            "answer": "The Liver",
            "category": "1",
            "difficulty": 4,
            "id": 20,
            "question": "What is the heaviest organ in the human body?"
        },
        {
            "answer": "Alexander Fleming",
            "category": "1",
            "difficulty": 3,
            "id": 21,
            "question": "Who discovered penicillin?"
        },
        {
            "answer": "Blood",
            "category": "1",
            "difficulty": 4,
            "id": 22,
            "question": "Hematology is a branch of medicine involving the study of what?"
        }
    ],
    "success": true,
    "total_questions": 3
}

```
**POST /quizzes**

To get questions to play the quiz.
Request Body: quiz_category and previous_questions.
Returns: Random questions within the given category. Example Request Payload {"previous_questions":[],"quiz_category":{"type":"Science","id":1}}

```
Example Response 
  {
    "question":
        {"answer":"Blood","category":1,"difficulty":4,"id":22,"question":"Hematology is a branch of medicine involving the study of what?"},
        "success":true
  }


```


## Testing
To run the tests, run
```
dropdb trivia_test
createdb trivia_test
psql trivia_test < trivia.psql
python test_flaskr.py
```