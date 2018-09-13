from django.db import models
from django.apps import apps
import os
import json
import time
import threading
from django.conf import settings



# For database extensions
# class MetaClass(models.Model):
#     tag = models.CharField(max_length=42)
#     name = models.CharField(max_length=100)
#     tip = models.TextField(null=True)
#     desc = models.TextField(null=True)
#     class Meta:
#         verbose_name = "MetaClass"
#         ordering = ['tag']
#
#     def __str__(self):
#         return self.tag
#
#
# class MetaParam(models.Model):
#     tag = models.CharField(max_length=42)
#     name = models.CharField(max_length=100)
#     classes = models.ManyToManyField(MetaClass, related_name="metaClass")
#     tip = models.TextField(null=True)
#     desc = models.TextField(null=True)
#
#     class Meta:
#         verbose_name = "MetaParam"
#         ordering = ['tag']
#
#     def __str__(self):
#         return self.tag


##class Metashp():
##    def __init__(self,rootFolder):
##        self.rootFolder = rootFolder
##        self.lastUpdate = None
##        self.jsonData = None
##        self.lock = threading.Lock()
##
##    def table(self):
##        self.lock.acquire()
##        var = self.jsonData
##        self.lock.release()
##        return var
##
##    def update(self):
##        data = self.find(self.rootFolder)
##        keys = []
##        for d in data:
##            for k in d.keys():
##                if k not in keys:
##                    keys.append(k)
##        for d in data:
##            for k in keys:
##                if k not in d.keys():
##                    d[k] = ''
##        columns = []
##        with open(apps.get_app_config('api').path + '\\static\\api\\metadef.json') as f:
##            metadef = json.load(f)
##        for k in keys:
##            cname = ''
##            vis = False
##            for m in metadef['meta']:
##                if m['tag'] == k:
##                    cname = m['class']
##                    if ('default' in cname) or ('root' in cname) :
##                        vis = True
##                    break
##            columns.append({'data':k,'className':cname,'visible':vis})
##        self.lock.acquire()
##        self.jsonData = {'columns':columns, 'content':data}
##        self.lock.release()
##        self.lastUpdate = time.time()
##
##    def find(self,topFolder):
##        result = []
##        for tag in os.listdir(topFolder):
##            newPath = os.path.join(topFolder, tag)
##            if tag.endswith(".metashape"):
##                with open(newPath, 'r') as f:
##                    t = {'folder':topFolder, 'shapeFile': tag[:-10]}
##                    t.update(json.load(f))
##                    result.append(t)
##            elif os.path.isdir(newPath) and not tag.endswith("_SHAPSE"):
##                result = result + self.find(newPath)
##        return result


