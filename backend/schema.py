import graphene
import app.schemas.board_schema
import app.schemas.card_schema
import app.schemas.project_schema
import app.schemas.team_schema
import app.schemas.user_schema
import app.schemas.mail_schema


class Queries(
    app.schemas.board_schema.BoardQueries,
    app.schemas.card_schema.CardQueries,
    app.schemas.project_schema.ProjectQueries,
    app.schemas.team_schema.TeamQueries,
    app.schemas.user_schema.UserQueries,
    app.schemas.mail_schema.MailQueries,
    graphene.ObjectType
):
    pass


class Mutations(
    app.schemas.board_schema.BoardMutations,
    app.schemas.card_schema.CardMutations,
    app.schemas.project_schema.ProjectMutations,
    app.schemas.team_schema.TeamMutations,
    app.schemas.user_schema.UserMutations,
    graphene.ObjectType
):
    pass


schema = graphene.Schema(query=Queries, mutation=Mutations)