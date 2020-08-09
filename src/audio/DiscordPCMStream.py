import audioop

from discord.opus import Decoder

class DiscordPCMStream:
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

        self.FRAME_COUNT = self.stream_data.qsize()*self.CHUNK  #len(b"".join(self.stream_data))
        self.DURATION = self.FRAME_COUNT / float(self.SAMPLE_RATE)

        print(f"FRAME COUNT: {self.FRAME_COUNT}")

        return self

    def __exit__(self, exc_type, exc_value, traceback):
        self.stream = None
        self.DURATION = None

    class PCMStream(object):
        def __init__(self, stream_data, sample_width):
            self.stream_data = stream_data  # an audio file object (e.g., a `wave.Wave_read` instance)
            self.SAMPLE_WIDTH = sample_width
            self.bytesPosition = 0

        async def read(self, sample_offset=0):
            buffer = self.stream_data.get()
            buffer = audioop.tomono(buffer, self.SAMPLE_WIDTH, 1, 1)  # convert stereo audio data to mono (this is the part that fucked me up bruh)
            return buffer