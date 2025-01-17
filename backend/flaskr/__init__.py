from crypt import methods
import os
from sre_parse import CATEGORIES
from unicodedata import category
from flask import Flask, request, abort, jsonify
from flask_sqlalchemy import SQLAlchemy
from flask_cors import CORS
import random

from models import setup_db, Question, Category

QUESTIONS_PER_PAGE = 10

def create_app(test_config=None):
    # create and configure the app
    app = Flask(__name__)
    setup_db(app)
    
    """
    @TODO: Set up CORS. Allow '*' for origins. Delete the sample route after completing the TODOs
    """
    #i made some changes to the frontend and updated request url by adding api
    cors = CORS(app, resources={r"/api/*": {"origins": "*"}})

    """
    @TODO: Use the after_request decorator to set Access-Control-Allow
    """
    # indicate which HTTP headers can be used when making the actual request.
    #header specifies the method or methods allowed when accessing the resource
    @app.after_request
    def after_request(response):
        response.headers.add('Access-Control-Allow-Headers', 'Content-Type,Authorization,true')
        response.headers.add('Access-Control-Allow-Methods', 'GET,PATCH,POST,DELETE,OPTIONS')
        return response

    """
    @TODO:
    Create an endpoint to handle GET requests
    for all available categories.
    """
    @app.route('/api/categories', methods=['GET'])
    def retrieve_categories():
        try:
            categories = Category.query.all()
            categories_dictionary = {}

            for category in categories:
                categories_dictionary[category.id] = category.type


            return jsonify({
                "success": True,
                "categories": categories_dictionary,
                "total_categories": len(categories)
            })
        except:
            abort(500)

    """
    @TODO:
    Create an endpoint to handle GET requests for questions,
    including pagination (every 10 questions).
    This endpoint should return a list of questions,
    number of total questions, current category, categories.

    TEST: At this point, when you start the application
    you should see questions and categories generated,
    ten questions per page and pagination at the bottom of the screen for three pages.
    Clicking on the page numbers should update the questions.
    """

    @app.route('/api/questions', methods=['GET'])
    def retrieve_questions():
        try:
            page = request.args.get('page', 1, type=int)
            start = (page-1)*QUESTIONS_PER_PAGE
            end = start + QUESTIONS_PER_PAGE
            questions = Question.query.all()
            formatted_questions = [question.format() for question in questions]
            categories = Category.query.all()
            categories_dictionary = {}

            for category in categories:
                categories_dictionary[category.id] = category.type

            return jsonify({
                "success": True,
                "questions": formatted_questions[start:end],
                "total_questions": len(formatted_questions),
                "categories":categories_dictionary
            })
        except:
            # This handles sending a request to the server whic it does not kmow how to handle.
            abort(500)

    """
    @TODO:
    Create an endpoint to DELETE question using a question ID.

    TEST: When you click the trash icon next to a question, the question will be removed.
    This removal will persist in the database and when you refresh the page.
    """
    @app.route('/api/questions/<int:question_id>', methods=['DELETE'])
    def delete_question(question_id):

        question = Question.query.filter(question.id == question_id).one_or_none()

        if question in None:
            abort(404)
        # The method for deleting a question has been created and is available in models.py file
        question.delete()

        return jsonify({
            "success":True,
            "message": 'question id % was deleted' %question_id
        })
    """
    @TODO:
    Create an endpoint to POST a new question,
    which will require the question and answer text,
    category, and difficulty score.

    TEST: When you submit a question on the "Add" tab,
    the form will clear and the question will appear at the end of the last page
    of the questions list in the "List" tab.
    """

    @app.route('/api/questions', methods=['POST'])
    def post_question():
        try:
            data = request.get_json()

            question = data.get('question')
            answer_text = data.get('answer')
            category = data.get('category')
            difficulty_score = data.get('difficulty')

            question_posted = Question(question=question ,answer=answer_text, category=category, difficulty=difficulty_score)
            # The method for posting a new question has been created and is available in models.py file
            question_posted.insert()
            return jsonify({
                "success": True,
                "message": "Question successfuly added"
            })
        except:
            abort(422)
    """
    @TODO:
    Create a POST endpoint to get questions based on a search term.
    It should return any questions for whom the search term
    is a substring of the question.

    TEST: Search by any phrase. The questions list will update to include
    only question that include that string within their question.
    Try using the word "title" to start.
    """
    @app.route('/api/questions/search', methods=['POST'])
    def search_question():
        try:
            data = request.get_json()
        
            search = data.get('searchTerm')
            result = Question.query.filter(Question.question.ilike("%" + search + "%")).all()
            #sometimes a serach returns nothing in this case i need to test if there is any results from the search , if not abort()

            if len(result) ==0:
                abort(404)

            page = request.args.get('page', 1, type=int)
            start = (page-1)*QUESTIONS_PER_PAGE
            end = start + QUESTIONS_PER_PAGE
            formatted_questions = [question.format() for question in result]

            return jsonify({
                "success": True,
                "questions":formatted_questions[start:end],
                "total_questions": len(formatted_questions)
        })
        except:
            abort(500)

    """
    @TODO:
    Create a GET endpoint to get questions based on category.

    TEST: In the "List" tab / main screen, clicking on one of the
    categories in the left column will cause only questions of that
    category to be shown.
    """
    @app.route('/api/categories/<int:category_id>/questions')
    def questions_by_category(category_id):
        category = Category.query.filter(Category.id == category_id).one_or_none()
        questions = Question.query.filter(Question.category ==category_id).one_or_none()

        if category is None:
            abort(404)
        elif questions is None:
            abort(404)
        else:
            try:
                page = request.args.get('page', 1, type=int)
                start = (page-1)*QUESTIONS_PER_PAGE
                end = start + QUESTIONS_PER_PAGE
                formatted_questions = [question.format() for question in questions]

                return jsonify({
                    "success":True,
                    "questions":formatted_questions[start:end],
                    "total_questions":len(questions),
                    "category":category.format()
                })
            except:
                abort(500)

    """
    @TODO:
    Create a POST endpoint to get questions to play the quiz.
    This endpoint should take category and previous question parameters
    and return a random questions within the given category,
    if provided, and that is not one of the previous questions.

    TEST: In the "Play" tab, after a user selects "All" or a category,
    one question at a time is displayed, the user is allowed to answer
    and shown whether they were correct or not.
    """
    @app.route('/api/quizzes', methods=['POST'])
    def play_the_quiz():
        data = request.get_json()

        # category and previous question parameters
        previous_question = data.get('previous_question')
        category = data.get('category')

        if previous_question is None:
            abort(422)
        elif category is None:
            abort(422)

        else:
            category_id = category.get('id')
            if category_id == 0:
                questions = Question.query.all()
                format_questions = [question.format() for question in questions]
                question = random.choice(format_questions)

                return jsonify({
                    'success':True,
                    'question':question.format()
                })

            else:
                questions = Question.query.filter(Question.category == category_id)
                format_questions = [question.format() for question in questions]

                while len(previous_question) < len(format_questions):
                    if Question.id not in previous_question:
                        return jsonify({
                            'success':True,
                            'question':random.choice(format_questions)
                        })
                    else:
                        return jsonify({
                            'success':False
                        })
        

    """
    @TODO:
    Create error handlers for all expected errors
    including 404 and 422.
    """
    @app.errorhandler(404)
    def not_found(error):
        return jsonify({
            "success": False,
            "error": 404,
            "message": "Resourse not found"
        }),404

    @app.errorhandler(422)
    def unprocessable(error):
        return jsonify({
            "success": False,
            "error": 422,
            "message": "Unprocessable Entity"
        }),422

    @app.errorhandler(400)
    def bad_request(error):
        return jsonify({
            "success": False,
            "error": 400,
            "message": "Bad Request"
        }),400

    @app.errorhandler(405)
    def method_not_allowed(error):
        return jsonify({
            "success": False,
            "error": 405,
            "message": "Method Not Allowed"
        }),405

    @app.errorhandler(500)
    def internal_server_error(error):
        return jsonify({
            "success": False,
            "error": 500,
            "message": "Internal Server Error"
        }),500

    return app

