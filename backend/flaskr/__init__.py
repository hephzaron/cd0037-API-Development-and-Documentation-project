import os
from flask import Flask, request, abort, jsonify
from flask_sqlalchemy import SQLAlchemy
from flask_cors import CORS, cross_origin
import random

from models import setup_db, Question, Category

QUESTIONS_PER_PAGE = 10

def paginate_questions(request, selected_questions):
    page = request.args.get("page", 1, type=int)
    start = (page - 1) * QUESTIONS_PER_PAGE
    end = start + QUESTIONS_PER_PAGE

    questions = [question.format() for question in selected_questions]
    current_questions = questions[start:end]

    return current_questions

def create_app(test_config=None):
    # create and configure the app
    app = Flask(__name__)
    setup_db(app)

    """
    @TODO: Set up CORS. Allow '*' for origins. Delete the sample route after completing the TODOs
    
    """
    CORS(app, resources={r"/api/*": {"origins": "*"}})

    """
    @TODO: Use the after_request decorator to set Access-Control-Allow
    """
    @app.after_request
    def after_request(response):
        response.headers.add(
            "Access-Control-Allow-Headers", "Content-Type,Authorization,true"
        )
        response.headers.add(
            "Access-Control-Allow-Methods", "GET, POST, PUT, PATCH, DELETE"
        )
        return response

    """
    @TODO:
    Create an endpoint to handle GET requests
    for all available categories.
    """
    @app.route('/categories')
    def get_categories():
        
        # Fetch an array of categories 
        category_arr = [
            category.format() for category in 
            Category.query.order_by(Category.type).all()
            ]
        
        # Convert an array of categories to a dictionary object
        category_dict = {}
        for object in category_arr:
            category_dict[str(object['id'])] = object['type']
            

        if len(category_arr) == 0:
            abort(404)

        return jsonify(
            {
                "success": True,
                "categories": category_dict
            }
        )

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
    @app.route('/questions')
    def get_questions():
        
        # Fetch an array of categories        
        category_arr = [
            category.format() for category in 
            Category.query.order_by(Category.type).all()
            ]
        
        # Convert an array of categories to a dictionary object
        category_dict = {}
        for object in category_arr:
            category_dict[str(object['id'])] = object['type']
            
        # Fetch all questions ordered by the category
        questions = Question.query.order_by(Question.category).all()
        
        # Paginate fetched questions in group of 10's
        selected_questions = paginate_questions(request, questions)

        if len(questions) == 0:
            abort(404)

        return jsonify(
            {
                'success': True,
                'questions': selected_questions,
                'total_questions': len(questions),
                'categories': category_dict,
                'current_category': category_dict[str(selected_questions[0]['category'])]
            }
        )        

    """
    @TODO:
    Create an endpoint to DELETE question using a question ID.

    TEST: When you click the trash icon next to a question, the question will be removed.
    This removal will persist in the database and when you refresh the page.
    """

    """
    @TODO:
    Create an endpoint to POST a new question,
    which will require the question and answer text,
    category, and difficulty score.

    TEST: When you submit a question on the "Add" tab,
    the form will clear and the question will appear at the end of the last page
    of the questions list in the "List" tab.
    """

    """
    @TODO:
    Create a POST endpoint to get questions based on a search term.
    It should return any questions for whom the search term
    is a substring of the question.

    TEST: Search by any phrase. The questions list will update to include
    only question that include that string within their question.
    Try using the word "title" to start.
    """

    """
    @TODO:
    Create a GET endpoint to get questions based on category.

    TEST: In the "List" tab / main screen, clicking on one of the
    categories in the left column will cause only questions of that
    category to be shown.
    """
    @app.route('/categories/<int:category_id>/questions')
    def get_by_category(category_id):
        
        # Get an array of questions by their category from questions table
        questions = [question.format() for question in 
                     Question.query.filter(Question.category==category_id).all()]
        
        # Fetch a category by it's id
        current_category_type = Category.query.filter(Category.id==category_id).one_or_none()
        category_type = current_category_type.format()['type']
        
        if (len(questions)==0 or current_category_type == None):
            abort(404)
            
        return jsonify(
            {
                'success': True,
                'questions': questions,
                'total_questions': len(questions),
                'current_category': category_type
            }
        )   

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

    """
    @TODO:
    Create error handlers for all expected errors
    including 404 and 422.
    """
    @app.errorhandler(404)
    def not_found(error):
        return (
            jsonify({
                "success": False,
                "error": 404,
                "message": "Resource not found"}),
            404
        )

    @app.errorhandler(422)
    def unprocessable_entity(error):
        return (
            jsonify({
                "success": False,
                "error": 422, 
                "message": "Unprocessable entity"}),
            422
        )

    return app

