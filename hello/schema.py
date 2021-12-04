import logging

import graphene
from graphene import relay
from graphene_django import DjangoObjectType  # type: ignore
from graphene_django.filter import DjangoFilterConnectionField  # type: ignore
from graphql_auth import UserStatus, mutations  # type: ignore
from graphql_auth.schema import MeQuery, UserQuery  # type: ignore
from graphql_jwt.decorators import login_required  # type: ignore

from .models import AidRequest


class AidRequestType(DjangoObjectType):
    class Meta:
        model = AidRequest
        interfaces = (relay.Node,)
        fields = (
            'id',
            'created_at',
            'what_is_needed',
            'completed',
            'who_is_it_for_freeform_text',
            'who_recorded_it_username',
            'zip_code',
        )
        filter_fields = {"id": ["exact"]}


class AidRequestsConnection(graphene.Connection):
    class Meta:
        node = AidRequestType


class Query(MeQuery, graphene.ObjectType):
    aid_requests = DjangoFilterConnectionField(AidRequestType)


class CreateAidRequest(graphene.Mutation):
    class Arguments:
        who_wants_it = graphene.String()
        what_is_it = graphene.String()

    request = graphene.Field(AidRequestType)

    # @login_required
    def mutate(self, info, who_wants_it, what_is_it):
        old_get_email_context = UserStatus.get_email_context

        def new_get_email_context(self, info, path, action, **kwargs):
            values = old_get_email_context(self, info, path, action, **kwargs)
            logger = logging.getLogger('testlogger')
            logger.info('Values returned: ' + repr(values))
            return values

        UserStatus.get_email_context = new_get_email_context
        logger = logging.getLogger('testlogger')
        logger.info('hello world')
        return
        # new_request = AidRequest(
        #     what_is_needed=what_is_it,
        #     zip_code=1,
        #     who_is_it_for_freeform_text=who_wants_it,
        #     who_recorded_it_username=info.context.user.username,
        # )
        # new_request.save()
        # return CreateAidRequest(request=new_request)


class UpdateIsRequestComplete(graphene.Mutation):
    class Arguments:
        id = graphene.ID()
        new_value = graphene.Boolean()

    request = graphene.Field(AidRequestType)

    @login_required
    def mutate(self, info, id, new_value):
        (type_, id) = relay.Node.from_global_id(id)
        request = AidRequest.objects.get(('id', int(id)))
        request.completed = new_value
        request.save()
        return UpdateIsRequestComplete(request=request)


class AuthMutation(graphene.ObjectType):
    register = mutations.Register.Field()
    token_auth = mutations.ObtainJSONWebToken.Field()


class Mutation(AuthMutation, graphene.ObjectType):
    create_aid_request = CreateAidRequest.Field()
    update_is_request_complete = UpdateIsRequestComplete.Field()


schema = graphene.Schema(query=Query, mutation=Mutation)
