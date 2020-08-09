import discord
from discord.ext import commands
from discord.rtp import SilencePacket, RTPPacket
from discord.opus import Decoder
from discord.reader import AudioSink, WaveSink

import speech_recognition as sr
import io
import audioop
import wave
import threading
import asyncio

bot = commands.Bot(command_prefix='bruh ')
bot.remove_command('help')

if not discord.opus.is_loaded():
    discord.opus.load_opus('libopus.so')


async def on_ready():
    await bot.change_presence(activity=discord.Game(name="testing shid"))
    print('we back')

bot.add_listener(on_ready)

# class DiscordPCMData(sr.AudioData):
#     def __init__(self, sink, vc):
#         # self.stream = None
#         self.stream = sink
#         self.vc = vc

#         self.CHUNK_SIZE = Decoder.FRAME_SIZE # 3840?
#         self.SAMPLE_RATE = Decoder.SAMPLING_RATE
#         self.SAMPLE_WIDTH = Decoder.SAMPLE_SIZE//Decoder.CHANNELS

#     def __enter__(self):
#         pass

#     def __exit__(self, exc_type, exc_value, traceback):
#         pass


# class DiscordPCMStream(sr.AudioSource):
#     def __init__(self, bytes_file, wav_object):
#         # self.filename_or_fileobject = filename_or_fileobject
#         self.stream = None
#         self.DURATION = None

#         self.audio = bytes_file
#         self.wav_object = wav_object
#         self.little_endian = False
#         self.SAMPLE_RATE = None
#         self.CHUNK = None
#         self.FRAME_COUNT = None

#         self.bytesPosition = 0

#     def __enter__(self):
#         assert self.stream is None, "This audio source is already inside a context manager"

#         # read the file as WAV
#         self.audio.seek(0)
#         self.little_endian = True

#         self.SAMPLE_WIDTH = self.wav_object.getsampwidth()

#         # 24-bit audio needs some special handling for old Python versions (workaround for https://bugs.python.org/issue12866)
#         samples_24_bit_pretending_to_be_32_bit = False

#         self.SAMPLE_RATE = self.wav_object.getframerate()
#         self.CHUNK = 4096 # 50 frames per second, 81.92 seconds per chunk?
#         self.FRAME_COUNT = self.wav_object.getnframes()
#         self.DURATION = self.FRAME_COUNT / float(self.SAMPLE_RATE)
#         self.stream = DiscordPCMStream.AudioFileStream(self.audio, self.wav_object, self.little_endian, samples_24_bit_pretending_to_be_32_bit, self.CHUNK)
#         return self

#     def __exit__(self, exc_type, exc_value, traceback):
#         # self.audio.close()
#         self.stream = None
#         self.DURATION = None

#     class AudioFileStream(object):
#         def __init__(self, audio, wav_object, little_endian, samples_24_bit_pretending_to_be_32_bit, chunk):
#             self.audio = audio  # an audio file object (e.g., a `wave.Wave_read` instance)
#             self.wav_object = wav_object
#             self.little_endian = little_endian  # whether the audio data is little-endian (when working with big-endian things, we'll have to convert it to little-endian before we process it)
#             self.samples_24_bit_pretending_to_be_32_bit = samples_24_bit_pretending_to_be_32_bit  # this is true if the audio is 24-bit audio, but 24-bit audio isn't supported, so we have to pretend that this is 32-bit audio and convert it on the fly
#             self.CHUNK = chunk

#         def read(self, size=-1):
#             # print(self.audio.tell())
#             # self.audio.seek(self.audio.tell() - 0 if size == -1 else size)
#             # print(f"read: {self.audio.tell()}")
#             buffer = self.audio.read(self.audio.getnframes() if size == -1 else size)
#             # buffer = self.audio.getvalue()[:self.audio.tell()]
#             if not isinstance(buffer, bytes): buffer = b""  # workaround for https://bugs.python.org/issue24608

#             sample_width = self.wav_object.getsampwidth()
#             if not self.little_endian:  # big endian format, convert to little endian on the fly
#                 if hasattr(audioop, "byteswap"):  # ``audioop.byteswap`` was only added in Python 3.4 (incidentally, that also means that we don't need to worry about 24-bit audio being unsupported, since Python 3.4+ always has that functionality)
#                     buffer = audioop.byteswap(buffer, sample_width)
#                 else:  # manually reverse the bytes of each sample, which is slower but works well enough as a fallback
#                     buffer = buffer[sample_width - 1::-1] + b"".join(buffer[i + sample_width:i:-1] for i in range(sample_width - 1, len(buffer), sample_width))

#             # workaround for https://bugs.python.org/issue12866
#             if self.samples_24_bit_pretending_to_be_32_bit:  # we need to convert samples from 24-bit to 32-bit before we can process them with ``audioop`` functions
#                 buffer = b"".join(b"\x00" + buffer[i:i + sample_width] for i in range(0, len(buffer), sample_width))  # since we're in little endian, we prepend a zero byte to each 24-bit sample to get a 32-bit sample
#                 sample_width = 4  # make sure we thread the buffer as 32-bit audio now, after converting it from 24-bit audio
#             if self.wav_object.getnchannels() != 1:  # stereo audio
#                 buffer = audioop.tomono(buffer, sample_width, 1, 1)  # convert stereo audio data to mono

