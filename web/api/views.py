from django.http import HttpResponse, JsonResponse, HttpResponseServerError
from django.apps import apps

import io
import base64
import os
import zipfile
import tempfile
import json

from django.shortcuts import redirect, render
from datetime import datetime

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

