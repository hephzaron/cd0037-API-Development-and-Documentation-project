from csv import DictWriter
import os
import unittest
import json
from flask_sqlalchemy import SQLAlchemy
from decouple import config

from flaskr import create_app
from models import setup_db, Question, Category

TEST_DATABASE_NAME = config('TEST_DATABASE_NAME')
TEST_DATABASE_URI = config('TEST_DATABASE_URI')


class SequentialTestLoader(unittest.TestLoader):
    '''
    A class to load test in sequential order overwriting the default loader in alphabetical order.
    It inherits from parent class unittest.TestLoader
    ...
    Methods
    -------
    getTestCaseNames(self, testCaseClass):
        get the test case names sorted in a sequential order
        Returns:
            testcase_names (list): a list of test cases within the file
    '''
    def getTestCaseNames(self, testCaseClass):
        testcase_names = super().getTestCaseNames(testCaseClass)
        testcase_methods = list(testCaseClass.__dict__.keys())
        testcase_names.sort(key=testcase_methods.index)
        return testcase_names

class TriviaTestCase(unittest.TestCase):
    '''
    A class to represent the trivia test case

    ...

    Attributes
    ----------
    app : Flask
        an instance of flask app
    client : FlaskClient
        an instance of flask client
    database_name : str
        name of test database
    database_path : str
        URI of database path

    Methods
    -------
    setUp(self):
        define test variables and initialize app.
    tearDown(self):
        executes after test cases
    test_get_categories(self):
        test the get_cateories route
    test_get_questions(self):
        test the get_questions route
    test_get_by_category(self):
        test the get_by_category route
    test_delete_question(self):
        test the route to delete a question
    test_404_if_question_to_delete_does_not_exist(self):
        test if question to delete does noy exist
    '''

    def setUp(self):
        '''
        Define test variables and initialize app
        '''
        self.app = create_app()
        self.client = self.app.test_client
        self.database_name = TEST_DATABASE_NAME
        self.database_path = TEST_DATABASE_URI
        setup_db(self.app, self.database_path)

        self.new_question = {
            'question': 'Who are the sponsors of Udacity Fullstack Web-development programme ?',
            'answer': 'ALX-T',
            'category': 4,
            'difficulty': 1
            }

        self.errored_question = {
            'question': 'Who are the sponsors of Udacity Fullstack Web-development programme ?',
            'answer': 'ALX-T',
            'category': 'Science',
            'difficulty': 1
            }

        # binds the app to the current context
        with self.app.app_context():
            self.db = SQLAlchemy()
            self.db.init_app(self.app)
            # create all tables
            self.db.create_all()

    def tearDown(self):
        '''Executed after reach test'''
        pass

    """
    TODO
    Write at least one test for each test for successful operation and for expected errors.
    """
    def test_get_categories(self):
        '''
        Tests a returned response of categories
            Parameters:
                self: TriviaTestCase
            Returns:
                None
        '''
        response = self.client().get('/categories')
        data = response.get_json()
        self.assertEqual(response.status_code, 200)
        self.assertEqual(len(data['categories'].keys()), 6)
        self.assertEqual(data['success'], True)
        self.assertIsInstance(data['categories'], dict)

    def test_get_questions(self):
        '''
        Tests a returned response object of paginated questions
            Parameters:
                self: TriviaTestCase
            Returns:
                None
        '''
        response = self.client().get('/questions')
        data = response.get_json()
        self.assertEqual(response.status_code, 200)
        self.assertEqual(data['success'], True)
        self.assertEqual(len(data['questions']), 10)
        self.assertTrue(data['current_category'])
        self.assertIsInstance(data['categories'], dict)

    def test_get_paginated_questions(self):
        '''
        Tests a returned response object of paginated questions
            Parameters:
                self: TriviaTestCase
            Returns:
                None
        '''
        response = self.client().get('/questions?page=2')
        data = response.get_json()
        self.assertEqual(response.status_code, 200)
        self.assertEqual(data['success'], True)
        self.assertEqual(len(data['questions']), 9)
        self.assertTrue(data['current_category'])
        self.assertIsInstance(data['categories'], dict)

    def test_get_by_category(self):
        '''
        Tests a returned response object of questions in a particular catgeory
            Parameters:
                self: TriviaTestCase
            Returns:
                None
        '''
        response = self.client().get('/categories/1/questions')
        data = response.get_json()
        self.assertEqual(response.status_code, 200)
        self.assertEqual(data['success'], True)
        self.assertEqual(data['total_questions'], 3)
        self.assertEqual(data['current_category'],'Science')

    def test_404_if_category_does_not_exist(self):
        '''
        Tests a returned error 404 response object if category does not exist
            Parameters:
                self: TriviaTestCase
            Returns:
                None
        '''
        response = self.client().get('/categories/20/questions')
        data = response.get_json()
        self.assertEqual(response.status_code, 404)
        self.assertEqual(data['success'], False)
        self.assertEqual(data['message'], "Resource not found")
        self.assertEqual(data['error'], 404)

    def test_delete_question(self):
        '''
        Tests delete a question route
            Parameters:
                self: TriviaTestCase
            Returns:
                None
        '''
        response = self.client().delete('/questions/19')
        data = response.get_json()
        self.assertEqual(response.status_code, 200)
        self.assertEqual(data['success'], True)
        self.assertEqual(data['id'], 19)
        self.assertEqual(data['message'], 'Question ID: 19 deleted successfully')


    def test_404_if_question_to_delete_does_not_exist(self):
        '''
        Tests if question to delete does not exists
            Parameters:
                self: TriviaTestCase
            Returns:
                None
        '''
        response = self.client().delete('/questions/19')
        data = response.get_json()
        self.assertEqual(response.status_code, 404)
        self.assertEqual(data['success'], False)
        self.assertEqual(data['message'], 'Resource not found')

    def test_create_question(self):
        '''
        Tests create a question route
            Parameters:
                self: TriviaTestCase
            Returns:
                None
        '''
        response = self.client().post('/questions', json=self.new_question)

        data = response.get_json()
        self.assertEqual(response.status_code, 201)
        self.assertTrue(data['success'])
        self.assertEqual(data['message'], 'Question was successfully created')

    def test_400_if_question_cannot_be_created(self):
        '''
        Tests if question cannot be be created
            Parameters:
                self: TriviaTestCase
            Returns:
                None
        '''
        response = self.client().post('/questions', json=self.errored_question)
        data = response.get_json()
        self.assertEqual(response.status_code, 400)
        self.assertEqual(data['success'], False)
        self.assertEqual(data['message'], 'Bad request')


# Make the tests conveniently executable
if __name__ == "__main__":
    unittest.main(testLoader = SequentialTestLoader(),verbosity=2)