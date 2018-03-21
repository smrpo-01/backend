import graphene
import app.schema


class Queries(
    app.schema.Query,
    graphene.ObjectType
):
    dummy = graphene.String()


schema = graphene.Schema(query=Queries)