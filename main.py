import asyncio, os, requests, random, re
import edge_tts
from moviepy.editor import *
from PIL import Image, ImageDraw, ImageFont
import google.generativeai as genai

async def make():
    genai.configure(api_key=os.getenv("GEMINI_KEY"))
    model = genai.GenerativeModel('gemini-1.5-flash')

    prompt = "Ek chhoti bachho ki kavita 80 words me hindi me likh. TITLE aur SCRIPT me de."
    full = model.generate_content(prompt).text
    print(full)
    title = full[:50]
    script = full

    # Voice
    await edge_tts.Communicate(script, "hi-IN-AarohiNeural", rate="+10%").save("voice.mp3")

    # PEXELS JUGAAD - Fixed
    headers = {"User-Agent": "Mozilla/5.0"}
    html = requests.get("https://www.pexels.com/search/videos/kids/", headers=headers).text
    links = re.findall(r'https://videos\.pexels\.com/video-files/\d+/\d+.*?\.mp4', html)
    if not links:
        links = ["https://videos.pexels.com/video-files/3209211/3209211-hd_1920_1080_25fps.mp4"]
    open("bg.mp4", 'wb').write(requests.get(links[0], headers=headers).content)

    # Video - No TextClip (Pillow se)
    audio = AudioFileClip("voice.mp3")
    bg = VideoFileClip("bg.mp4").subclip(0, audio.duration).resize((1080,1920)).without_audio()
    bg.write_videofile("temp.mp4", fps=24)

    # Final with audio
    final_bg = VideoFileClip("temp.mp4")
    final = final_bg.set_audio(audio)
    final.write_videofile("final.mp4", fps=24)
    print("READY")

asyncio.run(make())
