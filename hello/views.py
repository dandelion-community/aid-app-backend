from django.contrib.auth import get_user_model
from django.template.response import TemplateResponse
from django_registration.backends.activation import \
    views as activation_views  # type: ignore
from graphql_auth.constants import TokenAction  # type: ignore
from graphql_auth.exceptions import UserAlreadyVerified  # type: ignore
from graphql_auth.models import UserStatus  # type: ignore
from graphql_auth.settings import \
    graphql_auth_settings as app_settings  # type: ignore
from graphql_auth.signals import user_verified  # type: ignore
from graphql_auth.utils import get_token_paylod  # type: ignore

UserModel = get_user_model()


def index(request):
    return TemplateResponse(request, 'index.html', {})


class CustomAccountActivate(activation_views.ActivationView):
    def activate(self, *args, **kwargs):
        """
        This custom class allows us to use a non-GraphQL view that
        returns an HTML page instead of a GraphQL response. This is
        useful for handling activation links in emails, since those
        will open in a browser. We achieve this by using the
        activation view from django_registration.

        However, since we're using graphql_auth to create the user,
        we end up with a slightly different implementation of
        how the access tokens are generated.

        When django_registration's ActivationView
        tries to validate the access token through `self.validate_key`,
        it fails because it was expecting just the username signed
        with the salt "registration" (from the setting REGISTRATION_SALT).

        Conversely, graphql_auth expects the auth token to be
        `{"action":"activation","username":username}` signed with the
        salt "django.core.signing" (the default salt for the signing
        library).

        While the salts can be configured to match through settings,
        the payloads can't. So instead, I'm creating a view that
        is *almost* the same as django_registration's activation
        view, but it uses graphql_auth's implementation of auth token
        validation.

        django_registration implementation: site-packages/django_registration/backends/activation/views.py
        graphql_auth implementation: site-packages/graphql_auth/models.py
        """
        token = kwargs.get("activation_key")
        payload = get_token_paylod(
            token, TokenAction.ACTIVATION, app_settings.EXPIRATION_ACTIVATION_TOKEN
        )
        user = UserModel._default_manager.get(**payload)
        user_status = UserStatus.objects.get(user=user)
        if user_status.verified is False:
            user_status.verified = True
            user_status.save(update_fields=["verified"])
            user_verified.send(sender=UserStatus, user=user)
        else:
            raise UserAlreadyVerified
        return user


activate = CustomAccountActivate.as_view()