#             # print(buffer)
#             return buffer

class DiscordPCMStream(sr.AudioSource):
    """
    pls work
    """

    def __init__(self, data):
        self.stream = None

        self.stream_data = data
        self.little_endian = True  # RIFF WAV is a little-endian format (most ``audioop`` operations assume that the frames are stored in little-endian form)
        self.SAMPLE_RATE = Decoder.SAMPLING_RATE
        self.CHUNK = Decoder.FRAME_SIZE  # 3840
        self.SAMPLE_WIDTH = Decoder.SAMPLE_SIZE//Decoder.CHANNELS
        self.FRAME_COUNT = None
        self.DURATION = None

    def __enter__(self):
        assert self.stream is None, "This audio source is already inside a context manager"

        self.stream = DiscordPCMStream.PCMStream(self.stream_data, self.SAMPLE_WIDTH)

        self.FRAME_COUNT = len(b"".join(self.stream_data))
        self.DURATION = self.FRAME_COUNT / float(self.SAMPLE_RATE)

        print(f"FRAME COUNT: {self.FRAME_COUNT}")
        return self

    def __exit__(self, exc_type, exc_value, traceback):
        self.stream = None
        self.DURATION = None
    
    # def updateStream(self):
    #     self.stream = DiscordPCMStream.PCMStream(self.stream_data, self.SAMPLE_WIDTH)

    class PCMStream(object):
        def __init__(self, stream_data, sample_width):
            self.stream_data = stream_data  # an audio file object (e.g., a `wave.Wave_read` instance)
            self.SAMPLE_WIDTH = sample_width
            self.bytesPosition = 0

        def read(self, sample_offset=0):
            buffer = b"".join(self.stream_data)[self.bytesPosition:self.bytesPosition+sample_offset]
            self.bytesPosition += sample_offset

            buffer = audioop.tomono(buffer, self.SAMPLE_WIDTH, 1, 1)  # convert stereo audio data to mono (this is the part that fucked me up bruh)
            return buffer

def callback(recognizer_instance, audio_data):
        # with open("pain.wav", "wb+") as f:
        #     f.write(audio_data.get_wav_data())
        # # try:
        # print(recognizer_instance.recognize_google(audio_data, show_all=True))
        # # except Exception as e:
        #     print(e)
        # print(audio_data.get_raw_data())
        # pass
        print("callback called!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!")

class BytesLoop(io.IOBase):
    def __init__(self, buf=b''):
        self.buf = buf
    def read(self, n=-1):
        inp = io.BytesIO(self.buf)
        b = inp.read(n)
        self.buf = self.buf[len(b):]
        return b
    def readinto(self, b):
        inp = io.BytesIO(self.buf)
        l = inp.readinto(b)
        self.buf = self.buf[l:]
        return l
    def write(self, b):
        outp = io.BytesIO()
        l = outp.write(b)
        self.buf += outp.getvalue()
        return l
    def getvalue(self):
        return self.buf

class WavStream:
    def __init__(self):
        e

