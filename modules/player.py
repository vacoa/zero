from __future__ import unicode_literals
import vlc
import time
import gyoutube
import pafy
import os
import time
import json
import sys
from threading import Thread
import pulsectl

# Important (deprecated, now done directly in code): Configure vlcrc (~/.config/vlc/vlcrc) with 'alsa-audio-device=hw:0,0' and restart to choose your audio device

class Player():
    def __init__(self,rootFolder,gytb,deviceIndex=None):
        self.gytb = gytb
        self.rootFolder = rootFolder
        self.libFolder = rootFolder + '/lib'
        self.listFolder = rootFolder + '/list'
        self.ytbFolder = rootFolder + '/ytb'
        if not os.path.exists(self.libFolder):
            os.makedirs(self.libFolder)
        if not os.path.exists(self.listFolder):
            os.makedirs(self.listFolder)
        if not os.path.exists(self.ytbFolder):
            os.makedirs(self.ytbFolder)
        self.pulse = pulsectl.Pulse().sink_list()[deviceIndex]
        self.vlc = vlc.Instance('--aout=alsa', '--alsa-audio-device=hw:' + self.pulse.proplist['alsa.card'] + ',' + self.pulse.proplist['alsa.device'])
        self.player = self.vlc.media_list_player_new()
        self.media = []
        
    '''       
    def getDevices(self):
        devices = []
        m = self.vlc.media_player_new()
        mods = m.audio_output_device_enum()
        if mods:
            mod = mods
            while mod:
                mod = mod.contents
                devices.append(mod.device)
                mod = mod.next
        vlc.libvlc_audio_output_device_list_release(mods)
        return devices
    
    def setDevice(self,device):
        # PLease instantiate a new player before that (as soon as you change track or pause the player,
        # it will switch back to the default device defined in vlcrc
        # 'player = instance.media_player_new()'
        self.player.get_media_player().audio_output_device_set(None, device)
    '''      

    def medialoc(self,path):
        for p in path:
            self.media.add_media(self.vlc.media_new(p))

    def mediaurl(self,query):
        self.media.add_media(self.vlc.media_new(query))
        
        
    def mediaytb(self,query):
        list = self.gytb.searchPlaylistItemsInfo(query)
        for l in list:
            try:
                mystream = pafy.new(l['id']).getbestaudio()
                self.media.add_media(self.vlc.media_new(mystream.url))
            except Exception as e:
                print(str(e))


    def playmedia(self,mode,query):
        self.player.stop()
        self.player = self.vlc.media_list_player_new()
        self.media = self.vlc.media_list_new()
        self.player.set_media_list(self.media)
        if mode == "local":
            self.medialoc(query)
        elif mode == "youtube":
            thread = Thread(target=self.mediaytb, kwargs = {"query": query})
            thread.start()
        elif mode == "list":
            content = self.content()['list']
            pl = None
            for l in content:
                if l['file'] == self.listFolder + '/' + query + '.json':
                    pl = l
                    break
            paths = []
            for p in pl['lib']:
                print(self.libFolder + '/' + p)
                paths.append(self.libFolder + '/' + p)
            if pl is None:
                raise('Empty playlist for query "' + query + '"')
            self.medialoc(paths)
        elif mode == "url":
            self.mediaurl(query)
        while self.media.count() < 1:
            True
        self.player.play()
            

    def play(self):
        self.player.play()

    #Inconsistent behavior raising sometimes an error "Failed to connect to pulseaudio server"
    #def getvolume(self):
    #    return self.pulse.volume.values[0]*100

    def setvolume(self,vol):
        os.system('pactl set-sink-volume ' + self.pulse.name + ' ' + vol + '%')

    def count(self):
        return self.media.count()
        
    def next(self):
        self.player.next()

    def previous(self):
        self.player.previous()

    def is_playing(self):
        return self.player.is_playing()
        
    def pause(self):
        if self.player.is_playing():
            self.player.pause()
        
    def stop(self):
        self.player.stop()
        
    def content(self):
        list = {'lib':[],'list':[]}
        for root, directories, filenames in os.walk(self.libFolder):
            for filename in filenames:
                if filename.endswith('.mp3'):
                    list['lib'].append(os.path.join(root,filename))
        for root, directories, filenames in os.walk(self.listFolder):
            for filename in filenames:
                if filename.endswith('.json'):
                    file = os.path.join(root,filename)
                    with open(file) as f:
                        data = json.load(f)
                    list['list'].append({'file':file,'lib':data['lib']})
        return list
 
##secret = "/home/pi/zero/apiyoutube_secret.json"
##rootFolder = "/home/pi/share/player"
##gytb = gyoutube.Gyoutube(secret)
##ply = Player(rootFolder,gytb)
##print(ply.content())
##
##ply.playmedia('local',['/home/pi/share/player/lib/Comets.mp3', '/home/pi/share/player/lib/Chupee.mp3'])
##
##time.sleep(3)

##ply.playmedia('youtube','mozart vivaldi')
##ply.play_lib('Chupee.mp3')
##time.sleep(5)
##ply.play_lib('Comets.mp3')
##time.sleep(5)
##ply.pause()
##time.sleep(2)
##ply.resume()
##time.sleep(5)
##ply.stop()






