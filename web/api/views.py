from django.http import HttpResponse, JsonResponse, HttpResponseServerError
from django.apps import apps

from django.shortcuts import redirect, render
from datetime import datetime
import time
import inspect
import sys
import re

import threading

def singleton(fcn): # wrapper in case standard responses should be sent
    def wrapper(request):
        lock = apps.get_app_config('api').busyLock
        avail = lock.acquire(timeout=0.01)
        print('ACQUIRE')
        if avail:
            try:
                response = fcn(request)
                if 'callback' in response:
                    response['callback']()
                    response['callback'] = inspect.getsource(response['callback'])
                response['status'] = 'ok'
            except:
                e = sys.exc_info()[0]
                s = sys.exc_info()[1]
                print('ZERO ERROR:', e, s)
                response = {'status': 'ko',
                            'error': str(s)}
            print('RELEASE')
            lock.release()
        else:
            response = {'status':'busy'}
        return JsonResponse(response)
    return wrapper

def sb_pause(fcn): # Pause snowboy background process during requests
    def wrapper(request):
        sb = apps.get_app_config('api').sb
        oldstate = False
        if sb.state:
            oldstate = True
            t = threading.Thread(target=sb.stop)
            t.start()
        try:
            response = fcn(request)
            if oldstate:
                t.join()
                sb.launch()
        except:
            if oldstate:
                t.join()
                sb.launch()
            raise
        return response
    return wrapper

def ply_pause(fcn): # Pause player when listening
    def wrapper(request):
        ply = apps.get_app_config('api').ply
        wasplaying = False
        if ply.is_playing():
            wasplaying = True
            ply.pause()
        try: 
            response = fcn(request)
            if wasplaying:
                ply.play()
        except:
            if wasplaying:
                ply.play()
            raise
        return response
    return wrapper


@singleton
@sb_pause
@ply_pause
def action(request):
    gsp = apps.get_app_config('api').gsp
    act = apps.get_app_config('api').act
    report = gsp.listen()
    response = act.do(report)
    return response
    
@singleton
@ply_pause
def _action(request):
    gsp = apps.get_app_config('api').gsp
    act = apps.get_app_config('api').act
    report = gsp.listen()
    response = act.do(report)
    return response
    
@singleton
@sb_pause
@ply_pause
def speak(request):
    text = request.GET['text']
    spk = apps.get_app_config('api').spk
    spk.text(text)
    return {}

@singleton
@sb_pause
def player(request):
    cmd = request.GET['cmd']
    arg = request.GET['arg']

    ply = apps.get_app_config('api').ply
    if cmd == 'musique':
        if not arg:
            ply.playmedia('list','defaut')
    elif cmd == 'stop':
        ply.stop()
    elif cmd == 'play':
        ply.play()
    elif cmd == 'pause':
        ply.pause()
    elif cmd == 'next':
        ply.next()
    elif cmd == 'previous':
        ply.previous()
    elif cmd == 'volume':
        ply.setvolume(arg)
    else:
        raise Exception()
    return {}

@singleton
def leap(request):
    cmd = request.GET['cmd']
    arg = request.GET['arg']

    ply = apps.get_app_config('api').ply
    if cmd == 'stop':
        ply.stop()
    elif cmd == 'play':
        ply.play()
    elif cmd == 'pause':
        ply.pause()
    elif cmd == 'next':
        ply.next()
    elif cmd == 'previous':
        ply.previous()
    elif cmd == 'volume':
        ply.setvolume(arg)
    else:
        raise Exception()
    return {}

@singleton
@sb_pause
@ply_pause
def listen(request):
    gsp = apps.get_app_config('api').gsp
    report = gsp.listen()
    return {'data':report}


@singleton
def status(request):
    sb = apps.get_app_config('api').sb
    return {'sb':sb.state}

@singleton
def switchzero(request):
    state = request.GET['state']
    sb = apps.get_app_config('api').sb
    if state=='true' and (not sb.state):
        sb.launch()
    elif state=='false' and sb.state:
        sb.stop()
    else:
        raise Exception()
    return {}



        
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

