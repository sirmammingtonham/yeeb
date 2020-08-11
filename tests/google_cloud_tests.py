import speech_recognition as sr

f = sr.AudioFile("../src/pain.wav")
r = sr.Recognizer()
with f as source:
    data = r.record(f)

with open("../src/audio/yeeb-cloud.json", "r") as f:
    j = f.read()


command_mapping = {
        # true if has args, false otherwise
        # bruh.py
        "help": ('help'),
        "clear": ('clear'),
        "snap": ('snap'),
        "spam": ('spam'),
        "cringe": ('thatsprettycringe'),
        "how long": ('howlong'),
        "code": ('code'),
        "censor": ('censor'),
        "invite": ('invite'),
        "die": ('die'),
        "swear": ('swear'),
        "swearat": ('swearat'),

        "jacobify": ('jacobify'),
        "prolixify": ('prolixify'),
        "verbosify": ('verbosify'),

        "cumber": ('cumber'),
        "girl cumber": ('girlcumber'),
        "cum": ('cum'),
        "korra": ('korra'),
        "valortne": ('valortne'),

        # card.py?
        "shitty hearthstone": ('shitty hearthstone'),
        "hearthstone join": ('hearthstone join'),
        "hearthstone reset": ('hearthstone reset'),
        "time to duel": ('hearthstone itstimetoduel'),

        # music.py
        "connect": ('connect'),
        "play": ('play'),
        "now playing": ('now playing'),
        "on jah": ('onjah'),
        "moment": ('moment'),
        "sicko mode": ('go'),
        "jo jo": ('jojo'),
        "gio gio": ('giogio'),
        "pendi": ('pendi'),
        "oof": ('oof'),
        "x games": ('xgames'),
        "this": ('this'),
        "that": ('that'),
        "finna": ('finna'),
        "stop": ('stop'),
        "shid": ('shid'),

        # speech.py
        # "listen": ('listen'),
        "cancel": ('cancel'),
        "test": ('test'),
    }

print(r.recognize_google_cloud(
    data, credentials_json=j, preferred_phrases=list(command_mapping.keys()), show_all=False
))
