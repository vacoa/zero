from django.http import HttpResponse, JsonResponse, HttpResponseServerError
from django.apps import apps

from django.shortcuts import redirect, render
from datetime import datetime
import time

import threading



def listen(request):
    lock = apps.get_app_config('api').busyLock
    avail = lock.acquire(timeout=0.01)
    if avail:
        gsp = apps.get_app_config('api').gsp
        report = gsp.listen()
        lock.release()
        return JsonResponse({'status':'ok','data':report})
    else:
        return JsonResponse({'status':'busy'})
    
def status(request):
    sb = apps.get_app_config('api').sb
    return JsonResponse({'status':'ok',
                         'sb':sb.isAlive()})

def switchzero(request):
    state = request.GET['state']
    sb = apps.get_app_config('api').sb
    if state=='true' and (not sb.state):
        sb.launch()
    elif state=='false' and sb.state:
        sb.stop()
    else:
        return JsonResponse({'status':'ko'})
    return JsonResponse({'status':'ok'})
##def summary(request):
##
##    mshp = apps.get_app_config('api').metashp
##    data = mshp.table()
##    return JsonResponse(data)
##
##def preview(request):
##    folder = request.GET['folder']
##    shapeTag = request.GET['shapeFile']
##    img = folder + '\\' + shapeTag + '.png'
##    if not os.path.isfile(img):
##        data = {'status':'false'}
##    else:
##        with open(img, "rb") as f:
##            data = {'status':'true','base':base64.b64encode(f.read()).decode('utf-8')}
##    return JsonResponse(data)
##
##def dataset(request):
##    l = request.GET.getlist('listdata[]')
##    try:
##        zip_io = io.BytesIO()
##        with zipfile.ZipFile(zip_io, 'w', zipfile.ZIP_DEFLATED) as archive:
##            for s in l:
##                archive.write(s + '.metashape')
##                if os.path.isfile(s + '.mat'):
##                    archive.write(s + '.mat')
##                if os.path.isfile(s + '.png'):
##                    archive.write(s + '.png')
##                if os.path.isfile(s + '.log'):
##                    archive.write(s + '.log')
##        response = HttpResponse(zip_io.getvalue(), content_type = "application/zip")
##        response['Content-Disposition'] = 'attachment; filename=dataset.zip'
##        response['Content-Length'] = zip_io.tell()
##    except Exception as e:
##        print(e)
##        return HttpResponseServerError()
##    return response

