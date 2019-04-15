import pyaudio
import vlc
import pulsectl


# Start: cancelling alsa warnings
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
# End: cancelling alsa warnings

with no_alsa_error():
    p = pyaudio.PyAudio()
print('==============================================')
print('>>> Speech configuration:')
for i in range(p.get_device_count()):
    dev = p.get_device_info_by_index(i)
    print((i,dev['name'],dev['maxInputChannels']))
    

'''
print('==============================================')
print('>>> VLC configuration:')
devices = []
v = vlc.Instance()
m = v.media_player_new()
mods = m.audio_output_device_enum()
i = 0
if mods:
    mod = mods
    while mod:
        mod = mod.contents
        devices.append(mod.device)
        print((i,mod.device.decode()))
        tmp = mod.device
        i = i + 1
        mod = mod.next
vlc.libvlc_audio_output_device_list_release(mods)
'''

print('==============================================')
print('>>> Player configuration:')
l = pulsectl.Pulse().sink_list()
for i in range(len(l)):
    print((i,l[i].name,'hw:' + l[i].proplist['alsa.card'] + ',' + l[i].proplist['alsa.device']))

'''
print('==============================================')    
print('>>> Pulse Control source configuration:')
l = pulsectl.Pulse().source_list()
for i in range(len(l)):
    print((i,l[i]))
'''

