import jwt
import os

from django.contrib.auth.decorators import user_passes_test
from django.core.exceptions import ObjectDoesNotExist
from django.http import HttpResponse

from .models import User
from .service import redis_methods
from self import self


def my_login_required(function):
    try:
        def wrap(request, *args, **kwargs):
            token=redis_methods.get_token(self, 'token') # gets the token from the redis cache
            print("get the  Token", token)
            # token = request.META.get('HTTP_AUTHORIZATION')
            token_decode = jwt.decode(token,'secret_key', algorithms=['HS256'])
            # decodes the jwt token and gets the value of user details
            print("TOKEN DECODE", token_decode)
            uname = token_decode.get('username')
            user = User.objects.get(username=uname)

            user_id = user.id  # getting user id
            print("Laxman ID", user_id)
            request.user_id = user_id
            print("***", user_id)
            if user_id:
                # if it is present then go to next stp
                return function(request, *args, **kwargs)
            else:
                raise PermissionError # raises the permision error
        return wrap
    except Exception as e:
        print(e)
        return HttpResponse('something bad happend ')

