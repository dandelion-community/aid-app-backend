import logging

from django.http import HttpResponse
from django.shortcuts import render
from graphql_auth import UserStatus, mutations  # type: ignore


# Create your views here.
def index(request):
    # return HttpResponse('Hello from Python!')
    return render(request, "index.html")


def db(request):
    return render(request, "db.html", {"greetings": []})
