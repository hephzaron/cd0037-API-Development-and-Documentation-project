'''
This file contains all api endpoints implemented on the TriviaAPI

'''
import random
import os
from flask import Flask, request, abort, jsonify
from flask_sqlalchemy import SQLAlchemy
from flask_cors import CORS, cross_origin

from models import setup_db, Question, Category

QUESTIONS_PER_PAGE = 10

def paginate_questions(request_obj, selected_questions):
    '''
    Returns a list questions in chunks of 10 questions per page
        Parameters:
            request (flask.Request): A request object
            selected_questions (Array): An array of questions
        Returns:
            current_questions (Array): An array of paginated questions
    '''
    page = request_obj.args.get("page", 1, type=int)
    start = (page - 1) * QUESTIONS_PER_PAGE
    end = start + QUESTIONS_PER_PAGE

    questions = [question.format() for question in selected_questions]
    current_questions = questions[start:end]

    return current_questions

def create_app():
    '''
    Returns an instance of Flask app
        Parameters:
            None
        Returns:
            app (flask.Flask): In instance of Flask
    '''
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
        '''
        Returns a response object
            Parameters:
                response (Object): A response object
            Returns:
                response (Object): A response object
        '''
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
        '''
        An endpoint that fetches all available question categories
            Parameters:
                None
            Returns:
                <success> bool: successful transaction
                <categories> dict: a dictionary of categories with keys:<id> values: <type>
        '''

        # Fetch an array of categories
        category_arr = [
            category.format() for category in
            Category.query.order_by(Category.type).all()
            ]

        # Convert an array of categories to a dictionary object
        category_dict = {}
        for category in category_arr:
            category_dict[str(category['id'])] = category['type']


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
        '''
        An endpoint that fetches all available questions in pages
            Parameters:
                None
            Returns:
                <success> bool: successful transaction
                <questions> array: list of all paginated questions
                <total_questions> int: count of all questions in the database
                <categories> dict: a dictionary of categories with keys:<id> values: <type>
                <current_category> str: category of selected question
        '''
        # Fetch an array of categories
        category_arr = [
            category.format() for category in
            Category.query.order_by(Category.type).all()
            ]

        # Convert an array of categories to a dictionary object
        category_dict = {}
        for category in category_arr:
            category_dict[str(category['id'])] = category['type']

        # Fetch all questions ordered by the category
        questions = Question.query.order_by(Question.id).all()

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
    @app.route('/questions/<int:question_id>', methods=['DELETE'])
    def delete_question(question_id):
        '''
        An endpoint that deletes a question
            Parameters:
                question_id (int): id of question to be deleted
            Returns:
                <success> bool: successful transaction
                <message> str: response message on successful delete
                <id> int: id of deleted question
        '''
        # Get question with id: question_id
        question = Question.query.filter(Question.id==question_id).one_or_none()

        if question is None:
            abort(404)

        try:
            question.delete()
            return jsonify({
                'success': True,
                'id': question_id,
                'message': 'Question ID: {} deleted successfully'.format(question_id)
            })
        except:
            abort(500)

    """
    @TODO:
    Create an endpoint to POST a new question,
    which will require the question and answer text,
    category, and difficulty score.

    TEST: When you submit a question on the "Add" tab,
    the form will clear and the question will appear at the end of the last page
    of the questions list in the "List" tab.
    """
    @app.route('/questions', methods=['POST'])
    def create_question():
        '''
        An endpoint that creates a question
            Parameters:
                None
            Returns:
                <success> bool: successful transaction
                <message> str: response message on successful delete
        '''

        body = request.get_json()
        if not all(body.values()):
            abort(400)

        try:
            question = Question(**body)
            question.insert()

            return jsonify({
                'success': True,
                'message': 'Question was successfully created'
                }), 201

        except:
            abort(400)

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

        if current_category_type is not None:
            category_type = current_category_type.format()['type']

        if (len(questions)==0 or current_category_type is None):
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
    @app.errorhandler(400)
    def bad_request(error):
        return (
            jsonify({
                'success': False,
                'error': error,
                'message': 'Bad request'}),
            400
        )

    @app.errorhandler(404)
    def not_found(error):
        return (
            jsonify({
                'success': False,
                'error': 404,
                'message': 'Resource not found'}),
            404
        )

    @app.errorhandler(422)
    def unprocessable_entity(error):
        return (
            jsonify({
                'success': False,
                'error': 422,
                'message': 'Unprocessable entity'}),
            422
        )

    @app.errorhandler(500)
    def server_error(error):
        return (
            jsonify({
                'success': False,
                'error': 500,
                'message': "Server error"}),
            500
        )

    return app

