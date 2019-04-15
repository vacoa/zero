from datetime import datetime
import time
import inspect
import sys
import re
import os
import threading
from difflib import SequenceMatcher
from heapq import nlargest as _nlargest

class Action:
    def __init__(self, ply=None, spk=None, gsht=None):
        self.ply = ply
        self.spk = spk
        self.gsht = gsht

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
            elif trans.lower() in ["tais-toi","rien","ta gueule"]:
                self.spk.text('Ah, ok.')
            elif trans.lower()=="c'est qui la plus belle":
                self.spk.text("C'est Zoé.")
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
                            self.spk.text("D'accord, je change le volume.")
                            return {'callback': lambda:self.ply.setvolume(ch + m.group(2))}
                        else:
                            self.spk.text("Je ne peux pas mettre le volume à moins de 0 et plus de 60.")
                    else:
                        self.spk.text("Je n'ai pas compris la commande de volume.")
                else:
                    self.spk.text("Je n'ai pas compris la commande de volume.")
            elif trans.lower() in ['précédent','précédente','recule']:
                return {'callback': lambda:self.ply.previous()}
            elif trans.lower() in ['suivant','suivante','avance']:
                return {'callback': lambda:self.ply.next()}
            elif trans.lower() in ['pause','pose','poste','bose']:
                return {'callback': lambda:self.ply.pause()}
            elif trans.lower() in ['reprends','reprend','reprendre','continue']:
                return {'callback': lambda:self.ply.play()}
            elif trans.lower().startswith("note"):
                m = re.match( r'note (.*)', trans.lower(), re.M|re.I)
                if m:
                    print('(1)="' + m.group(1) + '"')
                    self.gsht.append_default([[str(datetime.now()),m.group(1)]])
                    self.spk.text("J'ai noté, " + m.group(1) + ".")
                else:
                    self.spk.text("Je n'ai pas compris la note.")
            elif trans.lower().startswith("liste de courses"):
                m = re.match( r'liste de courses (.*)', trans.lower(), re.M|re.I)
                if m:
                    print('(1)="' + m.group(1) + '"')
                    self.gsht.append('1kyqc8T8knRsbJ-UNr5RyscjTO87BLRsmh8bShsIfTe8',
                                    [[str(datetime.now()),m.group(1)]])
                    self.spk.text("J'ai noté dans la liste de courses, " + m.group(1) + ".")
                else:
                    self.spk.text("Je n'ai pas compris la note de liste de courses.")
            elif trans.lower()=="radio":
                self.spk.text("D'accord, je mets radio nova.")
                return {'callback': lambda:self.ply.playmedia('url',"http://novazz.ice.infomaniak.ch/novazz-128.mp3")}
            elif trans.lower().startswith("radio"):
                m = re.match( r'radio (.*)', trans.lower(), re.M|re.I)
                # http://fluxradios.blogspot.com to add new radios
                if m:
                    print('(1)="' + m.group(1) + '"')
                    labfm = ["rtl",
                             "france inter",
                             "europe 1",
                             "nova",
                             "tsf jazz",
                             "fip",
                             "france culture",
                             "france info",
                             "oui fm"]
                    urlfm = ["http://streaming.radio.rtl.fr/rtl-1-48-192",
                             "http://direct.franceinter.fr/live/franceinter-midfi.mp3",
                             "http://mp3lg4.tdf-cdn.com/9240/lag_180945.mp3",
                             "http://novazz.ice.infomaniak.ch/novazz-128.mp3",
                             "http://tsfjazz.ice.infomaniak.ch/tsfjazz-high.mp3",
                             "http://direct.fipradio.fr/live/fip-midfi.mp3",
                             "http://direct.franceculture.fr/live/franceculture-midfi.mp3",
                             "http://direct.franceinfo.fr/live/franceinfo-midfi.mp3",
                             "http://stream.ouifm.fr/ouifm-high.mp3"]
                    res = self.getMatch(m.group(1),[x.lower() for x in labfm], n=3, cutoff=0.7)
                    print('Match=' + str(res) + ' | Files=' + str(labfm))
                    if len(res)>0:
                        self.spk.text("D'accord, je mets radio " + labfm[res[0]] + ".")
                        return {'callback': lambda:self.ply.playmedia('url',urlfm[res[0]])}
                    else:
                        self.spk.text("Je n'ai pas trouvé la radio.")
                else:
                    self.spk.text("Je n'ai pas compris la commande de musique.")  
            elif trans.lower()=="musique":
                self.spk.text("D'accord, je mets la liste musicale par défaut.")
                return {'callback': lambda:self.ply.playmedia('list','defaut')}
            elif trans.lower().startswith("musique"):
                m = re.match( r'musique (.*)', trans.lower(), re.M|re.I)
                if m:
                    print('(1)="' + m.group(1) + '"')
                    path = os.listdir(self.ply.listFolder)
                    fil = []
                    for f in path:
                        if os.path.isfile(self.ply.listFolder + '/' + f):
                            fil.append(f[:-5])
                    res = self.getMatch(m.group(1),[x.lower() for x in fil], n=3, cutoff=0.7)
                    print('Match=' + str(res) + ' | Files=' + str(fil))
                    if len(res)>0:
                        self.spk.text("D'accord, je mets la liste musicale, " + fil[res[0]] + ".")
                        return {'callback': lambda:self.ply.playmedia('list',fil[res[0]])}
                    else:
                        self.spk.text("Je n'ai pas trouvé le dossier de musique.")
                else:
                    self.spk.text("Je n'ai pas compris la commande de musique.")  
            elif trans.lower().startswith("youtube"):
                m = re.match( r'youtube (.*)', trans.lower(), re.M|re.I)
                if m:
                    print('(1)="' + m.group(1) + '"')
                    self.spk.text_async("Je cherche " + m.group(1) + " sur Youtube. Je te prie de patienter quelques secondes.")
                    self.ply.playmedia('youtube',m.group(1))
                else:
                    self.spk.text("Je n'ai pas compris la commande de musique.")
            else:
                self.spk.text('Pourrais-tu parler de manière plus intelligible?')
                return {'trans':trans}
            return {}
        except:
            self.spk.text("J'ai besoin de dormir. Je m'éteins.")
            raise

    def getMatch(self,word, possibilities, n=3, cutoff=0.6):
        """Use SequenceMatcher to return a list of the indexes of the best 
        "good enough" matches. word is a sequence for which close matches 
        are desired (typically a string).
        possibilities is a list of sequences against which to match word
        (typically a list of strings).
        Optional arg n (default 3) is the maximum number of close matches to
        return.  n must be > 0.
        Optional arg cutoff (default 0.6) is a float in [0, 1].  Possibilities
        that don't score at least that similar to word are ignored.
        """

        if not n >  0:
            raise ValueError("n must be > 0: %r" % (n,))
        if not 0.0 <= cutoff <= 1.0:
            raise ValueError("cutoff must be in [0.0, 1.0]: %r" % (cutoff,))
        result = []
        s = SequenceMatcher()
        s.set_seq2(word)
        for idx, x in enumerate(possibilities):
            s.set_seq1(x)
            if s.real_quick_ratio() >= cutoff and \
               s.quick_ratio() >= cutoff and \
               s.ratio() >= cutoff:
                result.append((s.ratio(), idx))

        # Move the best scorers to head of list
        result = _nlargest(n, result)

        # Strip scores for the best n matches
        return [x for score, x in result]

    

