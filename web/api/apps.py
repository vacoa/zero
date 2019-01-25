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
import gyoutube
import player
import action
import gsheet
        

# USe noreload option to avoid being launched twice and possibly launch threads twice
class ApiConfig(AppConfig):

    name = 'api'
    busyLock = threading.Lock()
    root = "/home/pi/zero"
    urlroot = "http://192.168.178.82:8000"
    cred = root + "/Zero-b4a81cf1b175.json"
    modelone = root + "/repo2/resources/okzero.pmdl"
    modeltwo = root + "/repo2/resources/tesla.pmdl"
    gytbsecret = "/home/pi/zero/apiyoutube_secret.json"
    gytbFolder = "/home/pi/share/player"
    gshtsecret = "/home/pi/zero/gsheet_creds.json"
    
    spk = speak.Speak()
    gytb = gyoutube.Gyoutube(gytbsecret)
    gsht = gsheet.Gsheet(gshtsecret)
    ply = player.Player(gytbFolder,gytb)
    act = action.Action(ply=ply,spk=spk, gsht=gsht)
    gsp = gspeech.Gspeech(cred, speak=spk)
    sb = snowboy.Snowboy([modelone], urlroot + "/api/_action", ply)
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


