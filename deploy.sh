#!/bin/bash

APP_NAME=$1

heroku run -a $APP_NAME python manage.py migrate auth 
heroku run -a $APP_NAME python manage.py migrate 
heroku run -a $APP_NAME python manage.py collectstatic
heroku run -a $APP_NAME python manage.py createsuperuser