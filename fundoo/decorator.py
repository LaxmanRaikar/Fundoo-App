import jwt
import os
from .models import User




def my_login_required(function):
    def wrap(request, *args, **kwargs):
        token = request.META.get('HTTP_AUTHORIZATION')
        token_decode = jwt.decode(token, os.getenv("SIGNATURE"), algorithms=['HS256'])
        uname = token_decode.get('username')
        user_id = User.objects.get(username=uname)
