from discord.rtp import SilencePacket, RTPPacket
from discord.opus import Decoder
from discord.reader import AudioSink, WaveSink

from .DiscordPCMStream import DiscordPCMStream

import io
import wave
# import speech_recognition as sr

class TranscriptionSink(AudioSink):
    sampwidth = Decoder.SAMPLE_SIZE//Decoder.CHANNELS
    framerate = Decoder.SAMPLING_RATE
    num_frames = Decoder.SAMPLES_PER_FRAME

    def __init__(self, recognizer, processAudioCallback):
        self.callback = processAudioCallback
        self.needs_processing = True
        self.recognizer = recognizer
        self.wav_file = io.BytesIO()
        self.wav_writer = wave.open(self.wav_file, "wb")
        self.wav_writer.setnchannels(Decoder.CHANNELS)
        self.wav_writer.setsampwidth(Decoder.SAMPLE_SIZE//Decoder.CHANNELS)
        self.wav_writer.setframerate(Decoder.SAMPLING_RATE)

        self.stop = None

    def processAudio(self):
        # print(self.data)
        # print("processing")
        # raw = b''.join(self.data)
        # self.wav_writer.writeframes(raw)

        # print(self.wav_writer.getsampwidth())
        # print(self.wav_writer.getsampwidth())
        # print(self.wav_writer.getsampwidth())
        stream = DiscordPCMStream(self.wav_file, self.wav_writer)
        
        with stream as source:
            audio = self.recognizer.record(source)
            with open("bruh5.wav", "wb+") as f:
                f.write(audio.get_wav_data())
            print(self.recognizer.recognize_google(audio))
        # self.stop = self.recognizer.listen_in_background(stream, self.callback)

            # audio = self.recognizer.listen_in_background(source, self.callback)
            # print(self.recognizer.recognize_google(audio))
        # wav_data = self.wav_file.getvalue()
        # print([i for i in xrange(len(wav_data)) if s1[i] != s2[i]])
        # assert(wav_data == raw)

        # print(wav_data)
        # print(raw)
        # try:
        # audio = sr.AudioData(wav_data, Decoder.SAMPLING_RATE,
        # Decoder.SAMPLE_SIZE//Decoder.CHANNELS)

        # with open("bruh5.wav", "wb+") as f:
        #     f.write(audio.get_wav_data())
        # print(self.recognizer.recognize_google(audio, show_all=True))
        # except:
        #     print("bruh")
        # self.needs_processing = False

    def write(self, data):
        self.wav_writer.writeframes(data.data)
        # self.data.append(data.data)
        # if isinstance(data.packet, RTPPacket):
        #     print('got data')
        #     self.wav_writer.writeframes(data.data)
        # #     self.data.append(data.data)
        #     self.needs_processing = True

        # elif self.needs_processing:
        #     self.processAudio()
        #     # self.data.clear()
        # print(len(data.data), data.user, data.packet)

    def read(self):
        pass

    def cleanup(self):
        self.stop()