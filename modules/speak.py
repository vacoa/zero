import os, sys
import threading
import subprocess

class Speak():
    def __init__(self):
        self.lang = 'fr-FR'
        
    def text_async(self,txt):
        t = threading.Thread(target=self.text, args=(txt,))
        t.start()
        
    def text(self,txt):
        txt = txt.replace('à','a')
        txt = txt.replace('ç','ss')
        txt = txt.replace('é','ai')
        txt = txt.replace('è','ai')
        txt = txt.replace('ê','ai')
        txt = txt.replace('pas,','pa,')
        volume= "level='90'";
        subprocess.call('pico2wave -l ' + self.lang + ' -w response.wav "<volume ' + volume + '>' + txt + '</volume>" && aplay response.wav && rm response.wav', shell=True)
        
    def dong(self):
        f = os.path.join(os.path.join(os.path.dirname(os.path.dirname(os.path.realpath(__file__))),'resources'),'dong.wav')
        subprocess.call('aplay ' + f, shell=True)
