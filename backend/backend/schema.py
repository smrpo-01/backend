import graphene
import app.schema
import app.schemas.team_schema


class Queries(
    app.schema.Query,
    app.schemas.team_schema.Query,
    graphene.ObjectType
):
    pass


class Mutations(
    app.schema.Mutation,
    app.schemas.team_schema.Mutation,
    graphene.ObjectType
):
    pass


schema = graphene.Schema(query=Queries, mutation=Mutations)