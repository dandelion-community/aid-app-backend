import logging

from django.http import HttpResponse
from django.shortcuts import render
from graphql_auth import UserStatus, mutations  # type: ignore


# Create your views here.
def index(request):
    # return HttpResponse('Hello from Python!')
    old_get_email_context = UserStatus.get_email_context

    def new_get_email_context(self, info, path, action, **kwargs):
        values = old_get_email_context(self, info, path, action, **kwargs)
        logger = logging.getLogger('testlogger')
        logger.info('Values returned: ' + repr(values))
        return values

    UserStatus.get_email_context = new_get_email_context
    return render(request, "index.html")


def db(request):
    return render(request, "db.html", {"greetings": []})
