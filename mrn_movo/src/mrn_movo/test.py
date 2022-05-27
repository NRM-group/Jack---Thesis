#!/usr/bin/env python3

import gtts
from playsound import playsound

tts = gtts.gTTS("Please touch my hand", lang="en-ie")

tts.save("hello.mp3")
playsound("hello.mp3")