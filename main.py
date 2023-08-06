from flask import Flask, render_template, request, session
from PIL import Image, ImageDraw, ImageFont
import os
import time
from datetime import datetime


app = Flask(__name__)
app.secret_key = 'your_secret_key_here'

BACKGROUND_COLOR = 'black'
chosen_image_path = None
logo_image_path = None
modified_image_path = None

time_sec = time.localtime()
current_year = time_sec.tm_year
# getting the current date and time
current_datetime = datetime.now()
# getting the time from the current date and time in the given format
current_time = current_datetime.strftime("%a %d %B")


@app.route('/favicon.ico')
def favicon():
    return app.send_static_file('images/favicon.ico')


@app.route('/')
def home():
    global chosen_image_path, logo_image_path, modified_image_path
    chosen_image_path = "static/images/medusa1.png"
    session.pop('logo_image_path', None)
    session.pop('modified_image_path', None)
    return render_template("index.html", chosen_image=chosen_image_path, logo_image=logo_image_path,
                           BACKGROUND_COLOR=BACKGROUND_COLOR, date=current_time, year=current_year)


@app.route('/choose_image', methods=['POST'])
def choose_image():
    global chosen_image_path, modified_image_path

    if 'image_file' in request.files:
        image_file = request.files['image_file']
        if image_file.filename != '':
            chosen_image_path = os.path.join('static', 'uploads', 'chosen_image.png')
            image_file.save(chosen_image_path)
            # Reset logo_image_path and modified_image_path when a new image is chosen
            session.pop('logo_image_path', None)
            session.pop('modified_image_path', None)
            print("Image file received and saved successfully:", chosen_image_path)
    else:
        print("Image file not found in request.files")

    # Check if the modified_image_path is already stored in the session
    if 'modified_image_path' in session:
        modified_image_path = session['modified_image_path']

    return render_template("index.html", chosen_image=chosen_image_path, logo_image=logo_image_path,
                           modified_image=modified_image_path, BACKGROUND_COLOR=BACKGROUND_COLOR,
                           date=current_time, year=current_year)


@app.route('/add_watermark_text', methods=['POST'])
def add_watermark_text():
    global chosen_image_path, modified_image_path

    watermark_text = request.form['watermark_text']
    if watermark_text:
        img = Image.open(chosen_image_path)
        draw = ImageDraw.Draw(img)

        # Use the custom font from the "fonts" folder
        font_path = 'static/fonts/arial.ttf'
        font_size = 33

        # Use try-except block to handle any errors related to font loading
        try:
            font = ImageFont.truetype(font_path, font_size)

            # Get the bounding box for the text
            text_bbox = draw.textbbox((0, 0), watermark_text, font=font)

            # Calculate the width and height of the text bounding box
            text_width = text_bbox[2] - text_bbox[0]
            text_height = text_bbox[3] - text_bbox[1]

            # You can calculate the position of the text based on its size and image dimensions
            x = img.width - text_width - 10
            y = img.height - text_height - 10

            # Add the watermark text in crimson color to the bottom right corner
            draw.text((x, y), watermark_text, fill='crimson', font=font)

            # Correct the path for the modified image
            modified_image_filename = generate_modified_image_filename()
            modified_image_path = os.path.join('static', 'uploads', modified_image_filename)

            img.save(modified_image_path)
            # Store modified_image_path in session for persistence
            session['modified_image'] = modified_image_filename

        except IOError:
            # Use a default font if the custom font cannot be loaded
            pass

    return render_template("index.html", chosen_image=chosen_image_path, logo_image=logo_image_path,
                           modified_image=modified_image_filename, BACKGROUND_COLOR=BACKGROUND_COLOR,
                           date=current_time, year=current_year)


def generate_modified_image_filename():
    return 'modified_image.png'  # Use a fixed filename for the modified image


