'''Tests for sql_alchemy view example'''
from sql_alchemy_view.views import Notebook, Note, Base, session, engine


def test_database():
    Base.metadata.drop_all(engine)
    Base.metadata.create_all(engine)
    session.commit()

    notebook = Notebook('TESTE')
    session.add(notebook)
    session.commit()

    note1 = Note(notebook, 'DOC1', 'Test of Note number 1')
    note2 = Note(notebook, 'DOC2', 'Test of Note number 2')
    session.add(note1)
    session.add(note2)
    session.commit()
    notebooks = session.query(Notebook).all()
    assert len(notebooks) == 1
    assert notebooks[0].name == "TESTE"
    notes = notebooks[0].notes
    assert len(notes) == 2
    assert notes[0].title == "DOC1"
    assert notes[1].title == "DOC2"
