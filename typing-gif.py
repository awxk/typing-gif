"""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""
Copyright (c) 2023, Nick Dilday (https://github.com/awxk)
All rights reserved.
This source code is licensed under the BSD-style license found in the
LICENSE file in the root directory of this source tree.
"""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""

from PIL import Image, ImageDraw, ImageFont
import os

# Define the parameters for the gif
background_color = (0, 0, 0, 0)  # transparent background
text_color = (255, 255, 255)  # white text
outline_color = (24, 28, 44)  # character outline color (#181c2c)
font_path = os.path.join(os.path.dirname(__file__), 'consola.ttf')
font_size = 24  # font size
text = 'class Person {\n  name: string;\n  favoriteAnime: string;\n  \n  constructor(name = "Nic", favoriteAnime = "Code Geass") {\n    this.name = name;\n    this.favoriteAnime = favoriteAnime;\n  }\n  \n  greet() {\n    console.log(`Hello, my name is ${this.name} and my favorite anime is ${this.favoriteAnime}.`);\n  }\n}\n\nconst name = prompt("What is your name?");\nconst favoriteAnime = prompt("What is your favorite anime?");\nconst person = new Person(name || undefined, favoriteAnime || undefined);\nperson.greet();\nconsole.log("Welcome to my AniList profile. Feel free to leave a message!");'

# Split the text into lines and characters
lines = text.split('\n')
characters = [list(line) for line in lines]

# Calculate the size of the image based on the text
font = ImageFont.truetype(font_path, font_size)
line_height = font.getbbox('hg')[3] - font.getbbox('hg')[1]
image_width = max(font.getsize(line)[0] for line in lines) + 10
image_height = len(lines) * line_height + 10

# Create the frames of the gif
frames = []
background = Image.new('RGBA', (image_width, image_height))
printed_lines = []  # keep track of the lines that have been printed
for line_index, line in enumerate(lines):
    # Create a new image for each line
    image = background.copy()
    draw = ImageDraw.Draw(image)

    # Draw the text and the outline up to the current character for one line at a time
    for character_index in range(len(line)):
        current_line = ''.join(characters[line_index][:character_index+1])
        current_text_size = font.getsize(current_line)
        draw.text((5, line_index * line_height + 5), current_line, font=font,
                  fill=text_color, stroke_width=1, stroke_fill=outline_color)

        # Draw the previously printed lines in this frame
        for printed_line_index, printed_line_text in printed_lines:
            printed_line = ''.join(printed_line_text)
            draw.text((5, printed_line_index * line_height + 5), printed_line,
                      font=font, fill=text_color, stroke_width=1, stroke_fill=outline_color)

        # Add the image to the frames list
        frames.append(image.copy())

    # Add the current line to the printed lines list
    printed_lines.append((line_index, characters[line_index]))

# Add blank frames to the end to keep the text on screen
for i in range(50):
    frames.append(frames[-1])

# Save the frames as a gif
frames[0].save('typing.gif', format='GIF', save_all=True,
               append_images=frames[1:], duration=50, loop=0, transparency=0)
