# API Development and Documentation Final Project

## Trivia App

Udacity is invested in creating bonding experiences for its employees and students. A bunch of team members got the idea to hold trivia on a regular basis and created a webpage to manage the trivia app and play the game, but their API experience is limited and still needs to be built out.

That's where you come in! Help them finish the trivia app so they can start holding trivia and seeing who's the most knowledgeable of the bunch. This application can:

1. Display questions - both all questions and by category. Questions should show the question, category and difficulty rating by default and can show/hide the answer.
2. Delete questions.
3. Add questions and require that they include question and answer text.
4. Search for questions based on a text query string.
5. Play the quiz game, randomizing either all questions or within a specific category.

## About the Stack

### Backend

Flsask micro framework and sqlalcemy was used to build out the application. The application uses a postgresql database. The [backend](./backend/README.md) directory contains a completed Flask and SQLAlchemy server. You will work primarily in `__init__.py` to define your endpoints and can reference models.py for DB and SQLAlchemy setup. These are the files you'd want to edit in the backend:

1. `backend/flaskr/__init__.py`
2. `backend/test_flaskr.py`

> View the [Backend README](./backend/README.md) for more details.

### Frontend

 React has been used to build out the frontend of the application. The [frontend](./frontend/README.md) directory contains complete React frontend to consume the data from the Flask server. 

By making notes ahead of time, you will practice the core skill of being able to read and understand code and will have a simple plan to follow to build out the endpoints of your backend API.

> View the [Frontend README](./frontend/README.md) for more details.

How to Run the Backend
Step 1 - Start Postgres and set up the database and testing database
Click the button to start Postgres and set up the trivia and trivia_test databases:

Explore the database
You can enter the database with:


su - postgres bash -c "psql trivia"
Once you are inside the psql prompt, you can play around


\dt
SELECT * FROM categories;
SELECT * FROM questions LIMIT 5;
To exist postgres, run:


\q

Step 2 - Install the required packages
Navigate to the backend directory and run pip install


cd backend
pip3 install -r requirements.txt
Step 3. Start the backend server
Start the (backend) Flask server by running:


export FLASK_APP=flaskr
export FLASK_ENV=development
flask run
The server will restart automatically when changes are detected.

How to Run the Frontend
To run the frontend you'll need to open a new terminal. Go to File > New > Terminal

The dependencies are already installed in the workspace. If you need to install them again, navigate to the /frontend directory and run:


npm install
To start the app in development mode, navigate to the /frontend directory and run the start script:


cd frontend
npm start

GET '/api/categories'

Fetches a dictionary of categories in which the keys are the ids and the value is the corresponding string of the category
Request Arguments: None
Returns: An object with a single key, categories, that contains an object of id: category_string key: value pairs.

{
    "success": true,
    "categories": 
    {
    "1": "Science",
    "2": "Art",
    "3": "Geography",
    "4": "History",
    "5": "Entertainment",
    "6": "Sports"
    },
    "total_categories":2
}

GET '/api/questions'
Fetches a list of all questions. This endpoint returns a list of questions, number of total questions, current category, categories. The request inclused pagination for every 10 questions.

{
            "success": true,
            "questions": [
                {
                    "id": 1,
                    "question": "It can be cruel, poetic, or blind.But when it's denied, it's violence you may find",
                    "answer": "Justics",
                    "category": 3,
                    "difficulty": 3
                },
                {
                    "id": 2,
                    "question": "I Speak without a mouth and hear without ears. i have no body, but i come alive with wind. what am i?",
                    "answer":"An echo",
                    "category": 1,
                    "difficulty": 2
                }]
            "total_questions": 1,
            "categories": {
                '1' : "Science",
                '2' : "Art",
                '3' : "Geography",
                '4' : "History",
                '5' : "Entertainment",
                '6' : "Sports"
            },
            "current_category": None
        }

DELETE /api/questions/{question_id}
DELETEs a question using a question ID.This removal will persist in the database and when you refresh the page. an questiona-id argument is required. sample response

{
            "success":True,
            "message": 'question id 1 was deleted' 
        }

POST '/api/questions'
to POST a new question,which will require the question and answer text,category, and difficulty score.The requested question is a json object conatining key value pairs.
sample question

 {
            "question": "You measure my life in hours and i serve you by expiring. i'm quick when im thin and slow when im fat. The wind is my enemy. what am i?",
            "answer": "A candle",
            "category": 2,
            "difficulty": 3
        } 
 This endpoints returns success reposnse and a message. a sample response from the endpoint. 
{
                "success": True,
                "message": "Question added successfuly"
            }

POST 'api/questions/search'

Sends a post request in order to search for a specific question by search term
Request Body:
{
    'searchTerm': 'this is the term the user is looking for'
}

Returns: any array of questions, a number of totalQuestions that met the search term and the current category string
{
    'sucess': True
    'questions': [
        {
            'id': 1,
            'question': 'This is a question',
            'answer': 'This is an answer',
            'difficulty': 5,
            'category': 5
        },
    ],
    'totalQuestions': 100
}

GET 'api/categories/{id}/questions'

Fetches questions for a cateogry specified by id request argument
Request Arguments: id - integer
Returns: An object with questions for the specified category, total questions, and current category string
{
    'success':True,
    'questions': [
        {
            'id': 1,
            'question': 'This is a question',
            'answer': 'This is an answer',
            'difficulty': 5,
            'category': 4
        },
    ],
    'totalQuestions': 100,
    'category': 'History'
}

POST 'api/quizzes'

Sends a post request in order to get the next question
Request Body:
{
    'previous_questions': [1, 4, 20, 15]
    quiz_category': 'current category'
 }
Returns: a single new question object
{
    'sucess':True
    'question': {
        'id': 1,
        'question': 'This is a question',
        'answer': 'This is an answer',
        'difficulty': 5,
        'category': 4
    }
}

