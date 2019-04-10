from email._header_value_parser import get_token

from django.contrib.auth import login, authenticate
from django.shortcuts import render,redirect
from django.http import HttpResponse, HttpResponseRedirect,JsonResponse
from django.urls import reverse
from django.views.decorators.csrf import csrf_exempt
from self import self


from rest_auth.serializers import UserDetailsSerializer

# from rest_auth.serializers import UserDetailsSerializer

from rest_framework.generics import CreateAPIView
from rest_framework.response import Response
from self import self

from .serializers import UserSerializer, RegistrationSerializer
from .forms import SignUpForm
from django.utils.encoding import force_text
from django.utils.http import  urlsafe_base64_decode
from django.template.loader import render_to_string
from .tokens import account_activation_token
from django.contrib.sites.shortcuts import get_current_site
from django.utils.http import urlsafe_base64_encode
from django.utils.encoding import force_bytes
from django.contrib.auth.models import User
from .service import redis_methods
from .models import Notes

from django.contrib.auth.decorators import login_required
from django.core.mail import EmailMessage
from django.core.cache import cache
from django.contrib import messages
import boto3
import jwt
from .decorator import my_login_required
from .service import redis_methods


# from json import json_dumps
import json


def user_login(request, self=None):        # this method is used to login the user
    # if this is a POST request we need to process the form data
    res = {
        'message': 'Something went wrong',
        'data': {},
        'success': False
    }
    try:
        username = request.POST.get('username')  # getting information from post method
        print("mynamezscmkcnks",username)

        # if username is None:
        #     raise Exception("invalid username")
        password = request.POST.get('password')  # getting information from post method
        # if password is None:
        #     raise Exception("invalid password")

        user = authenticate(username=username, password=password)  # authenticating fields values
        # print('username', user)  # printing the information
        if user:  # if a valid user
            if user.is_active:  # and user is active
                login(request, user)  # login into the page

                payload = {
                    'username': username,  # payload information
                    'password': password  # payload information
                }
                # generating jwt_token using algorithm HS256
                jwt_token = {'token': jwt.encode(payload, "secret_key", algorithm='HS256').decode()}
                j_token = jwt_token['token']
                redis_methods.set_token(self, 'token', j_token)
                res['message'] = "Welcome You Are Logged Successfully.."  # printing the message
                res['success'] = True  # initialize to True
                cache.set('token', "token")  # printing the data in  cache set
                res['data'] = j_token  # storing data token
                print(res)  # printing the result
                print('logged in----------------', redis_methods.get_token(self, 'token'))
                return redirect('fundoo:get')
                # return render(request, 'fundoo/index.html', {"token": res})  # after successful login render to index.
                # return render(request, 'fundoo/dash_board.html', {"token": res})  # after successful login render to index.


            else:
                return HttpResponse(
                    messages.success(request, "your account is inactive"))  # else print account is inactive

        else:
            messages.error(request, 'invalid username or password')  # printing invalid entry
            print('invalid username or password')  # printing invalid entry
            return render(request, 'fundoo/login.html', context=res)  # render back to login page

    except Exception as e:  # handling exception
        print(e)
        return render(request, 'fundoo/login.html', context=res)


def signup(request):
    # this method is used to sign up

    if request.method == 'POST':        # post will process the form data
        form = SignUpForm(request.POST)
        if form.is_valid():
            user = form.save(commit=False)
            user.save()
            current_site = get_current_site(request)
            subject = 'Activate Your MySite Account'
            message = render_to_string('fundoo/acc_active_email.html', {
                'user': user,
                'domain': current_site.domain,
                'uid': urlsafe_base64_encode(force_bytes(user.pk)).encode().decode(),
                # takes user id and generates the base64 code(uidb64)
                # Here we receive uidb64, token. By using the "urlsafe_base64_decode"
                # we decode the base64 encoded uidb64 user id.
                # We query the database with user id to get user
                'token': account_activation_token.make_token(user),
                # takes the user object and generates the onetime usable token for the user(token)
            })
            # here we are sending the the activation link to the given email id
            to_email = form.cleaned_data.get('email')
            email = EmailMessage(
                subject, message, to=[to_email]
            )
            email.send()
            return HttpResponse('Activation link has been sent to the given mail id')

    else:
        form = SignUpForm()
    return render(request, 'fundoo/signup.html', {'form': form})


