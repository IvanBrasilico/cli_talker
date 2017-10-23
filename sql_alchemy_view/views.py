''' Demonstrates the use of Context_App hanging to allow
conversational context on access to a DataBase'''
import json
import os
import shlex
from sqlalchemy import create_engine
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy import Column, Integer, String
from sqlalchemy import ForeignKey
from sqlalchemy.orm import relationship, sessionmaker

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


def notebook_view(message):
    '''No rules mapping route, all routes "hard-coded"
    It could be made an object like RESTWaiter, to process "orders"
    and forward to a sql_alchemy object'''
    words = shlex.split(message.text)
    command = words[0]
    params = None
    result = _(
        'Sorry. I cannot understand you. Type notebook for a list of options.')
    if len(words) > 1:
        params = words[1:]
    if command == 'notebook':
        app.hang_in(message)
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
                result = _('Notebook ') + params[0] + _(' not found')
            else:
                result = _('Notebook ') + str(notebook.id) + ' ' + notebook.name + \
                    _(' opened!')
                app.store_on_user_session(message.user.id,
                                          'notebookid', notebook.id)
                # app.redirect('note', result, messsage)
                result = result + app.hang_forward(message, 'note')

        else:
            result = _('Error! Parameter "name" not entered.')
    elif command == 'add':
        if params:
            notebook = Notebook(params[0])
            result = _('Notebook ') + notebook.name + \
                _(' added!')
            session.add(notebook)
            session.commit()
        else:
            result = _('Error! Parameter "name" not entered.')
    elif command == 'exit':
        app.hang_out(message)
        result = _('Exiting...')

    return json.dumps(result)


def note_view(message):
    notebookid = app.retrieve_from_user_session(message.user.id,
                                                'notebookid')
    if notebookid is None:
        return _('No notebook opened! Type "notebook" first')
    notebook = session.query(Notebook).filter(
        Notebook.id == notebookid
    ).first()
    if notebook is None:
        return _('Error! Notebook not found!')
    words = shlex.split(message.text)
    command = words[0]
    params = None
    result = _(
        'Sorry. I cannot understand you. Type note for a list of options.')
    if len(words) > 1:
        params = words[1:]
    if command == 'note':
        result = _('Welcome to notebook ') + notebook.name + '\n' + \
            _('Type "list" to view your notebook notes') + ' \n' + \
            _('Type "add" "title" "content" to add a note') + ' \n' + \
            _('Type "del" "name" to delete a note') + ' \n' + \
            _('Type "close" to close the notebook') + ' \n' + \
            _('Type "exit" to get out of application \n')
        if params:  # Process next command if exists
            if params[0] in ['list', 'del', 'add']:
                command = params[0]
                if len(params) > 1:
                    params = params[1:]
                else:
                    params = []

    if command == 'list':
        result = [n.title + ' - ' + n.text for n in notebook.notes]
        result = '\n'.join(result)
    elif command == 'del':
        if params:
            note = session.query(Note).filter(
                Note.title == params[0]).first()
            if note is None:
                result = _('Note ') + params[0] + _(' not found')
            else:
                session.delete(note)
                session.commit()
                result = _('Note ') + str(note.id) + ' ' + note.title + \
                    _(' deleted!')
        else:
            result = _('Error! Parameter "title" not entered.')
    elif command == 'add':
        if len(params) == 2:
            note = Note(notebook, params[0], params[1])
            result = _('Note ') + note.title + \
                (' added!')
            session.add(note)
            session.commit()
        else:
            if params:
                result = _('Error! Parameter 2 "content" not entered.')
            else:
                result = _('Error! No parameters entered.')

    elif command == 'close':
        app.hang_out(message)
        result = _('Closing notebook...')
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
