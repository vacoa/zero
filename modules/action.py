from datetime import datetime
import time
import inspect
import sys
import re
import threading

class Action:
    def __init__(self, ply=None, spk=None):
        self.ply = ply
        self.spk = spk

    def do(self,gsp_report):
        trans = gsp_report['trans']
        stream = gsp_report['stream']
        stab = gsp_report['stab']
        conf = gsp_report['conf']
        isfin = gsp_report['isfin']
        try:
            if stream == 'initout':
                self.spk.text("Si tu ne parles pas, je ne te répondrai pas.")
            elif stream == 'maxtime':
                self.spk.text('Arrête, arrête! Tu parles beaucoup trop pour un humain.')
            elif trans.lower() in ["tais-toi","rien"]:
                self.spk.text('Ah, ok.')
            elif trans.lower()=="c'est qui la plus belle":
                self.spk.text("C'est Zohé.")
            elif trans.lower().startswith('volume'):
                m = re.match( r'volume([^0-9]*)([0-9]+)(.*)', trans.lower(), re.M|re.I)
                if not m:
                    m = re.match( r'volume à([^0-9]*)([0-9]+)(.*)', trans.lower(), re.M|re.I)
                if m:
                    print('(1)="' + m.group(1) + '" | (2)="' + m.group(2) + '"')
                    ch = None
                    if m.group(1) in [' ']:
                        ch = '';
                    elif m.group(1) in [' plus ',' + ']:
                        ch = '+'
                    elif m.group(1) in [' moins ',' - ']:
                        ch = '-'
                    if ch is not None:
                        if int(m.group(2))>=0 or int(m.group(2))<=60:
                            return {'callback': lambda:self.ply.setvolume(ch + m.group(2))}
                        else:
                            self.spk.text("Je ne peux pas mettre le volume à moins de 0 et plus de 60.")
                    else:
                        self.spk.text("Je n'ai pas compris la commande de volume.")
                else:
                    self.spk.text("Je n'ai pas compris la commande de volume.")
            else:
                self.spk.text('Pourrais-tu parler de manière plus intelligible?')
                return {'trans':trans}
            return {}
        except:
            self.spk.text("J'ai besoin de dormir. Je m'éteins.")
            raise