class TestSink(AudioSink):
    sampwidth = Decoder.SAMPLE_SIZE//Decoder.CHANNELS
    framerate = Decoder.SAMPLING_RATE*2
    num_frames = Decoder.SAMPLES_PER_FRAME

    def __init__(self):
        self.data = []
        self.needs_processing = True
        self.r = sr.Recognizer()
        # self.wav_file = io.BytesIO()#"pain.wav" #io.BytesIO()  # "test.wav"  # BytesLoop()
        # self.wav_writer = wave.open(self.wav_file, "wb")
        # self.wav_writer.setnchannels(Decoder.CHANNELS)
        # self.wav_writer.setsampwidth(Decoder.SAMPLE_SIZE//Decoder.CHANNELS)
        # self.wav_writer.setframerate(Decoder.SAMPLING_RATE)
        self.stream = DiscordPCMStream(self.data)
        self.processing = False

    def test(self):
        # reader = wave.open("pain.wav", "rb")
        # with open("bruh3.data", "wb+") as f:
        #     f.write(reader.readframes(reader.getnframes()))
        with open("bruh3.data", "rb") as f:
            data = f.read()
        # data = audioop.tomono(data, Decoder.SAMPLE_SIZE//Decoder.CHANNELS, 1, 1)
        # audio = sr.AudioData(data, Decoder.SAMPLING_RATE, Decoder.SAMPLE_SIZE//Decoder.CHANNELS)

        # stream = DiscordPCMStream(data)
        with self.stream as source:
            # frames = io.BytesIO()
            # while True:  # loop for the total number of chunks needed

            #     buffer = source.stream.read(source.CHUNK)
            #     if len(buffer) == 0: break

            #     frames.write(buffer)

            # frame_data = frames.getvalue()
            # frames.close()
            # audio = sr.AudioData(frame_data, source.SAMPLE_RATE, source.SAMPLE_WIDTH)
            # audio = self.recognizer.record(source)
            audio = self.recognizer.listen(source, snowboy_configuration=("../src/audio/snowboy", ["../src/audio/snowboy/bruh.pmdl"]))
            print(f"audio: {audio}")
        # pass
        with open("pain3.wav", "wb+") as f:
            f.write(audio.get_wav_data())


    def processAudio(self, callback):
        assert isinstance(self.stream, sr.AudioSource), "Source must be an audio source"
        running = [True]

        def threaded_listen():
            with self.stream as s:
                while running[0]:
                    try:  # listen for 3 seconds, then check again if the stop function has been called
                        audio = self.r.listen(s, timeout=3, phrase_time_limit=5, snowboy_configuration=(
                            "../src/audio/snowboy", ["../src/audio/snowboy/bruh.pmdl"]
                        ))
                    except sr.WaitTimeoutError:  # listening timed out, just try again
                        print("timeoutted")
                    else:
                        print("success?")
                        if running[0]: callback(self, audio)

        def stopper(wait_for_stop=True):
            running[0] = False
            if wait_for_stop:
                listener_thread.join()  # block until the background thread is done, which can take around 1 second

        listener_thread = threading.Thread(target=threaded_listen)
        listener_thread.daemon = True
        listener_thread.start()

        self.stop = stopper
        return self.stop

        # stream = DiscordPCMStream(self.data)
        # with self.stream as source:
        #     audio = self.recognizer.listen(source, snowboy_configuration=("../src/audio/snowboy", ["../src/audio/snowboy/bruh.pmdl"]))
        # with open("pain3.wav", "wb+") as f:
        #     f.write(audio.get_wav_data())

        # test = wave.open(self.wav_file, "rb")

        # stream = sr.AudioFile(self.wav_file)
        # stream = sr.AudioFile.AudioFileStream(test, True, False)
        # self.recognizer.listen_in_background(stream, callback)



        # with stream as source:
        #     print(source.stream.read(4096))
        # print(self.data)
        # print("processing")
        # raw = b''.join(self.data)
        # self.wav_writer.writeframes(raw)

        # print(self.wav_writer.getsampwidth())
        # print(self.wav_writer.getsampwidth())
        # print(self.wav_writer.getsampwidth())
        # self.processing = True

        # stream = DiscordPCMStream(self.wav_file, self.wav_writer)
        # with stream as source:
        # # #     data = self.recognizer.record(source)
        #     test = self.recognizer.listen(source, snowboy_configuration=("../src/audio/snowboy", ["../src/audio/snowboy/bruh.pmdl"]))
        #     print(test.get_raw_data())
        # self.recognizer.listen_in_background(stream, callback)

        # # with stream as source:
        # #     pass
        #     # data = source.stream.read(4096)
        # #     with open("bruh333.wav", "wb+") as f:
        # #         f.write(data)
        # #     print(source.stream.read(4096))

        # # assert(self.data == self.wav_file.getvalue())

        # # print(self.wav_writer.getsampwidth())

        # self.wav_file.seek(0)

        # frames = io.BytesIO()
        # while True:
        #     buffer = self.wav_file.read(Decoder.FRAME_SIZE)
        #     if len(buffer) == 0: break

        #     frames.write(buffer)
        


        # data = sr.AudioData(b''.join(self.data), Decoder.SAMPLING_RATE*2, Decoder.SAMPLE_SIZE//Decoder.CHANNELS)
        # frames.close()
        # with open("pain.wav", "wb+") as f:
        #     f.write(data.get_wav_data())

        # # self.needs_processing = False
        # self.processing = False
        # with open("bruh2.data", "wb+") as f:
        #     f.write(b"".join(self.data))

    def write(self, data):
        # BytesLoop.write(data.data)
        # if not self.processing:
        # if len(self.data) >= 500:
        #     self.data.clear()
        #     self.stream.updateStream()
        # if data.packet == SilencePacket:
        #     self.data.clear()
        # else:
        self.data.append(data.data)


    def read(self):
        pass

    def cleanup(self):
        pass


sink = TestSink()

def callback(r_instance, audio):
    print("callback called")
    print(audio.get_raw_data())

@bot.command()
async def test(ctx):
    # r = sr.Recognizer()
    # source = DiscordPCMSource(TestSink(), vc)
    # r.listen(source)
    vc = await ctx.author.voice.channel.connect()
    vc.listen(sink)
    await asyncio.sleep(3)
    sink.processAudio(callback)
    # sink.processAudio()
    # sink.test()


@bot.command()
async def process(ctx):
    sink.processAudio()


@bot.command()
async def record(ctx):
    vc = await ctx.author.voice.channel.connect()
    vc.listen(WaveSink("bruh.wav"))


@bot.command()
async def check_frame_size(ctx):
    await ctx.send(str(Decoder.FRAME_SIZE))


@bot.command()
async def coom(ctx):
    await bot.logout()

if __name__ == "__main__":
    # sink.test()

    with open('../src/token.txt', 'r') as f:
        TOKEN = f.readline()

    bot.run(TOKEN)