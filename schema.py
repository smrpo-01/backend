import graphene
from graphene import relay
from graphene_sqlalchemy import SQLAlchemyConnectionField, SQLAlchemyObjectType
from models import User as UserModel
from models import Project as ProjectModel


class User(SQLAlchemyObjectType):

    class Meta:
        model = UserModel
        interfaces = (relay.Node,)


class Project(SQLAlchemyObjectType):

    class Meta:
        model = ProjectModel
        interfaces = (relay.Node,)


class Query(graphene.ObjectType):
    node = relay.Node.Field()
    users = graphene.List(User)
    projects = graphene.List(Project)

    def resolve_users(self, info):
        return User.get_query(info)

    def resolve_projects(self, info):
        return Project.get_query(info)


schema = graphene.Schema(query=Query, types=[User, Project])