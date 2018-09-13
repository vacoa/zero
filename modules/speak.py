import os, sys
import threading

class Speak():
    def __init__(self):
        self.lang = 'fr-FR'
        
    def text_async(self,txt):
        t = threading.Thread(target=self.text, args=('Oui?',))
        t.start()
        
    def text(self,txt):
        txt = txt.replace('à','a')
        txt = txt.replace('ç','ss')
        txt = txt.replace('é','ai')
        txt = txt.replace('è','ai')
        txt = txt.replace('ê','ai')
        txt = txt.replace('pas,','pa,')
        volume= "level='90'";
        os.system('pico2wave -l ' + self.lang + ' -w response.wav "<volume ' + volume + '>' + txt + '</volume>"')
        os.system('aplay response.wav ')
        os.system('rm response.wav')
        
    def dong(self):
        f = os.path.join(os.path.join(os.path.dirname(os.path.dirname(os.path.realpath(__file__))),'resources'),'dong.wav')
        os.system('aplay ' + f)
