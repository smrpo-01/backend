from sqlalchemy import create_engine
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import scoped_session, sessionmaker

engine = create_engine('sqlite:///database.sqlite3', convert_unicode=True)
db_session = scoped_session(sessionmaker(autocommit=False,
                                         autoflush=False,
                                         bind=engine))
Base = declarative_base()
Base.query = db_session.query_property()


def init_db():
    from models import User, Project
    Base.metadata.drop_all(bind=engine)
    Base.metadata.create_all(bind=engine)

    u1 = User(email='user1@demo.com', name='U1', password='demodemo1')
    db_session.add(u1)
    u2 = User(email='user2@demo.com', name='U2', password='demodemo1')
    db_session.add(u2)
    u3 = User(email='user3@demo.com', name='U3', password='demodemo1')
    db_session.add(u3)

    p1 = Project(name='Project 1')
    p2 = Project(name='Project 2')

    p1.project_members.append(u1)
    p1.project_members.append(u2)
    p1.project_members.append(u3)
    db_session.add(p1)
    p2.project_members.append(u2)
    db_session.add(p2)

    db_session.commit()


