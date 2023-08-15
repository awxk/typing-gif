from PIL import Image, ImageDraw, ImageFont

# Define the parameters for the gif
background_color = (0, 0, 0, 0)  # transparent background
font_path = "consola.ttf"
font_size = 24
text_color = "#9FADBD"
outline_color = "#0B1622"
padding = 10  # Adjust the padding as needed

text = """
class Person {
    username: string;
    favoriteAnime: string;
    
    constructor(username = "user") {
        this.username = username;
        this.favoriteAnime = Math.random() < 0.5 ? "Code Geass" : "To Your Eternity";
    }
    greet() {
        console.log(`Hello, my name is ${this.username} and my favorite anime is ${this.favoriteAnime}.`);
    }
}
const username = prompt("What is your name?");
const person = new Person(username || undefined);
person.greet();
console.log("Welcome to my AniList profile. Feel free to leave a message.");
"""

# Split the text into lines and characters
lines = text.split('\n')
characters = [list(line) for line in lines]

# Calculate the size of the image based on the text
font = ImageFont.truetype(font_path, font_size)
line_height = font.getbbox('hg')[3] - font.getbbox('hg')[1]
image_width = max(font.getsize(line)[0] for line in lines) + 2 * padding
image_height = len(lines) * line_height + 2 * padding

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
        draw.text((padding, padding + line_index * line_height), current_line, font=font,
                  fill=text_color, stroke_width=1, stroke_fill=outline_color)

        # Draw the previously printed lines in this frame
        for printed_line_index, printed_line_text in printed_lines:
            printed_line = ''.join(printed_line_text)
            draw.text((padding, padding + printed_line_index * line_height), printed_line,
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
               append_images=frames[1:], duration=25, loop=0, transparency=0)
