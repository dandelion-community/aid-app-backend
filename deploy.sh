#!/bin/bash

APP_NAME=$1

heroku run -a $APP_NAME python manage.py migrate auth 
heroku run -a $APP_NAME python manage.py migrate 

# Looks like this one is not needed -- staging deployment rendered
# css fine on the admin UI without running this command.
# heroku run -a $APP_NAME python manage.py collectstatic

# Only needed for new deployments.
# heroku run -a $APP_NAME python manage.py createsuperuser