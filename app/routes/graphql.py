from flask import Blueprint, request
from flask_graphql import GraphQLView
from app.graphql.schema import schema
from app.middleware.auth import verify_token

graphql_blueprint = Blueprint('graphql', __name__)


class AuthenticatedGraphQLView(GraphQLView):
    decorators = [verify_token]

    def get_context(self):
        return {
            'user_id': getattr(request, 'user_uid', None)
        }


graphql_blueprint.add_url_rule(
    '/graphql',
    view_func=AuthenticatedGraphQLView.as_view(
        'graphql',
        schema=schema,
        graphiql=True
    )
)