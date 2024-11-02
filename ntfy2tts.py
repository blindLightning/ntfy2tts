import asyncio
import json
import signal
import sys
import ntfpy
import pyttsx3
from accessible_output3 import outputs as AO3
from pydub import AudioSegment, playback

audio = AudioSegment.from_wav("./sound.wav")
#fix keyboard interrupts.
signal.signal(signal.SIGINT, signal.SIG_DFL)


async def main():
    configFile=open("config.json")
    config=json.load(configFile)
    configFile.close()
    url=config["url"]
    topic=config["topic"]
    speaker = None
    screen_reader_output = config.get("screen_reader_output", False)
    if screen_reader_output: speaker = AO3.auto.Auto()
    sound = config.get("sound", True)
    client=ntfpy.NTFYClient(ntfpy.NTFYServer(url), topic)
    await client.subscribe(lambda message: speakMessage(message, screen_reader_output, speaker, sound))

def speak(text, screen_reader_output: bool, speaker: any, sound: bool=True):
    if sound: playback.play(audio)
    if not screen_reader_output:
        engin=pyttsx3.init()
        engin.say(text)
        engin.runAndWait()
    elif screen_reader_output and speaker is not None:
        speaker.speak(text)

def speakMessage(message: ntfpy.message.NTFYMessage, screen_reader_output: bool, speaker: any, sound: bool=True):
    starter=message.title if message.title is not None else message.topic
    speak(f'{starter}: {message.message}', screen_reader_output, speaker, sound)
if __name__ == "__main__":

    loop = asyncio.get_event_loop()
    try:
        loop.run_until_complete(main())
    except asyncio.CancelledError:
        pass