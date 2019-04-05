import jwt
import os

from django.contrib.auth import authenticate

from .models import User
from .service import redis_methods
from self import self
from django.contrib.auth.models import User




def my_login_required(function):
    def wrap(request, *args, **kwargs):
        print("Laxman")
        token=redis_methods.get_token(self, 'token')
        print("Laxman Token", token)
        # token = request.META.get('HTTP_AUTHORIZATION')
        token_decode=jwt.decode(token,'secret_key',algorithms=['HS256'])
        # token_decode = jwt.decode(token, os.getenv("SIGNATURE"), algorithms=['HS256'])
        print("TOKEN DECODE", token_decode)
        uname = token_decode.get('username')
        password =token_decode.get('password')
        print("mymailid", uname)
        print("mypassword", password)
        user= User.objects.get(username=uname)
        passw =user.email
        print("namma",passw)
        user_id=user.id  # getting user id
        print("Laxman ID", user_id)
        request.user_id = user_id
        print("***", user_id)
        user = authenticate(username=user, password=password)

        return function(request, *args, **kwargs)
    return wrap