# def upload_pic(request):
#
#     if request.method == 'POST':
#         uploaded_file = request.FILES['pic']
#         print(uploaded_file.name)
#         file_name=str(uploaded_file.name)
#         print(uploaded_file.size)
#         s3 = boto3.client('s3')
#         # s3.upload_file(uploaded_file, 'fundooapp777',"filename.jpg")
#         s3.upload_fileobj(uploaded_file, 'fundooapp777', Key=file_name)
#
#     return render(request, 'fundoo/upload.html', {})


def acc_login(request):
    return render(request, 'fundoo/login.html', {})


def activate(request, uidb64, token):
    # this method is used to send the activation link to the respective email id
    try:
        uid = force_text(urlsafe_base64_decode(uidb64))
        user = User.objects.get(id=uid)
    except (TypeError, ValueError, OverflowError, User.DoesNotExist):
        user = None

    if user is not None and account_activation_token.check_token(user, token):
        user.is_active = True
        #user.profile.email_confirmed = True
        user.save()
        login(request, user, backend='django.contrib.auth.backends.ModelBackend')
        return HttpResponse('Thank you for your email confirmation. Now you can login your account.')
    else:
        return HttpResponse('Activation link is invalid!')


def account_activation_sent(request):
    return render(request, 'acc_active_sent.html')


class RestLogin(CreateAPIView):
    serializer_class =UserSerializer

    def post(self, request, *args, **kwargs):
        res = {"message": "something bad happened",
               "data": {},
               "success": False}

        try:
            username = request.data['username']
            if username is None:
                raise Exception("Username is required")
            password = request.data['password']
            if password is None:
                raise Exception("password is required")
            user = authenticate(username=username, password=password)
            print('user-->', user)
            if user:
                if user.is_active:
                    payload = {'username': username, 'password': password}
                    # token = jwt.encode(payload, "secret_key", algorithm='HS256').decode('utf-8')
                    jwt_token = {
                        'token': jwt.encode(payload, "Cypher", algorithm='HS256').decode('utf-8')
                    }
                    print(jwt_token)
                    token = jwt_token['token']
                    res['message'] = "Logged in Successfully"
                    res['data'] = token
                    res['success'] = True
                    return Response(res)
                else:
                    return Response(res)
            if user is None:
                return Response(res)
        except Exception as e:
            print(e)
            return Response(res)


class RegisterRapi(CreateAPIView):
    serializer_class = RegistrationSerializer

    def post(self, request, *args, **kwargs):
        res = {"message": "something bad happened",
               "data": {},
               "success": False}
        username = request.data['username']  # getting the username
        email = request.data['email']   # getting the email id
        password = request.data['password']     # getting the password
        if username and email and password is not "":   # condition
            user = User.objects.create_user(username=username, email=email, password=password)
            user.is_active = False
            user.save()

            message = render_to_string("fundoo/acc_active_email.html", {
                'user': user,
                'domain': 'http://127.0.0.1:8000',
                'uid': urlsafe_base64_encode(force_bytes(user.pk)).decode(),
                'token': account_activation_token.make_token(user),


            })
            mail_subject = 'Activate your account...'
            to_email = email
            send_email = EmailMessage(mail_subject, message, to=[to_email])
            send_email.send()
            res['message'] = "registered Successfully...Please activate your Account"
            res['success'] = True
            return Response(res)
        else:
            return Response(res)


def index(request):
    return render(request, 'fundoo/index.html')


def dash_board(request):
    return render(request, 'fundoo/dash_board.html')



#
# def createnote(request):
#     if request.method == 'POST':
#         token = request.META.get('HTTP_AUTHORIZATION')
#         print("dis is token",token)
#         print(request.POST.get('title'))
#         title = request.POST.get('title')
#
#         description = request.POST.get('description')
#         color = request.POST.get('color')
#         is_archived = request.POST.get('is_archive')
#         image = request.POST.get('image')
#         is_pinned = request.POST.get('is_pinned')
#         notes = Notes(title=title, description=description, color=color, is_archived=is_archived, image=image,
#                       is_pinned=is_pinned)
#
#         notes.save()
#         print(notes)
#
#     return render(request, 'fundoo/notes/getnote.html')

# @csrf_exempt
def getnotes(request):
    """this method is used to display the notes in home screen created by the respective user """

    if request.method == 'GET':
        token = redis_methods.get_token(self, 'token')
        # gets the token from the redis cache
        token_decode = jwt.decode(token, 'secret_key', algorithms=['HS256'])
        # decodes the token
        print("TOKEN DECODE", token_decode)
        uname = token_decode.get('username')  # gets the user name from the token
        user = User.objects.get(username=uname)
        user_id = user.id  # getting user id
        request.user_id = user_id
        notes = Notes.objects.filter(user_id =user.id)
        print("allmynotes", notes)
        return render(request, 'fundoo/notes/getnote.html', {'notes': notes})


