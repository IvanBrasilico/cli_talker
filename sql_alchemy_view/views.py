''' Demonstrates the use of Context_App hanging to allow 
conversational context on access to a DataBase'''
import json
import os
import shlex
from sqlalchemy import create_engine
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy import Column, Integer, String
from sqlalchemy import ForeignKey
from sqlalchemy.orm import relationship, backref, sessionmaker

from botteryapp import app

path = os.path.dirname(os.path.abspath(__file__))

engine = create_engine('sqlite:////' + path + '/notebooks.db')
Base = declarative_base()
Base.metadata.drop_all(engine)
Base.metadata.create_all(engine)

Session = sessionmaker(bind=engine)
session = Session()


class Notebook(Base):
    """Parent Class. Designates a Collection of Notes"""
    __tablename__ = 'notebooks'
    id = Column(Integer, primary_key=True)
    name = Column(String(20), unique=True)

    def __init__(self, name):
        self.name = name


class Note(Base):
    """Just a simple note"""
    __tablename__ = 'notes'
    id = Column(Integer, primary_key=True)
    notebook_id = Column(Integer, ForeignKey('notebooks.id'))
    notebook = relationship("Notebook", back_populates="notes")
    title = Column(String(20), unique=True)
    text = Column(String(200))

    def __init__(self, notebook, title, text):
        self.notebook_id = notebook.id
        self.title = title
        self.text = text


Notebook.notes = relationship(
    "Note", order_by=Note.id, back_populates="notebook")


def sql_view(message):
    '''No rules mapping route, all routes "hard-coded"
    It could be made an object like RESTWaiter, to process "orders"
    and forward to a sql_alchemy object'''
    app.hang_in(message)
    words = shlex.split(message.text)
    command = words[0]
    params = None
    result = _(
        'Sorry. I cannot understand you. Type notebook for a list of options.')
    if len(words) > 1:
        params = words[1:]
    if command == 'notebook':
        result = _('Welcome to notebooks Application! \n'
                   'Type "list" to view your notebooks \n'
                   'Type "add" "name" to add a notebook \n'
                   'Type "open" "name" to open a notebook \n'
                   'Type "exit" to get out off application \n')
        if params:
            if params[0] in ['list', 'open', 'add']:
                command = params[0]
                if len(params) > 1:
                    params = params[1:]
                else:
                    params = []

    if command == 'list':
        notebooks = session.query(Notebook).all()
        result = [str(n.id) + ' - ' + n.name for n in notebooks]
        result = '\n'.join(result)
    elif command == 'open':
        if params:
            notebook = session.query(Notebook).filter(
                Notebook.name == params[0]).first()
            if notebook is None:
                result = 'Notebook ' + params[0] + ' não encontrado'
            else:
                result = 'Notebook ' + str(notebook.id) + ' ' + notebook.name + \
                    ' opened!'
        else:
            result = _('Error! Parameter "name" not entered.')
    elif command == 'add':
        if params:
            notebook = Notebook(params[0])
            result = 'Notebook ' + notebook.name + \
                     ' added!'
            session.add(notebook)
            session.commit()
        else:
            result = _('Error! Parameter "name" not entered.')
    elif command == 'exit':
        app.hang_out(message)
        result = _('Exiting...')

    return json.dumps(result)


def input_example(message):
    # app.input(message, name, prompt, valid_values=[]) ->
    #   Creates an name entry in a OrderedDict with a tuple
    #   (prompt, valid_values)
    # user_session ->
    #   dict with returned user inputs
    if not app.input_queue:
        app.hang_in(message)
        app.input(message, 'name', 'Enter Project Name:')
        app.input(message, 'language', 'Enter Project Language: ',
                  ['python2', 'python3'])
        app.input(message, 'url', 'Enter Project site:')
        app.input(message, 'priority', 'Enter Project priority:',
                  ['insane', 'medium', 'dontmatter'])
        return app.print_next_input(message)
    stay, response = app.next_input_queue(message)
    if stay:
        return response
    # Save project and exit view
    app.hang_out(message)
    return 'Project created: ' + response
