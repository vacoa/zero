from django.apps import AppConfig
from . import models
from threading import Thread
import time


class ApiConfig(AppConfig):
    name = 'api'
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