# @my_login_required
# def delete(request, pk):
#     """ this method is used to delete the note"""
#     if request.method == 'GET':
#         notes =Notes.objects.get(pk=pk)  # gets the pk value of note
#         notes.delete() # deletes the note by checking the pk value
#         return redirect("fundoo:get")
#         # redirects to  the respective page given in the code
#

@my_login_required
def createnote(request):
    """this method is used to create the note"""

    if request.method == 'POST':
        print("inside post create")
        # get username and password from submitted form
        auth_user =request.user_id

        print("Authentication User", auth_user)
        title = request.POST.get('title')  # get title
        print("title:", title)
        description = request.POST.get('description')  # get description
        print("description:", description)
        color = request.POST.get('color')  # get color
        print("color:", color)
        is_archived = request.POST.get('is_archive')  # get archive status
        print("is_archived:", is_archived)
        image = request.POST.get('image')  # get the image details
        print("image:", image)
        is_pinned = request.POST.get('is_pinned')  # get the pinned status
        print("is_pinned:", is_pinned)
        notes = Notes(title=title, description=description, color=color, is_archived=is_archived, user_id=auth_user,
                      image=image,
                      is_pinned=is_pinned)
        # all details are stored in this variable
        print(notes)
        notes.save()  # save the data
        allnotes = Notes.objects.all().order_by('-created_time')
        context = {  # 'title':title, # 'description':description
        'allnotes': allnotes}
    return redirect("fundoo:get")







# def createnote(request):
#     if request.method == 'POST':
#         token = request.META.get('HTTP_AUTHORIZATION')
#         print("dis is token",token)
#         print(request.POST.get('title'))
#         title = request.POST.get('title')
#
#         description = request.POST.get('description')
#         color = request.POST.get('color')
#         is_archived = request.POST.get('is_archive')
#         image = request.POST.get('image')
#         is_pinned = request.POST.get('is_pinned')
#         notes = Notes(title=title, description=description, color=color, is_archived=is_archived, image=image,
#                       is_pinned=is_pinned)
#
#         notes.save()
#         print(notes)
#
#     return render(request, 'fundoo/notes/getnote.html')


@csrf_exempt
def delete(request, pk):
    """ this method is used to delete the note"""
    res = {}
    try:
        if request.method == 'GET':
            notes =Notes.objects.get(pk=pk) # get the note of particular pk value
            notes.delete()  # deletes the note
            return redirect("fundoo:trashmenu")
            # redirects to  the respective page given in the code
    except Exception as e:
        res['message'] = 'something bad happend'  # returns the responce if error occurs
        return JsonResponse(res, status=404)

#@my_login_required
@csrf_exempt
def update(request, pk):
    """ this method is used to update the note"""
    note = Notes.objects.get(pk=pk) # gets the note of respective pk value
    print(note)
    title = request.POST['title']  # posts the entered title input
    print("my title", title)
    description = request.POST['description'] # posts the enetered description input
    # reminder = request.POST['reminder']
    note.title = title
    note.description = description
    # note.remainder = reminder
    note.save()
    # updated values are saved

    allnotes = Notes.objects.all().order_by('-created_time')
    context = {  # 'title':title, # 'description':description
        'allnotes': allnotes}
    return render(request, 'fundoo/notes/getnote.html', context)

@login_required
def pinned(request, pk):
    """ this method is used to pin the note"""
    res ={}
    try:
        note = Notes.objects.get(pk=pk)     # get the note of respective pk value
        print('MYNOTE',note)
        if note.is_pinned == False or note.is_pinned == None:  # checks the pinned status in db
            note.is_pinned = True   # if condition is satisfies then the value is changed to true
            note.save() # note is saved
            return redirect(reverse('fundoo:get'))
        else:
            note.is_pinned =False   # checks the pinned status in db
            note.save()     # note  is saved
            return redirect(reverse('fundoo:get'))
    except Exception as e:
        res['message'] = 'something bad happend'    # returns the responce
        return JsonResponse(res, status=404)


def trash(request,pk):
    """this method is used to move the deleted card from dashboard to trash"""
    res = {}
    try:
        note =Notes.objects.get(pk=pk) # get the note of respective pk value
        if note.trash ==False:
            note.trash =True
            note.save()
            return redirect('fundoo:get')
    except Exception as e:
        res['message'] = 'something bad happend'
        return JsonResponse(res, status=404)


