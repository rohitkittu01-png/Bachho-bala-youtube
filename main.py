import asyncio, os, requests, random
import edge_tts
from moviepy.editor import *
import google.generativeai as genai

async def make():
    genai.configure(api_key=os.getenv("GEMINI_KEY"))
    model = genai.GenerativeModel('gemini-flash-latest')

    # 1. TITLE + SCRIPT + DESCRIPTION + HASHTAGS ek saath Gemini se
    prompt = """
    Ek bachho ki kavita/kahani bana. Output is format me de:
    TITLE:... (5 words ka catchy)
    SCRIPT:... (100 words hindi me)
    DESCRIPTION:... (YouTube ke liye 2 line)
    HASHTAGS: #kids #cartoon #...
    """
    full = model.generate_content(prompt).text
    print(full) # Ye log me dikhega

    # Simple parse
    try:
        title = full.split("TITLE:")[1].split("SCRIPT:")[0].strip()
        script = full.split("SCRIPT:")[1].split("DESCRIPTION:")[0].strip()
        desc = full.split("DESCRIPTION:")[1].split("HASHTAGS:")[0].strip()
        tags = full.split("HASHTAGS:")[1].strip()
    except:
        title = "Pyari Kavita"
        script = full[:200]
        desc = "Bachho ke liye pyari kavita"
        tags = "#kids #poem"

    # Save title/desc for YouTube upload later
    open("title.txt","w",encoding="utf-8").write(title)
    open("desc.txt","w",encoding="utf-8").write(desc + "\n\n" + tags)

    # 2. Cute Voice
    await edge_tts.Communicate(script, "hi-IN-AarohiNeural", rate="+10%").save("voice.mp3")

    # 3. Background video
    headers = {"Authorization": os.getenv("PEXELS_KEY")}
    v = requests.get(f"https://api.pexels.com/videos/search?query=kids cartoon&per_page=1", headers=headers).json()
    video_url = v['videos'][0]['video_files'][0]['link']
    open("bg.mp4", 'wb').write(requests.get(video_url).content)

    # 4. Final Video
    audio = AudioFileClip("voice.mp3")
    bg = VideoFileClip("bg.mp4").subclip(0, audio.duration).resize((1080,1920)).without_audio()
    txt = TextClip(title, fontsize=80, color='yellow', font='Arial-Bold', stroke_color='black', stroke_width=3, method='caption', size=(900, None)).set_duration(3).set_position(('center', 200))
    final = CompositeVideoClip([bg.set_audio(audio), txt])
    final.write_videofile("final.mp4", fps=30)

    print(f"READY: {title}")

asyncio.run(make())
import asyncio, os, requests, random, re
import edge_tts
from moviepy.editor import *
import google.generativeai as genai

async def make():
    genai.configure(api_key=os.getenv("GEMINI_KEY"))
    model = genai.GenerativeModel('gemini-flash-latest')

    # 1. TITLE + SCRIPT
    prompt = """
    Ek bachho ki chhoti kavita/kahani bana. Output is format me de:
    TITLE: 5 words ka catchy title
    SCRIPT: 100 words hindi me
    DESCRIPTION: YouTube ke liye 2 line
    HASHTAGS: #kids #cartoon
    """
    full = model.generate_content(prompt).text
    print(full)
    try:
        title = full.split("TITLE:")[1].split("SCRIPT:")[0].strip()
        script = full.split("SCRIPT:")[1].split("DESCRIPTION:")[0].strip()
    except:
        title = "Pyari Kavita"
        script = full[:200]

    # 2. Cute Voice
    await edge_tts.Communicate(script, "hi-IN-AarohiNeural", rate="+10%").save("voice.mp3")

    # 3. PEXELS JUGAAD - Bina Key ke
    def get_pexels_video(query="kids cartoon"):
        url = f"https://www.pexels.com/search/videos/{query}/"
        headers = {"User-Agent": "Mozilla/5.0"}
        html = requests.get(url, headers=headers).text
        links = re.findall(r'"video_files":\[{"id":.*? "link":"(https://.*?\.mp4)"', html)
        if not links:
            links = ["https://videos.pexels.com/video-files/3209211/3209211-hd_1920_1080_25fps.mp4"]
        video_url = links[0].replace("\\u002F", "/")
        print("Video URL:", video_url)
        open("bg.mp4", 'wb').write(requests.get(video_url).content)

    get_pexels_video("kids cartoon background")

    # 4. Final Pro Video
    audio = AudioFileClip("voice.mp3")
    bg = VideoFileClip("bg.mp4").subclip(0, audio.duration).resize((1080,1920)).without_audio()
    txt = TextClip(title, fontsize=80, color='yellow', font='Arial-Bold', stroke_color='black', stroke_width=3, method='caption', size=(900, None)).set_duration(3).set_position(('center', 200))
    final = CompositeVideoClip([bg.set_audio(audio), txt])
    final.write_videofile("final.mp4", fps=30)
    print(f"READY: {title}")

asyncio.run(make())
