import asyncio
import edge_tts
from moviepy.editor import *
import requests

async def make():
    print("Starting...")
    # Fixed script - Gemini hata diya fail ho raha tha
    script = "Chanda mama gol matol, roti jaisi gol. Chanda mama aao ji, kheer puri khao ji."
    
    # Voice
    print("Voice bana raha hu...")
    await edge_tts.Communicate(script, "hi-IN-AarohiNeural").save("voice.mp3")
    
    # Video - Direct link, bina kisi jugaad ke
    print("Video download...")
    url = "https://videos.pexels.com/video-files/3209211/3209211-hd_1920_1080_25fps.mp4"
    open("bg.mp4", 'wb').write(requests.get(url).content)
    
    # Final
    print("Final video bana raha hu...")
    audio = AudioFileClip("voice.mp3")
    bg = VideoFileClip("bg.mp4").subclip(0, audio.duration).resize((1080,1920))
    final = bg.set_audio(audio)
    final.write_videofile("final.mp4", fps=24)
    print("HO GAYA READY")

asyncio.run(make())