def trashitem(request):
    """ this method is used to show the trash note cards """
    if request.method == 'GET':
        token = redis_methods.get_token(self, 'token') # gets the token from the redis cache
        token_decode = jwt.decode(token, 'secret_key', algorithms=['HS256']) # decodes the token
        print("TOKEN DECODE", token_decode)
        uname = token_decode.get('username') # gets the username from the token
        user = User.objects.get(username=uname)
        user_id = user.id  # getting user id
        request.user_id = user_id
        notes = Notes.objects.filter(user_id=user.id)
        print("print notes", notes)
    return render(request, 'fundoo/notes/trash_note.html', {'notes': notes})
    # renders to the respective html page


def restore_trash(request,pk):
    """ this method is used to restore the trash item """
    res = {}
    try:
        note = Notes.objects.get(pk=pk)  # get the note of respective pk value
        if note.trash == True:  # checks the status of trash field in db
            note.trash = False  # if condition satisfies value is changed to false
            note.save()         # data is saved in db
            return redirect('fundoo:trashmenu')
            # redirects to the respective page
    except Exception as e:
        res['message'] = 'something bad happend'
        return JsonResponse(res, status=404)

# def trash(request,pk):
#     res={}
#     try:
#         note =Notes.objects.get(pk=pk)
#         if note.trash ==False:
#             note.trash = True
#             note.save()
#             return redirect('fundoo:get')
#     except Exception as e:
#         res['message'] = 'something bad happend'
#         return JsonResponse(res, status=404)


@login_required
def is_archive(request, pk):
    """ this method is used to pin the note"""
    res ={}
    try:
        note = Notes.objects.get(pk=pk)     # get the note of respective pk value
        print('MYNOTE', note)
        if note.is_archived == None or note.is_archived == False:  # checks the pinned status in db
            note.is_archived = True   # if condition is satisfies then the value is changed to true
            note.save() # note is saved
            return redirect(reverse('fundoo:get'))
        else:
            note.is_archived =False   # checks the pinned status in db
            note.save()     # note  is saved
            return redirect(reverse('fundoo:get'))
    except Exception as e:
        res['message'] = 'something bad happend'    # returns the responce
        return JsonResponse(res, status=404)



def show_archive(request):
    """ THIS METHOD IS USED TO DISPLAY THE ARCHIVE CARDS OF THE LOGGED IN USER """
    if request.method == 'GET':
        token = redis_methods.get_token(self, 'token')  # gets the token from the redis cache
        token_decode = jwt.decode(token, 'secret_key', algorithms=['HS256'])  # decodes the token
        print("TOKEN DECODE", token_decode)
        uname = token_decode.get('username')  # gets the username from the token
        user = User.objects.get(username=uname)
        user_id = user.id  # getting user id
        request.user_id = user_id
        notes = Notes.objects.filter(user_id=user.id)
        print("print notes", notes)
    return render(request,'fundoo/notes/archive_note.html', {'notes': notes})

@csrf_exempt
def setcolor(request, pk):
    if request.method == 'POST':
        note = Notes.objects.get(pk=pk)
        colour = request.post['change_color']
        print("mycolour", colour)
        note.color = colour
        print(id)
        note.save()
        allnotes = Notes.objects.all().order_by('-created_time')
        # all_labels = Labels.objects.all().order_by('-created_time')
        # map_labels = MapLabel.objects.all().order_by('-created_time')
        print(allnotes)
    return redirect('fundoo:get')


@login_required
def copy_note(request, pk):
    """ This method is used to copy the note"""
    if request.method == 'GET':
        # get note with given id
        note = Notes.objects.get(pk=pk)     # gets the pk value of note
        title = note.title      # gets the title of the note
        color = note.color      # gets the color of the note
        trash = note.trash      # gets the trash value of note
        user_id =note.user_id   # gets the user id value of the note
        is_archived = note.is_archived     # gets the is_archived status of the note
        image = note.image      # gets the image of the note
        is_pinned = note.is_pinned      #  gets the  is_pinned status of the note
        # set description of requested id to new note
        description = note.description  # gets the description of the note
       # creates the copy  of note
        copy = Notes(title=title, description=description, color=color, trash=trash, is_archived=is_archived,
                        image=image, user_id=user_id, is_pinned=is_pinned,)
        # save's newcopy to database
        copy.save()
        allnotes = Notes.objects.all().order_by('-created_time')
        # all_labels = Labels.objects.all().order_by('-created_time')
        # map_labels = MapLabel.objects.all().order_by('-created_time')
        print(allnotes)
    return redirect('fundoo:get')







