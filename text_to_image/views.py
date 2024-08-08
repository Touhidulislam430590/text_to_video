from io import BytesIO
from django.shortcuts import render
from django.http import HttpResponse
from PIL import Image, ImageDraw, ImageFont
from .models import GeneratedImage
from django.core.files.uploadedfile import InMemoryUploadedFile
import textwrap

def generate_image(request):
    if request.method == 'POST':
        # Get input text from the form
        text = request.POST['content']

        # Define image dimensions
        img_width = 400
        img_height = 200

        # Set font and font size
        font_path = 'arial.ttf'
        font_size = 30
        font = ImageFont.truetype(font_path, font_size)

        # Create draw object and calculate text dimensions
        draw = ImageDraw.Draw(Image.new('RGB', (1, 1)))
        text_width, text_height = draw.textsize(text, font)

        # Calculate number of lines and line height
        line_height = font.getsize('hg')[1]
        lines = textwrap.wrap(text, width=int(img_width/font_size))

        # Create new image object
        img = Image.new('RGB', (img_width, img_height), color='white')

        # Create draw object with new image
        draw = ImageDraw.Draw(img)

        # Calculate text position
        y_pos = (img_height - len(lines) * line_height) / 2

        # Add each line of text to the image
        for line in lines:
            text_width, text_height = draw.textsize(line, font)
            x_pos = (img_width - text_width) / 2
            draw.text((x_pos, y_pos), line, fill='black', font=font)
            y_pos += line_height

        # Save image to a byte buffer
        buffer = BytesIO()
        img.save(buffer, format='PNG')
        buffer.seek(0)

        # Create a new GeneratedImage object and save the image to it
        img_file = InMemoryUploadedFile(buffer, None, 'image.png', 'image/png', buffer.getbuffer().nbytes, None)
        generated_image = GeneratedImage(text=text, image=img_file)
        generated_image.save()

        # Render a response with the generated image
        return render(request, 'text_to_image/bake_image.html', {'generated_image': generated_image})

    else:
        return render(request, 'text_to_image/bake_image.html')