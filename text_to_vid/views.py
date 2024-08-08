from django.shortcuts import render
from PIL import Image, ImageDraw, ImageFont
import pyttsx3
from moviepy.editor import ImageClip, concatenate_videoclips, AudioFileClip
import numpy as np

# Create your views here.

def make_video(request):
    if request.method == 'POST':
        texts = request.POST['content'].split('. ')
        name = request.POST['video_name']
        for i, text in enumerate(texts):
            print(i, text)
             # Create a new image with a white background
            width, height = 1200, 700
            background_color = (255, 255, 255)
            img = Image.new('RGB', (width, height), background_color)

            # Add text to the image
            font_path = "arial.ttf"
            font_size = 36
            font = ImageFont.truetype(font_path, font_size)
            draw = ImageDraw.Draw(img)

            # Generate new audio using text
            engine = pyttsx3.init()
            voices = engine.getProperty('voices')

            engine.setProperty('rate', 150)
            engine.setProperty('voice', voices[1].id)

            engine.save_to_file(text, f'{name}_{i}.mp3')
            engine.runAndWait()

            # Wrap the text to fit in the image width
            text_lines = []
            words = text.split()
            while words:
                line = ""
                while words and draw.textsize(line + words[0], font)[0] < 1000:
                    line += words.pop(0) + " "
                text_lines.append(line.strip())

            # Calculate the total text height
            text_height = sum(draw.textsize(line, font)[1] for line in text_lines)

            # Draw the text in the center of the image
            y = (height - text_height) // 2
            for line in text_lines:
                text_width, text_height = draw.textsize(line, font)
                x = (width - text_width) // 2
                draw.text((x, y), line, font=font, fill=(0, 0, 0))
                y += text_height


            # Convert the image to a numpy array
            img_array = np.array(img)

            # Set the duration of the video clip and load the audio file
            clip_duration = 5
            audio = AudioFileClip(f'{name}_{i}.mp3')

            # Create the video clip with the text image and audio track
            clip = ImageClip(img_array, duration=clip_duration)
            clip = clip.set_audio(audio)

            # Create a list of clips and concatenate them
            clip_list = [clip]
            final_clip = concatenate_videoclips(clip_list)

            # Write the final clip to a video file
            final_clip.write_videofile(f'{name}_{i}.mp4', fps=30)





    return render(request, 'home.html')