from sqlalchemy import Table, Integer, ForeignKey, Column, String
from sqlalchemy.orm import backref, relationship
from database import Base


projects = Table(
    'projects',
    Base.metadata,
    Column('user_id', Integer, ForeignKey('user.id'), primary_key=True),
    Column('project_id', Integer, ForeignKey('project.id'), primary_key=True)
)


class User(Base):
    __tablename__ = 'user'
    id = Column(Integer, primary_key=True)
    email = Column(String, unique=True, nullable=False)
    name = Column(String, nullable=False)
    password = Column(String, nullable=False)


class Project(Base):
    __tablename__ = 'project'
    id = Column(Integer, primary_key=True)
    name = Column(String, nullable=False)
    project_members = relationship('User', secondary=projects, backref=backref('projects', lazy=True))