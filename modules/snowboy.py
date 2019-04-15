import logger
from threading import Thread
import sys, os
sys.path.append(os.path.join(os.path.dirname(os.path.realpath(__file__)),'snowboy'))
import snowboydecoder
import urllib.request
import time



class Snowboy(Thread):
    def __init__(self, model, apicallback, player, sensitivity=0.5, device=None):
        Thread.__init__(self)

        self.apicallback = apicallback
        self.model = model
        self.device_index = device
        
        self.detector = snowboydecoder.HotwordDetector(self.model, sensitivity=[0.48])
        self.callbacks = [lambda: self.callbackone()]
        
        self.interrupted = False # Command
        self.state = False # Result

        self.timecallback = 0
        self.ply = player
        
    def run(self):
        logger.info("Snowboy run")
        while True:
            self.state = True
            logger.info("Snowboy launch")
            while not self.interrupted:
                self.detector.start(detected_callback=self.callbacks,
                               interrupt_check=self.interrupt_callback,
                               sleep_time=0.001,
                               device_index=self.device_index)
            self.detector.terminate()
            self.state = False
            logger.info("Snowboy stop")
            while self.interrupted:
                time.sleep(2)
            
    def interrupt_callback(self):
        return self.interrupted
    
    def stop(self):
        self.interrupted = True
        while self.state:
            time.sleep(1)
        
    def launch(self):
        self.interrupted = False
        while not self.state:
            time.sleep(1)
        
    def callbackone(self):
        if not self.ply.is_playing():
            logger.info('Snowboy callback 1 ...')
            self.timecallback = time.time()
            contents = urllib.request.urlopen(self.apicallback).read()

    def callbacktwo(self):
        if not self.ply.is_playing() and time.time() < self.timecallback+3:
            logger.info('Snowboy callback 2 ...')
            self.timecallback = time.time()
            contents = urllib.request.urlopen(self.apicallback).read()

            
        
        
##        self.lock.acquire()
##        print('ACQUIRE')
##        report = self.gsp.listen()
##        self.lock.release()
##        print('RELEASE')
