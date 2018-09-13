from django.apps import AppConfig
from . import models
import threading
import time
import sys, os
sys.path.append(os.path.join(os.path.dirname(os.path.dirname(os.path.dirname(os.path.realpath(__file__)))),'modules'))
import logger
import gspeech
import speak

class ApiConfig(AppConfig):
    name = 'api'
    busyLock = threading.Lock()
    cred = "/home/pi/zero/Zero-b4a81cf1b175.json"
    spk = speak.Speak()
    gsp = gspeech.Gspeech(cred, speak=spk)
    
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


