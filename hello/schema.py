import graphene
from graphene import relay
from graphene_django import DjangoObjectType  # type: ignore
from graphene_django.filter import DjangoFilterConnectionField  # type: ignore

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


class Query(graphene.ObjectType):
    aid_requests = DjangoFilterConnectionField(AidRequestType)


schema = graphene.Schema(query=Query)
