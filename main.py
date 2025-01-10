import os
from flask import Flask, render_template, request, flash, redirect, url_for
from PIL import Image
from collections import Counter
import webcolors


UPLOAD_FOLDER = 'static/uploads'
ALLOWED_EXTENSIONS = ['png', 'jpg', 'jpeg', 'gif']

app = Flask(__name__)
app.config['UPLOAD_FOLDER'] = UPLOAD_FOLDER
app.secret_key = 'your_secret_key'


def color_codes(image_path):
    img = Image.open(image_path).convert("RGB")
    img = img.resize((100, 100))
    pixels = list(img.getdata())
    color_count = Counter(pixels)
    top_colors = color_count.most_common(10)
    hex_colors = [(color, webcolors.rgb_to_hex(color))for color, _ in top_colors]
    return hex_colors


@app.route("/")
def home():
    return render_template('index.html')


@app.route("/photo", methods=["POST", "GET"])
def upload_photo():
    if request.method == "POST":
        try:
            img = request.files["photo"]
            path = os.path.join(app.config['UPLOAD_FOLDER'], img.filename)
            img.save(path)

            top_colors = color_codes(img)

            return render_template('upload.html', photo_filename=img.filename, top_colors=top_colors)
        except FileNotFoundError:
            flash("Please select a file", "error")
            return redirect(url_for('home'))


if __name__ == "__main__":
    app.run(debug=True)
