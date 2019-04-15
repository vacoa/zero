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
import configparser          

# USe noreload option to avoid being launched twice and possibly launch threads twice
class ApiConfig(AppConfig):

    name = 'api'
    busyLock = threading.Lock()
    root = os.path.dirname(os.path.realpath(__file__)) + "/../.."
    
    config = configparser.ConfigParser()
    config.read(root + '/config.ini')
    
    urlroot = 'http://' + config['GLOBAL']['IP'] + ':' + config['GLOBAL']['PORT'] 
    gspeechsecret = config['DEFAULT']['KEY_ROOT'] + "/" + config['DEFAULT']['KEY_GSPEECH']
    
    gytbsecret = config['DEFAULT']['KEY_ROOT'] + "/" + config['DEFAULT']['KEY_GYTB']
    gytbFolder = config['DEFAULT']['GYTB_ROOT']
    gshtsecret = config['DEFAULT']['KEY_ROOT'] + "/" + config['DEFAULT']['KEY_GSHEET']
    speechDevice = int(config['DEFAULT']['SPEECH_DEVICE'])
    playerDevice = int(config['DEFAULT']['PLAYER_DEVICE'])
    sheetId = config['DEFAULT']['SHEET_ID']
    
    modelone = root + "/resources/okzero.pmdl"
    modeltwo = root + "/resources/tesla.pmdl"
    
    spk = speak.Speak(device_index=speechDevice)
    gytb = gyoutube.Gyoutube(gytbsecret)
    gsht = gsheet.Gsheet(gshtsecret,defaultId=sheetId)
    ply = player.Player(gytbFolder,gytb, deviceIndex=playerDevice)
    act = action.Action(ply=ply,spk=spk, gsht=gsht)
    gsp = gspeech.Gspeech(gspeechsecret, speak=spk, device=speechDevice)
    sb = snowboy.Snowboy([modelone], urlroot + "/api/_action", ply, device=speechDevice)
    sb.start()
    sb.launch()

    
    


