# import boto3
# from django.http import HttpResponse
# from django.shortcuts import render
#
#
from os import path

import boto3
import jwt
from django.contrib.auth.models import User
from django.http import HttpResponse
from django.shortcuts import render
from self import self
from .models import filepath

from fundoo.service import redis_methods


def uploadto_aws(request):

    if request.method == 'POST':
        uploaded_file = request.FILES['document']   # taking the file from local
        # uploaded_file = open(path, 'rb')  # image to upload with read access
        token = redis_methods.get_token(self, 'token')
        token_decode = jwt.decode(token, 'secret_key', algorithms=['HS256'])
        # token_decode = jwt.decode(token, os.getenv("SIGNATURE"), algorithms=['HS256'])
        print("TOKEN DECODE", token_decode)
        uname = token_decode.get('username')
        user = User.objects.get(username=uname)
        file_nam = str(user)       # taking file name in string
        file_name=file_nam+".jpg"
        print("filename", file_name)
        s3 = boto3.client('s3')             # using boto to upload file in aws s3 bucket
        
        s3.upload_fileobj(uploaded_file, 'fundooapp777', Key=file_name)

        # filename= request.POST.get('abc')
        # fi= filepath(filename=filename)
        return HttpResponse('IMAGE HAS BEEN UPLOADED')
    return render(request, 'fundoo/upload.html', {})
