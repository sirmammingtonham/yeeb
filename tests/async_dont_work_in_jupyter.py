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

    def __enter__(self):
        assert self.stream is None, "This audio source is already inside a context manager"

        # read the file as WAV
        self.audio.seek(0)
        self.little_endian = True

        self.SAMPLE_WIDTH = self.wav_object.getsampwidth()

        # 24-bit audio needs some special handling for old Python versions (workaround for https://bugs.python.org/issue12866)
        samples_24_bit_pretending_to_be_32_bit = False

        self.SAMPLE_RATE = self.wav_object.getframerate()
        self.CHUNK = 4096
        self.FRAME_COUNT = self.wav_object.getnframes()
        self.DURATION = self.FRAME_COUNT / float(self.SAMPLE_RATE)
        self.stream = DiscordPCMStream.AudioFileStream(self.audio, self.wav_object, self.little_endian, samples_24_bit_pretending_to_be_32_bit)
        return self

    def __exit__(self, exc_type, exc_value, traceback):
        # self.audio.close()
        self.stream = None
        self.DURATION = None

    class AudioFileStream(object):
        def __init__(self, audio, wav_object, little_endian, samples_24_bit_pretending_to_be_32_bit):
            self.audio = audio  # an audio file object (e.g., a `wave.Wave_read` instance)
            self.wav_object = wav_object
            self.little_endian = little_endian  # whether the audio data is little-endian (when working with big-endian things, we'll have to convert it to little-endian before we process it)
            self.samples_24_bit_pretending_to_be_32_bit = samples_24_bit_pretending_to_be_32_bit  # this is true if the audio is 24-bit audio, but 24-bit audio isn't supported, so we have to pretend that this is 32-bit audio and convert it on the fly

        def read(self, size=-1):
            buffer = self.audio.read(self.audio.getnframes() if size == -1 else size)
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
            return buffer


class TestSink(AudioSink):
    sampwidth = Decoder.SAMPLE_SIZE//Decoder.CHANNELS
    framerate = Decoder.SAMPLING_RATE
    num_frames = Decoder.SAMPLES_PER_FRAME

    def __init__(self):
        self.data = []
        self.needs_processing = True
        self.recognizer = sr.Recognizer()
        self.wav_file = io.BytesIO()
        self.wav_writer = wave.open(self.wav_file, "wb")
        self.wav_writer.setnchannels(Decoder.CHANNELS)
        self.wav_writer.setsampwidth(Decoder.SAMPLE_SIZE//Decoder.CHANNELS)
        self.wav_writer.setframerate(Decoder.SAMPLING_RATE)

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
            print(self.recognizer.recognize_google(audio))
        # wav_data = self.wav_file.getvalue()
        # print([i for i in xrange(len(wav_data)) if s1[i] != s2[i]])
        # assert(wav_data == raw)

        # print(wav_data)
        # print(raw)
        # try:
        # audio = sr.AudioData(wav_data, Decoder.SAMPLING_RATE,
        # Decoder.SAMPLE_SIZE//Decoder.CHANNELS)

        with open("bruh5.wav", "wb+") as f:
            f.write(audio.get_wav_data())
        # print(self.recognizer.recognize_google(audio, show_all=True))
        # except:
        #     print("bruh")
        self.needs_processing = False

    def write(self, data):
        self.wav_writer.writeframes(data.data)
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

bot.run("NTQ3MTU2NzAyNjI2MTg1MjMw.XxDEmQ.rchZQYc66BSPeLaeJEk0ifq-Q5Y")