@app.route('/add_watermark_logo', methods=['POST'])
def add_watermark_logo():
    global chosen_image_path, logo_image_path, modified_image_path

    if 'logo_file' in request.files:
        logo_file = request.files['logo_file']
        if logo_file.filename != '':
            logo_image_path = os.path.join('uploads', 'logo_image.png')
            logo_file.save(logo_image_path)
            # Store logo_image_path in session for persistence
            session['logo_image_path'] = logo_image_path
            # Call the function to handle the watermark logo
            handle_watermark_logo()

    # Check if the modified_image_path is already stored in the session
    if 'modified_image_path' in session:
        modified_image_path = session['modified_image_path']

    return render_template("index.html", chosen_image=chosen_image_path, logo_image=logo_image_path,
                           modified_image=modified_image_path, BACKGROUND_COLOR=BACKGROUND_COLOR,
                           date=current_time, year=current_year)


def handle_watermark_logo():
    global chosen_image_path, logo_image_path, modified_image_path

    if logo_image_path:
        img = Image.open(chosen_image_path)

        # Load the watermark logo image
        logo_img = Image.open(logo_image_path)

        # Calculate the desired size for the watermark logo (e.g., 100x100 pixels)
        desired_logo_size = (100, 100)

        # Resize the watermark logo while maintaining its aspect ratio
        logo_img.thumbnail(desired_logo_size)

        # Calculate the position for the watermark logo in the top left corner
        logo_x = 10
        logo_y = 10

        # Create a mask from the logo image's alpha channel
        logo_mask = logo_img.convert('L').point(lambda x: 255 if x > 0 else 0)

        # Paste the watermark logo on the modified image
        img.paste(logo_img, (logo_x, logo_y), logo_mask)

        # Correct the path for the modified image
        modified_image_filename = generate_modified_image_filename()
        modified_image_path = os.path.join('static', 'uploads', modified_image_filename)

        img.save(modified_image_path)
        # Store modified_image_path in session for persistence
        session['modified_image_path'] = modified_image_path


@app.route('/add_watermark_text_and_logo', methods=['POST'])
def add_watermark_text_and_logo():
    global chosen_image_path, logo_image_path, modified_image_path

    watermark_text = request.form['watermark_text']
    if watermark_text:
        # Retrieve the modified image with the logo from the session
        modified_image_path = session.get('modified_image_path')

        if modified_image_path:
            img = Image.open(modified_image_path)
            draw = ImageDraw.Draw(img)

            # Load the custom font for the watermark text
            font_path = 'static/fonts/arial.ttf'
            font_size = 33
            try:
                font = ImageFont.truetype(font_path, font_size)

                # Calculate text position and add watermark text
                text_bbox = draw.textbbox((0, 0), watermark_text, font=font)
                text_width = text_bbox[2] - text_bbox[0]
                text_height = text_bbox[3] - text_bbox[1]
                x = img.width - text_width - 10
                y = img.height - text_height - 10
                draw.text((x, y), watermark_text, fill='crimson', font=font)

            except IOError:
                # Use a default font if the custom font cannot be loaded
                pass

            # Save the modified image with watermark text
            img.save(modified_image_path)

    return render_template("index.html", chosen_image=chosen_image_path, logo_image=logo_image_path,
                           modified_image_text_and_logo=modified_image_path, BACKGROUND_COLOR=BACKGROUND_COLOR,
                           date=current_time, year=current_year)


@app.route('/save', methods=['POST'])
def save():
    global chosen_image_path, logo_image_path, modified_image_path

    # Check if the modified_image_path is already stored in the session
    if 'modified_image_path' in session:
        modified_image_path = session['modified_image_path']
        if modified_image_path:
            new_image_path = os.path.join('uploads', 'final_image.jpg')
            img = Image.open(modified_image_path)

            # Convert the image to JPEG format before saving
            img = img.convert('RGB')
            img.save(new_image_path, format='JPEG')

            # Reset modified_image_path after saving the final image
            session.pop('modified_image_path', None)

    return render_template("index.html", chosen_image=chosen_image_path, logo_image=logo_image_path,
                           modified_image_text_and_logo=modified_image_path, BACKGROUND_COLOR=BACKGROUND_COLOR,
                           date=current_time, year=current_year)


if __name__ == "__main__":
    # Get the port number from the environment variable (default to 5000 if not set)
    port = int(os.environ.get('PORT', 5000))

    # Run the Flask app on the specified port and bind to all interfaces
    app.run(debug=True, host='0.0.0.0', port=port)
