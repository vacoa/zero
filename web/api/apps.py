from django.apps import AppConfig
from . import models
import threading
import time
import sys, os
sys.path.append(os.path.join(os.path.dirname(os.path.dirname(os.path.dirname(os.path.realpath(__file__)))),'modules'))
import logger
import gspeech
import speak
import snowboy

# USe noreload option to avoid being launched twice and possibly launch threads twice
class ApiConfig(AppConfig):
    name = 'api'
    busyLock = threading.Lock()
    root = "/home/pi/zero"
    urlroot = "http://192.168.178.82:8000"
    cred = root + "/Zero-b4a81cf1b175.json"
    model = root + "/repo2/resources/okzero.pmdl"
    spk = speak.Speak()
    gsp = gspeech.Gspeech(cred, speak=spk)
    sb = snowboy.Snowboy(model, urlroot + "/api/listen")
    sb.start()
    sb.launch()
    
##    metashp = models.Metashp('\\\\imcsmb.imu.intel.com\\cogpow\\SHAPE_auto')
##
##
##    def ready(self):
##        thread = Thread(target=self.loop)
##        thread.daemon = True
##        thread.start()
##
##    def loop(self):
##        while True:
##            self.metashp.update()
##            time.sleep(10)


