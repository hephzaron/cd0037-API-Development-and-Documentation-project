'''
This file contains all models of the TriviaAPI database
'''
from sqlalchemy import Column, String, Integer
from flask_sqlalchemy import SQLAlchemy
from decouple import config

DATABASE_URI = config('DATABASE_URI')

SQLALCHEMY_TRACK_MODIFICATIONS = config('SQLALCHEMY_TRACK_MODIFICATIONS')
SECRET_KEY = config('SECRET_KEY')
SQLALCHEMY_ECHO = eval(config('SQLALCHEMY_ECHO'))

db = SQLAlchemy()

def setup_db(app, database_path=DATABASE_URI):
    '''
    Binds a flask application and a SQLAlchemy service
        Parameters:
            app (Flask(__name__)): an instance of flask app
            database_path (str): database uri
        Returns:
            None
    '''
    app.config["SQLALCHEMY_DATABASE_URI"] = database_path
    app.config["SQLALCHEMY_TRACK_MODIFICATIONS"] = SQLALCHEMY_TRACK_MODIFICATIONS
    app.config["SQLALCHEMY_ECHO"] = SQLALCHEMY_ECHO
    db.app = app
    db.init_app(app)
    db.create_all()


class Question(db.Model):
    '''
    A class to create model for questions table
    ...
    Parameters
    ----------
    db.Model (SQLAlchemy) : SQLAlchemy object

    Attributes
    ----------
    id : Integer
        question id
    question : String
        question
    answer : String
        answer to question
    category : Integer
        the section a question belongs to
    difficulty : Integer
        level of difficulty question belongs to
    '''
    __tablename__ = 'questions'

    id = Column(Integer, primary_key=True)
    question = Column(String, nullable=False)
    answer = Column(String, nullable=False)
    category = Column(Integer, nullable=False)
    difficulty = Column(Integer, nullable=False)

    def __init__(self, question, answer, category, difficulty):
        self.question = question
        self.answer = answer
        self.category = category
        self.difficulty = difficulty

    def insert(self):
        '''
        Adds a new question to the database
            Parameters:
                self
            Returns:
                None
        '''
        db.session.add(self)
        db.session.commit()

    def update(self):
        '''
        Updates a question already saved on the database
            Parameters:
                self
            Returns:
                None
        '''
        db.session.commit()

    def delete(self):
        '''
        Deletes a question from the database
            Parameters:
                self
            Returns:
                None
        '''
        db.session.delete(self)
        db.session.commit()

    def format(self):
        '''
        Return Question attributes
            Parameters:
                self
            Returns:
                id <int> : question id
                question <str> : question
                answer <str>: answer to question
                category <int>: category id question belongs to
                difficulty <int>: level of question difficulty
        '''
        return {
            'id': self.id,
            'question': self.question,
            'answer': self.answer,
            'category': self.category,
            'difficulty': self.difficulty
            }

class Category(db.Model):
    '''
    Creates model for categories table
        Parameters:
            db.Model (SQLAlchemy) : SQLAlchemy object
        Returns:
            None
    '''
    __tablename__ = 'categories'

    id = Column(Integer, primary_key=True)
    type = Column(String, nullable=False)

    def __init__(self, type):
        self.type = type

    def format(self):
        '''
        Return Category attributes
            Parameters:
                self
            Returns:
                id <int> : question id
                type <str> : question
        '''
        return {
            'id': self.id,
            'type': self.type
            }
