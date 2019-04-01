from email._header_value_parser import get_token

from django.contrib.auth import login, authenticate
from django.shortcuts import render,redirect
from django.http import HttpResponse, HttpResponseRedirect
from django.urls import reverse

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
        #print('username', user)  # printing the information
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
                return redirect('fundoo:dashboard')


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


def signup(request): # this method is used to sign up

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
                'uid': urlsafe_base64_encode(force_bytes(user.pk)).decode(),
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


def upload_pic(request):

    if request.method == 'POST':
        uploaded_file = request.FILES['pic']
        print(uploaded_file.name)
        file_name=str(uploaded_file.name)
        print(uploaded_file.size)
        s3 = boto3.client('s3')
        #s3.upload_file(uploaded_file, 'fundooapp777',"filename.jpg")
        s3.upload_fileobj(uploaded_file, 'fundooapp777', Key=file_name)

    return render(request, 'fundoo/upload.html', {})


def acc_login(request):
    return render(request, 'fundoo/login.html', {})

def activate(request, uidb64, token):
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

def abc(request):
    return render(request, 'fundoo/abc.html')



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
#     return render(request, 'fundoo/dash_board.html')
#
#
@my_login_required
def getnotes(request):
    if request.method == 'GET':
        import json
        # notes = Notes.objects.values_list('title', 'description').get(pk=pk)
        token = redis_methods.get_token(self,'token')
        token_decode = jwt.decode(token, 'secret_key', algorithms=['HS256'])
        # token_decode = jwt.decode(token, os.getenv("SIGNATURE"), algorithms=['HS256'])
        print("TOKEN DECODE", token_decode)
        uname = token_decode.get('username')
        user = User.objects.get(username=uname)
        user_id = user.id  # getting user id
        print("Laxman kjj ID", user_id)
        request.user_id = user_id
        notes = Notes.objects.filter(user_id =user.id)
        # notes = json.dumps(notes)
        # print(type(json.loads(notes)) )
        # print(notes)
        print("kkkkk",notes)
        # return render(request, 'fundoo/notes/getnote.html', {'notes': notes})
        return render(request, 'fundoo/notes/getnote.html', {'notes':notes })
#
#
def delete(request, pk):
    if request.method == 'GET':
        notes =Notes.objects.get(pk=pk)
        notes.delete()
        return redirect("fundoo:get")


#
#
# def update(request, pk):
#     # if request.method =='POST':
#         notes = Notes.objects.get(pk=pk)
#         return render(request,'fundoo/update.html', {'notes':notes})

    #
    # def home(request):
    #     allnotes = Notes.objects.all().order_by('-created_time')
    #     # all_labels = Labels.objects.all().order_by('-created_time')
    #
    #     import pprint
    #     pp = pprint.PrettyPrinter(indent=4)
    #     # pp.pprint( allnotes)
    #     context = {  # 'title':title,
    #         # 'description':description
    #         'allnotes': allnotes }
    #
    #     return render(request, 'notes/note_section.html', context)


@my_login_required
def createnote(request):
    # print("META",request.META)
    if request.method == 'POST':
        # get username and password from submitted form
        auth_user =request.user_id
        print("Authentication User", auth_user)
        title = request.POST.get('title')
        print("title:", title)
        description = request.POST.get('description')
        print("description:", description)
        color = request.POST.get('color')
        print("color:", color)
        is_archived = request.POST.get('is_archive')
        print("is_archived:", is_archived)
        image = request.POST.get('image')
        print("image:", image)
        is_pinned = request.POST.get('is_pinned')
        print("is_pinned:", is_pinned)

        notes = Notes(title=title, description=description, color=color, is_archived=is_archived, user_id=auth_user, image=image,
                      is_pinned=is_pinned)
        print(notes)
        notes.save()

    allnotes = Notes.objects.all().order_by('-created_time')
    context = {  # 'title':title, # 'description':description
        'allnotes': allnotes}
    return render(request, 'fundoo/notes/getnote.html', context)


def deletenote(request, pk):
    if request.method == 'GET':
        # get the note with requested id
        note = Notes.objects.get(pk=pk)
        print(note.trash)
        if note.trash == False:
            note.trash = True
            note.save()
            return render(request, 'fundoo/notes/getnote.html', )
        # else:
        #     note.is_deleted = True
        #     # delete note
        #     note.delete()
        #     return redirect('show_trash')

    notes = Notes.objects.all().order_by('-created_time')

    context = {  # 'title':title, # 'description':description
        'notes': notes}

    return render(request, 'notes/show_trash.html', context)










