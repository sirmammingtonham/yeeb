import discord
from discord.ext import commands
from discord.rtp import SilencePacket, RTPPacket
from discord.opus import Decoder
from discord.reader import AudioSink, WaveSink

import speech_recognition as sr
import io
import audioop
import wave

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


class DiscordPCMStream(sr.AudioSource):
    def __init__(self, bytes_file, wav_object):
        # self.filename_or_fileobject = filename_or_fileobject
        self.stream = None
        self.DURATION = None

        self.audio = bytes_file
        self.wav_object = wav_object
        self.little_endian = False
        self.SAMPLE_RATE = None
        self.CHUNK = None
        self.FRAME_COUNT = None

        self.bytesPosition = 0

    def __enter__(self):
        assert self.stream is None, "This audio source is already inside a context manager"

        # read the file as WAV
        self.audio.seek(0)
        self.little_endian = True

        self.SAMPLE_WIDTH = self.wav_object.getsampwidth()

        # 24-bit audio needs some special handling for old Python versions (workaround for https://bugs.python.org/issue12866)
        samples_24_bit_pretending_to_be_32_bit = False

        self.SAMPLE_RATE = self.wav_object.getframerate()
        self.CHUNK = 4096 # 50 frames per second, 81.92 seconds per chunk?
        self.FRAME_COUNT = self.wav_object.getnframes()
        self.DURATION = self.FRAME_COUNT / float(self.SAMPLE_RATE)
        self.stream = DiscordPCMStream.AudioFileStream(self.audio, self.wav_object, self.little_endian, samples_24_bit_pretending_to_be_32_bit, self.CHUNK)
        return self

    def __exit__(self, exc_type, exc_value, traceback):
        # self.audio.close()
        self.stream = None
        self.DURATION = None

    class AudioFileStream(object):
        def __init__(self, audio, wav_object, little_endian, samples_24_bit_pretending_to_be_32_bit, chunk):
            self.audio = audio  # an audio file object (e.g., a `wave.Wave_read` instance)
            self.wav_object = wav_object
            self.little_endian = little_endian  # whether the audio data is little-endian (when working with big-endian things, we'll have to convert it to little-endian before we process it)
            self.samples_24_bit_pretending_to_be_32_bit = samples_24_bit_pretending_to_be_32_bit  # this is true if the audio is 24-bit audio, but 24-bit audio isn't supported, so we have to pretend that this is 32-bit audio and convert it on the fly
            self.CHUNK = chunk

        def read(self, size=-1):
            # print(self.audio.tell())
            # self.audio.seek(self.audio.tell() - 0 if size == -1 else size)
            # print(f"read: {self.audio.tell()}")
            buffer = self.audio.read(self.audio.getnframes() if size == -1 else size)
            # buffer = self.audio.getvalue()[:self.audio.tell()]
            if not isinstance(buffer, bytes): buffer = b""  # workaround for https://bugs.python.org/issue24608

            sample_width = self.wav_object.getsampwidth()
            if not self.little_endian:  # big endian format, convert to little endian on the fly
                if hasattr(audioop, "byteswap"):  # ``audioop.byteswap`` was only added in Python 3.4 (incidentally, that also means that we don't need to worry about 24-bit audio being unsupported, since Python 3.4+ always has that functionality)
                    buffer = audioop.byteswap(buffer, sample_width)
                else:  # manually reverse the bytes of each sample, which is slower but works well enough as a fallback
                    buffer = buffer[sample_width - 1::-1] + b"".join(buffer[i + sample_width:i:-1] for i in range(sample_width - 1, len(buffer), sample_width))

            # workaround for https://bugs.python.org/issue12866
            if self.samples_24_bit_pretending_to_be_32_bit:  # we need to convert samples from 24-bit to 32-bit before we can process them with ``audioop`` functions
                buffer = b"".join(b"\x00" + buffer[i:i + sample_width] for i in range(0, len(buffer), sample_width))  # since we're in little endian, we prepend a zero byte to each 24-bit sample to get a 32-bit sample
                sample_width = 4  # make sure we thread the buffer as 32-bit audio now, after converting it from 24-bit audio
            if self.wav_object.getnchannels() != 1:  # stereo audio
                buffer = audioop.tomono(buffer, sample_width, 1, 1)  # convert stereo audio data to mono

            # print(buffer)
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
3840

class TestSink(AudioSink):
    sampwidth = Decoder.SAMPLE_SIZE//Decoder.CHANNELS
    framerate = Decoder.SAMPLING_RATE*2
    num_frames = Decoder.SAMPLES_PER_FRAME

    def __init__(self):
        self.data = []
        self.needs_processing = True
        self.recognizer = sr.Recognizer()
        self.wav_file = io.BytesIO()#"pain.wav" #io.BytesIO()  # "test.wav"  # BytesLoop()
        self.wav_writer = wave.open(self.wav_file, "wb")
        self.wav_writer.setnchannels(Decoder.CHANNELS)
        self.wav_writer.setsampwidth(Decoder.SAMPLE_SIZE//Decoder.CHANNELS)
        self.wav_writer.setframerate(Decoder.SAMPLING_RATE)
        
        self.processing = False

    def test(self):
        # with open("bruh2.data", "rb") as f:
        #     data = f.read()
        
        audio = sr.AudioData(data, Decoder.SAMPLING_RATE*2, Decoder.SAMPLE_SIZE//Decoder.CHANNELS)

        # print(self.recognizer.recognize_sphinx(audio))
        # with open("pain2.wav", "wb+") as f:
        #     f.write(audio.get_wav_data())


        self.recognizer.listen(audio, snowboy_configuration=("../src/audio/snowboy", ["../src/audio/snowboy/bruh.pmdl"]))
        # pass

        # print('in test')
        # r = sr.Recognizer()
        # harvard = sr.AudioFile('OSR_us_000_0010_8k.wav')
        # with harvard as source:
        #     audio = r.record(source)
        # print('shit recorded')
        # print(r.recognize_google(audio))
        # print('huh')

    def processAudio(self):
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

        stream = DiscordPCMStream(self.wav_file, self.wav_writer)
        with stream as source:
        # #     data = self.recognizer.record(source)
            test = self.recognizer.listen(source, snowboy_configuration=("../src/audio/snowboy", ["../src/audio/snowboy/bruh.pmdl"]))
            print(test.get_raw_data())
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
        if not self.processing:
            self.data.append(data.data)
            self.wav_writer.writeframes(data.data)
        # print(f"write: {self.wav_file.tell()}")
        # self.processAudio()
        # self.data.append(data.data)
        # if isinstance(data.packet, RTPPacket):
        #     print('got data')
        #     self.data.append(data.data)
        #     self.needs_processing = True

        # elif self.needs_processing:
        #     self.processAudio()
        #     self.data.clear()
        # print(len(data.data), data.user, data.packet)

    def read(self):
        pass

    def cleanup(self):
        pass


sink = TestSink()


@bot.command()
async def test(ctx):
    # r = sr.Recognizer()
    # source = DiscordPCMSource(TestSink(), vc)
    # r.listen(source)
    vc = await ctx.author.voice.channel.connect()
    vc.listen(sink)
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

with open('../src/token.txt', 'r') as f:
    TOKEN = f.readline()

bot.run(TOKEN)