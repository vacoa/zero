import os, sys
import threading
import subprocess
import pyaudio
from ctypes import *
from contextlib import contextmanager

def py_error_handler(filename, line, function, err, fmt):
    pass
ERROR_HANDLER_FUNC = CFUNCTYPE(None, c_char_p, c_int, c_char_p, c_int, c_char_p)
c_error_handler = ERROR_HANDLER_FUNC(py_error_handler)

@contextmanager
def no_alsa_error():
    try:
        asound = cdll.LoadLibrary('libasound.so')
        asound.snd_lib_error_set_handler(c_error_handler)
        yield
        asound.snd_lib_error_set_handler(None)
    except:
        yield
        pass

class Speak():
    def __init__(self,device_index=None):
        self.lang = 'fr-FR'
        with no_alsa_error():
                p = pyaudio.PyAudio()
        devname = p.get_device_info_by_index(device_index)['name']
        self.device = devname[-4:-1]
        #print(self.device), not so robust, to be fixed
        
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
        subprocess.call('pico2wave -l ' + self.lang + ' -w response.wav "<volume ' + volume + '>' + txt + '</volume>" && sox response.wav -r 44100 response_44100.wav && aplay --device=plughw:' + self.device + ' response_44100.wav && rm response.wav && rm response_44100.wav', shell=True)
        
    def dong(self):
        f = os.path.join(os.path.join(os.path.dirname(os.path.dirname(os.path.realpath(__file__))),'resources'),'dong_44100.wav')
        subprocess.call('aplay --device=plughw:' + self.device + ' ' + f, shell=True)
