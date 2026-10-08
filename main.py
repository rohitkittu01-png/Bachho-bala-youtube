import asyncio, requests, subprocess
import edge_tts

async def make():
    print("Starting...")
    script = "Chanda mama gol matol, roti jaisi gol."
    await edge_tts.Communicate(script, "hi-IN-AarohiNeural").save("voice.mp3")
    
    print("Video download...")
    url = "https://videos.pexels.com/video-files/3209211/3209211-hd_1920_1080_25fps.mp4"
    open("bg.mp4", 'wb').write(requests.get(url).content)
    
    print("Merging...")
    subprocess.run("ffmpeg -y -i bg.mp4 -i voice.mp3 -shortest -vf scale=1080:1920 final.mp4", shell=True)
    print("DONE")

asyncio.run(make())
