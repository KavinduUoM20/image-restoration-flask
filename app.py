from flask import Flask, render_template, request, redirect, url_for
import cv2
import numpy as np
from PIL import Image
from io import BytesIO

app = Flask(__name__)

def apply_nonlinear_filter(image):
    # Apply the non-linear filter (median filter)
    filtered_image = cv2.medianBlur(image, 3)
    return filtered_image

@app.route("/", methods=["GET", "POST"])
def index():
    if request.method == "POST":
        # Check if the post request has the file part
        if 'file' not in request.files:
            return redirect(request.url)

        file = request.files['file']

        # If user does not select file, browser also submits an empty part without filename
        if file.filename == '':
            return redirect(request.url)

        # Check if the file is allowed and has the right extension
        allowed_extensions = {'png', 'jpg', 'jpeg', 'gif'}
        if file and '.' in file.filename and file.filename.rsplit('.', 1)[1].lower() in allowed_extensions:
            # Read the image
            image = Image.open(BytesIO(file.read())).convert("L")
            image_array = np.array(image)

            # Apply the non-linear filter
            filtered_image_array = apply_nonlinear_filter(image_array)

            # Convert NumPy array back to PIL image for display
            filtered_image = Image.fromarray(filtered_image_array)

            # Save the filtered image
            filtered_image_path = "static/filtered_image.png"
            filtered_image.save(filtered_image_path)

            return render_template("index.html", original_image=image, filtered_image_path=filtered_image_path)

    return render_template("index.html", original_image=None, filtered_image_path=None)

if __name__ == "__main__":
    app.run(debug=True)
