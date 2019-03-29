# import boto3
# from django.http import HttpResponse
# from django.shortcuts import render
#
#
import boto3
from django.http import HttpResponse
from django.shortcuts import render


def uploadto_aws(request):

    if request.method == 'POST':
        uploaded_file = request.FILES['document']   # taking the file from local
        print(uploaded_file.name)

        print(uploaded_file)
        file_name=str(uploaded_file)       # taking file name in string

        s3 = boto3.client('s3')             # using boto to upload file in aws s3 bucket
        #s3.upload_file(uploaded_file, 'fundooapp777',"filename.jpg")
        s3.upload_fileobj(uploaded_file, 'fundooapp777', Key=file_name)
        return HttpResponse('IMAGE HAS BEEN UPLOADED')
    return render(request, 'fundoo/upload.html', {})
