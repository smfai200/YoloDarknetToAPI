"""
Definition of views.
"""

from django.shortcuts import render,redirect
from django.http import HttpRequest,HttpResponse
from django.template import RequestContext
from datetime import datetime
from django.core.files.storage import FileSystemStorage
from app.forms import DocumentForm
import os
import requests
import urllib.request as req


def home(request):
    """Renders the home page."""
    assert isinstance(request, HttpRequest)
    return render(
        request,
        'app/index.html',
        {
            'title':'Home Page',
            'year':datetime.now().year,
        }
    )

def ProcessImage(request):
    if request.method == 'POST':
        #if and request.FILES['myfile']:
        try:
          myfile = request.FILES['myfile']
          print(myfile)
        except:
         cameraip = request.POST['cameraip']
         print(cameraip)
         r = requests.get('http://'+cameraip+':8000/takeimage/',data={})
         imgurl = 'http://'+cameraip+':8000/media/image.jpg'
         req.urlretrieve(imgurl, "/home/ghost_rider/DarkNetAPI/DarkNetAPI/media/imagename.jpg")
         doProcessOnImage('imagename.jpg')
         return redirect('http://127.0.0.1:8000/media/predictions1.jpg')
         #return redirect('http://'+cameraip+':8000/media/image.jpg')

        fs = FileSystemStorage()
        filename = fs.save(myfile.name, myfile)
        uploaded_file_url = fs.url(filename)
        doProcessOnImage(filename)
        return redirect('http://127.0.0.1:8000/media/predictions1.jpg')
        #return render(request, 'app/imageresult.html', {})
    elif(request.method == 'GET'):
        return render(
        request,
        'app/ImageView.html',{}
    )
    
def SignalImage(request):
    if request.method == 'POST':
        myfile = request.FILES['myfile']
        print(myfile)
        fs = FileSystemStorage()
        filename = fs.save(myfile.name, myfile)
        uploaded_file_url = fs.url(filename)
        doProcessOnImage(filename)
        return redirect('http://127.0.0.1:8000/media/predictions1.jpg')
    elif(request.method == 'GET'):
        return render(
        request,
        'app/ImageView.html',{}
    )

def model_form_upload(request):
    if request.method == 'POST':
        form = DocumentForm(request.POST, request.FILES)
        if form.is_valid():
            form.save()
            return redirect('home')
    else:
        form = DocumentForm()
    return render(request, 'app/model_form_upload.html', {
        'form': form
    })


def doProcessOnImage(Imagename):
    try:
      command = 'cd /home/ghost_rider/darknet && ./darknet detect cfg/yolov3.cfg yolov3.weights '+'/home/ghost_rider/DarkNetAPI/DarkNetAPI/media/'+str(Imagename)
      os.system(command)
      os.system("cp /home/ghost_rider/darknet/predictions1.jpg /home/ghost_rider/DarkNetAPI/DarkNetAPI/media/")
      return True
    except:
      return False
