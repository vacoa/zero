import gspeech
import logger, sys

cred = "/home/pi/zero/Zero-b4a81cf1b175.json"

gsp = gspeech.Gspeech(cred)
gsp.listen()