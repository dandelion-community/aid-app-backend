import hello.views
from django.contrib import admin
from django.urls import include, path
from django.views.decorators.csrf import csrf_exempt
from graphene_django.views import GraphQLView  # type: ignore
from hello import views

admin.autodiscover()


# To add a new path, first import the app:
# import blog
#
# Then add the new path:
# path('blog/', blog.urls, name="blog")
#
# Learn more here: https://docs.djangoproject.com/en/2.1/topics/http/urls/

urlpatterns = [
    path("", hello.views.index, name="index"),
    path("admin/", admin.site.urls),
    path('accounts/', include('django_registration.backends.activation.urls')),
    path('accounts/', include('django.contrib.auth.urls')),
    path('activate/<str:activation_key>', views.activate, name="activate"),
    path("graphql", csrf_exempt(GraphQLView.as_view(graphiql=True))),
]
