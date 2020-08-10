from discord.opus import Decoder
from discord.reader import AudioSink

from .DiscordPCMStream import DiscordPCMStream
from .AudioClasses import WaitTimeoutError, RequestError, UnknownValueError, AudioData

import asyncio
import os, sys
import math
import audioop
import tempfile
import threading, collections, queue
import json
import base64

from oauth2client.client import GoogleCredentials
from googleapiclient.discovery import build
import googleapiclient.errors

import socket
import googleapiclient.http

snowboy_location = "audio/snowboy"
snowboy_hot_word_files = ["audio/snowboy/bruh.pmdl"]

sys.path.append(snowboy_location)
import snowboydetect
sys.path.pop()

class TranscriptionSink(AudioSink):
    def __init__(self, callback, loop):
        # recognizer variables
        self.energy_threshold = 300  # minimum audio energy to consider for recording
        self.dynamic_energy_threshold = True
        self.dynamic_energy_adjustment_damping = 0.15
        self.dynamic_energy_ratio = 1.5
        self.pause_threshold = 0.8  # seconds of non-speaking audio before a phrase is considered complete
        self.operation_timeout = None  # seconds after an internal operation (e.g., an API request) starts before it times out, or ``None`` for no timeout
        self.phrase_threshold = 0.3  # minimum seconds of speaking audio before we consider the speaking audio a phrase - values below this are ignored (for filtering out clicks and pops)
        self.non_speaking_duration = 0.5  # seconds of non-speaking audio to keep on both sides of the recording

        # sink variables
        self.buffer = asyncio.Queue()
        self.callback = callback
        self.stream = DiscordPCMStream(self.buffer)

        self.loop = loop
        self.stop = False


    async def snowboy_wait_for_hot_word(self, source, timeout=None):
        """ modified from SpeechRecognition python """
        detector = snowboydetect.SnowboyDetect(
            resource_filename=os.path.join(snowboy_location, "resources", "common.res").encode(),
            model_str=",".join(snowboy_hot_word_files).encode()
        )
        detector.SetAudioGain(1.0)
        detector.SetSensitivity(",".join(["0.4"] * len(snowboy_hot_word_files)).encode())
        snowboy_sample_rate = detector.SampleRate()

        elapsed_time = 0
        seconds_per_buffer = float(source.CHUNK) / source.SAMPLE_RATE
        resampling_state = None

        # buffers capable of holding 5 seconds of original and resampled audio
        five_seconds_buffer_count = int(math.ceil(5 / seconds_per_buffer))
        frames = collections.deque(maxlen=five_seconds_buffer_count)
        resampled_frames = collections.deque(maxlen=five_seconds_buffer_count)
        while True:
            elapsed_time += seconds_per_buffer
            if timeout and elapsed_time > timeout:
                raise WaitTimeoutError("listening timed out while waiting for hotword to be said")

            buffer = await source.stream.read(source.CHUNK)
            if len(buffer) == 0: break  # reached end of the stream
            frames.append(buffer)

            # resample audio to the required sample rate
            resampled_buffer, resampling_state = audioop.ratecv(buffer, source.SAMPLE_WIDTH, 1, source.SAMPLE_RATE, snowboy_sample_rate, resampling_state)
            resampled_frames.append(resampled_buffer)

            # run Snowboy on the resampled audio
            snowboy_result = detector.RunDetection(b"".join(resampled_frames))
            assert snowboy_result != -1, "Error initializing streams or reading audio data"
            if snowboy_result > 0: 
                print("bruh has been uttered")
                break  # wake word found
        return b"".join(frames), elapsed_time

    async def listen(self, source, timeout=None, phrase_time_limit=None, snowboy_configuration=None):
        """ modified from SpeechRecognition python """
        seconds_per_buffer = float(source.CHUNK) / source.SAMPLE_RATE
        pause_buffer_count = int(math.ceil(self.pause_threshold / seconds_per_buffer))  # number of buffers of non-speaking audio during a phrase, before the phrase should be considered complete
        phrase_buffer_count = int(math.ceil(self.phrase_threshold / seconds_per_buffer))  # minimum number of buffers of speaking audio before we consider the speaking audio a phrase
        non_speaking_buffer_count = int(math.ceil(self.non_speaking_duration / seconds_per_buffer))  # maximum number of buffers of non-speaking audio to retain before and after a phrase

        # read audio input for phrases until there is a phrase that is long enough
        elapsed_time = 0  # number of seconds of audio read
        buffer = b""  # an empty buffer means that the stream has ended and there is no data left to read
        snowboy_configuration = None
        while True:
            frames = collections.deque()

            # read audio input until the hotword is said
            # snowboy_location, snowboy_hot_word_files = snowboy_configuration
            buffer, delta_time = await self.snowboy_wait_for_hot_word(source, timeout)
            elapsed_time += delta_time
            if len(buffer) == 0: break  # reached end of the stream

            # read audio input until the phrase ends
            pause_count, phrase_count = 0, 0
            phrase_start_time = elapsed_time
            while True:
                # handle phrase being too long by cutting off the audio
                elapsed_time += seconds_per_buffer
                if phrase_time_limit and elapsed_time - phrase_start_time > phrase_time_limit:
                    break

                buffer = await source.stream.read(source.CHUNK)
                if len(buffer) == 0: break  # reached end of the stream
                frames.append(buffer)
                phrase_count += 1

                # check if speaking has stopped for longer than the pause threshold on the audio input
                energy = audioop.rms(buffer, source.SAMPLE_WIDTH)  # unit energy of the audio signal within the buffer
                if energy > self.energy_threshold:
                    pause_count = 0
                else:
                    pause_count += 1
                if pause_count > pause_buffer_count:  # end of the phrase
                    break

            # check how long the detected phrase is, and retry listening if the phrase is too short
            phrase_count -= pause_count  # exclude the buffers for the pause before the phrase
            if phrase_count >= phrase_buffer_count or len(buffer) == 0: break  # phrase is long enough or we've reached the end of the stream, so stop listening

        # obtain frame data
        for i in range(pause_count - non_speaking_buffer_count - 5): frames.pop()  # remove extra non-speaking frames at the end, but leave a bit for detection purposes
        frame_data = b"".join(frames)
        frame_data = frame_data[source.CHUNK:] # remove the first chunk so we don't hear any part of the bruh
        return AudioData(frame_data, source.SAMPLE_RATE, source.SAMPLE_WIDTH)


    async def recognize_sphinx(self, audio_data, keyword_entries=None, show_all=False):
        """ modified from SpeechRecognition python """
        assert isinstance(audio_data, AudioData), "``audio_data`` must be audio data"
        assert keyword_entries is None or all(isinstance(keyword, (type(""), type(u""))) and 0 <= sensitivity <= 1 for keyword, sensitivity in keyword_entries), "``keyword_entries`` must be ``None`` or a list of pairs of strings and numbers between 0 and 1"
        print("starting recognition")
        language_directory = "audio/sphinx_en-US"
            
        acoustic_parameters_directory = os.path.join(language_directory, "acoustic-model")
        language_model_file = os.path.join(language_directory, "language-model.lm.bin")
        phoneme_dictionary_file = os.path.join(language_directory, "pronounciation-dictionary.dict")


        # create decoder object
        config = pocketsphinx.Decoder.default_config()
        config.set_string("-hmm", acoustic_parameters_directory)  # set the path of the hidden Markov model (HMM) parameter files
        config.set_string("-lm", language_model_file)
        config.set_string("-dict", phoneme_dictionary_file)
        config.set_string("-logfn", os.devnull)  # disable logging (logging causes unwanted output in terminal)
        decoder = pocketsphinx.Decoder(config)

        # obtain audio data
        raw_data = audio_data.get_raw_data(convert_rate=16000, convert_width=2)  # the included language models require audio to be 16-bit mono 16 kHz in little-endian format
        # obtain recognition results
        if keyword_entries is not None:  # explicitly specified set of keywords
            with tempfile.NamedTemporaryFile("w") as f:
                # generate a keywords file - Sphinx documentation recommendeds sensitivities between 1e-50 and 1e-5
                f.writelines("{} /1e{}/\n".format(keyword, 100 * sensitivity - 110) for keyword, sensitivity in keyword_entries)
                f.flush()

                # perform the speech recognition with the keywords file (this is inside the context manager so the file isn;t deleted until we're done)
                decoder.set_kws("keywords", f.name)
                decoder.set_search("keywords")
                decoder.start_utt()  # begin utterance processing
                decoder.process_raw(raw_data, False, True)  # process audio data with recognition enabled (no_search = False), as a full utterance (full_utt = True)
                decoder.end_utt()  # stop utterance processing

        else:  # no keywords, perform freeform recognition
            decoder.start_utt()  # begin utterance processing
            decoder.process_raw(raw_data, False, True)  # process audio data with recognition enabled (no_search = False), as a full utterance (full_utt = True)
            decoder.end_utt()  # stop utterance processing

        if show_all: return decoder
        # return results
        hypothesis = decoder.hyp()
        if hypothesis is not None: 
            return hypothesis.hypstr
        raise UnknownValueError()  # no transcriptions available

    async def recognize_google_cloud(self, audio_data, preferred_phrases, credentials_json=None, show_all=False):
        """ modified from SpeechRecognition python """

        # See https://cloud.google.com/speech/reference/rest/v1/RecognitionConfig
        flac_data = audio_data.get_flac_data(
            convert_rate=None if 8000 <= audio_data.sample_rate <= 48000 else max(8000, min(audio_data.sample_rate, 48000)),  # audio sample rate must be between 8 kHz and 48 kHz inclusive - clamp sample rate into this range
            convert_width=2  # audio samples must be 16-bit
        )

        if self.operation_timeout and socket.getdefaulttimeout() is None:
            # override constant (used by googleapiclient.http.build_http())
            googleapiclient.http.DEFAULT_HTTP_TIMEOUT_SEC = self.operation_timeout

        api_credentials = GoogleCredentials.from_stream(credentials_json)

        speech_service = build("speech", "v1", credentials=api_credentials, cache_discovery=False)
        speech_config = {"encoding": "FLAC", 
            "sampleRateHertz": audio_data.sample_rate, 
            "languageCode": "en-US", 
            "speechContexts": [{"phrases": preferred_phrases}]
        }
        if show_all:
            speech_config["enableWordTimeOffsets"] = True  # some useful extra options for when we want all the output
        request = speech_service.speech().recognize(body={"audio": {"content": base64.b64encode(flac_data).decode("utf8")}, "config": speech_config})

        try:
            response = request.execute()
        except googleapiclient.errors.HttpError as e:
            raise RequestError(e)
        except URLError as e:
            raise RequestError("recognition connection failed: {0}".format(e.reason))
        
        if show_all: return response
        if "results" not in response or len(response["results"]) == 0: raise UnknownValueError()
        transcript = ""
        for result in response["results"]:
            transcript += result["alternatives"][0]["transcript"].strip() + " "

        return transcript

    async def initListenerLoop(self):
        while not self.stop:
            with self.stream as source:
                audio = await self.listen(source, snowboy_configuration=(
                    "../src/audio/snowboy", ["../src/audio/snowboy/bruh.pmdl"]
                ))
                await self.callback(audio)

    def write(self, data):
        asyncio.run_coroutine_threadsafe(self.buffer.put(data.data), loop=self.loop)
        

    def cleanup(self):
        self.stop = True