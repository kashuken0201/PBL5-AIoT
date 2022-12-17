from django.shortcuts import get_object_or_404, render, redirect
from .models import *
from django.http.response import StreamingHttpResponse
from facemask.camera import *
from django.views.decorators import gzip

# Create your views here.
def log_view(request):
    logs = Log.objects.all()
    context = {
        "logs": logs
    }
    return render(request, "face/log.html", context)

def face_view(request):
    logs = Log.objects.all()
    context = {
        "logs": logs
    }
    return render(request, "face/face-recognize.html", context)

@gzip.gzip_page
def stream_view(request):
    # if(camera == None):
    #     camera = IPWebCam()
    return StreamingHttpResponse(gen(VideoCamera()),
				content_type='multipart/x-mixed-replace; boundary=frame')

def capture_view(request):
    capture(VideoCamera.get_instance())
    return redirect('/capture')

def detect_view(request):
    return redirect('/dectect')


