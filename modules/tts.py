from pubsub import pub
from time import sleep
import pyttsx3

from elevenlabs import ElevenLabs, VoiceSettings, play
import os

class TTS:
    
    def __init__(self, **kwargs):
        self.translator = kwargs.get('translator', None)
        self.service = kwargs.get('service', 'pyttsx3')
        if self.service == 'elevenlabs':
            self.init_elevenlabs(kwargs)
        else:
            self.init_pyttsx3(kwargs)
        # Set subscribers
        pub.subscribe(self.speak, 'tts')

    def speak(self, msg):
        if self.service == 'elevenlabs':
            self.speak_elevenlabs(msg)
        else:
            self.speak_pyttsx3(msg)
        
    def init_pyttsx3(self, **kwargs):
        engine = pyttsx3.init()
        voices = engine.getProperty('voices')
        #rate = engine.getProperty('rate')
        #engine.setProperty('rate', rate+100)
        #for i in voices:
        engine.setProperty('voice', voices[10].id)
        print('voice' + voices[10].id)
        #engine.say('Hello, World!')
        #engine.runAndWait()
        self.engine = engine        

    def speak_pyttsx3(self, msg):
        pub.sendMessage('log', msg="[TTS] {}".format(msg))
        if self.translator is not None:
            msg = self.translator.request(msg)
        self.engine.say(msg)
        self.engine.runAndWait()
    
    def init_elevenlabs(self, **kwargs):
        self.client = ElevenLabs(
            api_key=os.getenv('ELEVENLABS_KEY') or ''
        )
        self.voice_id = kwargs.get('voice_id', None)
        
    def speak_elevenlabs(self, msg):
        # This uses ElevenLabs, create an API key and export in your .bashrc file using `export ELEVENLABS_KEY=<KEY>` before use
        output = self.client.text_to_speech.convert(
            voice_id=self.voice_id,
            optimize_streaming_latency="0",
            output_format="mp3_22050_32",
            text="msg",
            voice_settings=VoiceSettings(
                stability=0.1,
                similarity_boost=0.3,
                style=0.2,
            ),
        )

        play(output)
                
if __name__ == '__main__':
    tts = TTS()
    tts.speak('Test')
