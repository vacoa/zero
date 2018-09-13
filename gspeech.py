from __future__ import division

import re
import sys
import os
import time
import logger

from google.cloud import speech
from google.cloud.speech import enums
from google.cloud.speech import types
import pyaudio
from six.moves import queue




class MicrophoneStream(object):
    """Opens a recording stream as a generator yielding the audio chunks."""
    def __init__(self, rate, chunk, initout, timeout, maxtime, last):
        self._rate = rate
        self._chunk = chunk
        
        # Event parameters
        self.initout = initout
        self.timeout = timeout
        self.last = last
        self.status = None
        self.starttime = None
        self.maxtime = maxtime
        self.firsttime = None

        # Create a thread-safe buffer of audio data
        self._buff = queue.Queue()
        self.closed = True

    def __enter__(self):
        self.status = 'open'
        self.starttime = time.time()
        self._audio_interface = pyaudio.PyAudio()
        self._audio_stream = self._audio_interface.open(
            format=pyaudio.paInt16,
            # The API currently only supports 1-channel (mono) audio
            # https://goo.gl/z757pE
            channels=1, rate=self._rate,
            input=True, frames_per_buffer=self._chunk,
            # Run the audio stream asynchronously to fill the buffer object.
            # This is necessary so that the input device's buffer doesn't
            # overflow while the calling thread makes network requests, etc.
            stream_callback=self._fill_buffer,
        )

        self.closed = False
        return self

    def __exit__(self, type, value, traceback):
        self._audio_stream.stop_stream()
        self._audio_stream.close()
        self.closed = True
        # Signal the generator to terminate so that the client's
        # streaming_recognize method will not block the process termination.
        self._buff.put(None)
        self._audio_interface.terminate()

    def _fill_buffer(self, in_data, frame_count, time_info, status_flags):
        """Continuously collect data from the audio stream, into the buffer."""
        self._buff.put(in_data)
        if (time.time() > self.starttime+self.initout and self.last is None):
            self.closed = True
            self.status = 'initout'
        elif (self.last is not None and time.time()>self.last+self.timeout):
            self.closed = True
            self.status = 'timeout'
        elif (self.firsttime is not None and time.time()>self.maxtime+self.firsttime):
            self.closed = True
            self.status = 'maxtime'
        return None, pyaudio.paContinue

    def generator(self):
        while not self.closed:
            # Use a blocking get() to ensure there's at least one chunk of
            # data, and stop iteration if the chunk is None, indicating the
            # end of the audio stream.
            
            
            chunk = self._buff.get()
            if chunk is None:
                return
            data = [chunk]

            # Now consume whatever other data's still buffered.
            while True:
                try:
                    chunk = self._buff.get(block=False)
                    if chunk is None:
                        return
                    data.append(chunk)
                except queue.Empty:
                    break      

            yield b''.join(data)
            



        



class Gspeech():
    def __init__(self, cred, language_code='fr-FR'):
        # Audio recording parameters
        self.rate = 16000
        self.chunk = int(self.rate / 10)  # 100ms
        
        os.environ["GOOGLE_APPLICATION_CREDENTIALS"] = cred
        
        # See http://g.co/cloud/speech/docs/languages
        # for a list of supported languages.
        self.language_code = 'fr-FR'  # a BCP-47 language tag

        self.client = speech.SpeechClient()
        self.config = types.RecognitionConfig(
            encoding=enums.RecognitionConfig.AudioEncoding.LINEAR16,
            sample_rate_hertz=self.rate,
            language_code=self.language_code)
        self.streaming_config = types.StreamingRecognitionConfig(
            config=self.config,
            interim_results=True)
        
    def listen(self):
        initout = 2 # First timeout, when no word at all has been detected yet
        timeout = 1 # Second timeout, to decide to close the stream
        maxtime = 10 # Maximum listening time from first result
        last = None # If none initout applies from the generator enter time, otherwise timeout applies from last
        
        report = {'stream':None, # Status of the stream
                  'stab':None, # Stability of the result
                  'conf':None, # Confidence in the transcript
                  'isfin':None} # Is the result final according to Google
        
        with MicrophoneStream(self.rate, self.chunk, initout, timeout, maxtime, last) as stream:
            
            audio_generator = stream.generator()
            requests = (types.StreamingRecognizeRequest(audio_content=content)
                        for content in audio_generator)
            
            responses = self.client.streaming_recognize(self.streaming_config, requests)
            
            logger.info('Listening...')
            for response in responses:
                if not response.results:
                    continue

                result = response.results[0]
                if not result.alternatives:
                    continue

                transcript = result.alternatives[0].transcript
                stream.last = time.time()
                if stream.firsttime is None:
                    stream.firsttime = stream.last
                report['stream'] = stream.status
                report['stab'] = result.stability
                report['conf'] = result.alternatives[0].confidence
                report['isfin'] = result.is_final
                
                logger.debug('[tmp] ' + transcript + ' ' + str(report))
                if result.is_final or report['stream'] != 'open':
                    if re.search(r'\b(exit|quit)\b', transcript, re.I):
                        print('Exiting..')
                        break
            
            if report['stream'] is None:
                report['stream'] = stream.status
                report['trans'] = None
            else:
                report['trans'] = transcript
            logger.info('[fin] report = ' + str(report))      

        



        
