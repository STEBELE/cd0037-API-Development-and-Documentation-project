import os
import unittest
import json
from flask_sqlalchemy import SQLAlchemy

from flaskr import create_app
from models import setup_db, Question, Category


class TriviaTestCase(unittest.TestCase):
    """This class represents the trivia test case"""

    def setUp(self):
        """Define test variables and initialize app."""
        self.app = create_app()
        self.client = self.app.test_client
        self.database_name = "trivia_test"
        self.database_path = "postgres://{}/{}".format('localhost:5432', self.database_name)
        setup_db(self.app, self.database_path)

        # binds the app to the current context
        with self.app.app_context():
            self.db = SQLAlchemy()
            self.db.init_app(self.app)
            # create all tables
            self.db.create_all()
    
    def tearDown(self):
        """Executed after reach test"""
        pass

    # GET /api/categories 
    # test for successful operation
    def test_retrieve_categories(self):
        res = self.client('/api/categories')
        data = json.loads(res.data)

        self.assertEqual(res.status, 200)
        self.assertEqual(data['success'], True)
        self.assertEqual(len(data['categories']),4)
    
    # test for expected errors
    def test_404_no_category(self):
        res = self.client().get('/api/categories')
        data = json.loads(res.data)

        self.assertEqual(res.status_code, 404)
        self.assertEqual(data['success'], False)
        self.assertEqual(data['message'], 'Resourse not found')


    # GET /api/questions
    # test for successful operation
    def test_retrieve_questions(self):
        res = self.client('/api/questions')
        data = json.loads(res.data)

        self.assertEqual(res.status, 200)
        self.assertEqual(data['success'], True)
        self.assertEqual(len(data['questions']),4) 
        self.assertEqual(len(data['total_questions']),5)
        self.assertEqual(len(data['categories']),4)
    # test for expected errors
    def test_404_requesting_beyond_valid_page(self):
        res = self.client().get('/api/questions?page=1000')
        data = json.loads(res.data)

        self.assertEqual(res.status, 404)
        self.assertEqual(data['success'], False)
        self.assertEqual(len(data['questions']),4)


    # DELETE /api/questions/{question_id}
    # test for successful operation
    def test_delete_question(self):
        res = self.client().delete('/api/questions/1')
        data = json.loads(res.data)

        question = Question.query.filter(question.id == 1).one_or_none()

        self.assertEqual(res.status, 200)
        self.assertEqual(data['success'], True)
        self.assertEqual(len(data['message']),1) 
        self.assertEqual(len(data['total_questions']),5)
        self.assertEqual(len(data['categories']),4)

    # test for expected errors
    def test_422_if_question_does_not_exist(self):
        res = self.client().delete('/api/questions/1000')
        data = json.loads(res.data)

        self.assertEqual(res.status_code, 422)
        self.assertEqual(data['success'], False)
        self.assertEqual(data['message'], "unprocessable")

    # POST /api/questions
    # test for successful operation
    def test_post_question(self): 
        new_question = {
            'question': 'question',
            'answer': 'answer',
            'difficulty':3,
            'category':2
        }
        res = self.client().post('/api/questions', json=new_question)
        data = json.loads(res.data)

        self.assertEqual(res.status_code, 200)
        self.assertEqual(data['success'], True)
        self.assertEqual(data['message'])
    
    # test for expected errors
    def test_400_incomplete_post_question(self):
        new_question = {
            'question': '',
            'answer': ' ',
            'difficulty':3,
            'category':2
        }
        res = self.client().post('/api/questions', json=new_question)
        data = json.loads(res.data)

        self.assertEqual(res.status_code, 400)
        self.assertEqual(data['success'], False)
        self.assertEqual(data['message'], 'bad request')

    # GET /api/categories/{id}/questions'
    # test for successful operation
    def test_question_by_category(self):
        res = self.client().get('/api/categories/1/questions')
        data = json.loads(res.data)

        self.assertEqual(res.status_code, 200)
        self.assertEqual(data['questions'])
        self.assertEqual(data['total_questions'])
        self.assertEqual(data['category'])

    # test for expected errors
    def test_404_no_question_by_category(self):
        res = self.client().get('/api/categories/12/questions')
        data = json.loads(res.data)

        self.assertEqual(res.status_code, 404)
        self.assertEqual(data['success'], False)
        self.assertEqual(data['message'], 'Resourse not found')


    # POST /api/questions/search
    # test for successful operation
    def test_search_question(self): 
        search = {"searchTearm": "Anime"}
        res = self.client().post('/api/questions/search', json=search)
        data = json.loads(res.data)

        self.assertEqual(res.status_code, 200)
        self.assertEqual(data['success'], True)
        self.assertEqual(data['question'],1)

    # test for expected errors
    def test_422_no_search_tearm(self):
        search = {"searchTearm": " "}
        res = self.client().post('/api/questions/search', json=search)
        data = json.loads(res.data)

        self.assertEqual(res.status_code, 422)
        self.assertEqual(data['success'], False)
        self.assertEqual(data['message'], 'unprocessable')
    
    # POST /api/quizzes
    # test for successful operation
    def play_the_quiz(self): 
        previous_q = {"previous_question":[],
         "category": {'id':'1', 'type': 'literature'}}
        res = self.client().post('/api/quizzes', json=previous_q)
        data = json.loads(res.data)

        self.assertEqual(res.status_code, 200)
        self.assertEqual(data['success'], True)
        self.assertEqual(data['question'], True)
        self.assertEqual(data['message'])

    # test for expected errors
    def test_422_incomplete_input_play_the_quiz(self):
        previous_q = {"previous_question":[],
         "category": {'id':' 3'}}
        res = self.client().post('/api/quizzes', json=previous_q)
        data = json.loads(res.data)

        self.assertEqual(res.status_code, 422)
        self.assertEqual(data['success'], False)
        self.assertEqual(data['message'], 'unprocessable')

    """
    TODO
    Write at least one test for each test for successful operation and for expected errors.
    """


# Make the tests conveniently executable
if __name__ == "__main__":
    unittest.main()