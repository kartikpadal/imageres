from flask import Flask, render_template, request
from werkzeug.utils import secure_filename
import os
import uuid
from superres_model import enhance_image

# Flask setup
app = Flask(__name__)
UPLOAD_FOLDER = "static/uploads"
RESULT_FOLDER = "static/results"

app.config["UPLOAD_FOLDER"] = UPLOAD_FOLDER
app.config["RESULT_FOLDER"] = RESULT_FOLDER
app.config["MAX_CONTENT_LENGTH"] = 16 * 1024 * 1024  # 16 MB

# Ensure folders exist
os.makedirs(UPLOAD_FOLDER, exist_ok=True)
os.makedirs(RESULT_FOLDER, exist_ok=True)

@app.route("/")
def index():
    """Show upload page"""
    return render_template("index.html")

@app.route("/enhance", methods=["POST"])
def enhance():
    """Handle image upload and enhancement"""
    if "image" not in request.files:
        return "Error: No image uploaded", 400

    file = request.files["image"]
    if file.filename == "":
        return "Error: No selected file", 400

    # Save uploaded image with unique name
    filename = secure_filename(f"{uuid.uuid4()}_{file.filename}")
    file_path = os.path.join(app.config["UPLOAD_FOLDER"], filename)
    file.save(file_path)

    # Enhance image using model
    output_path = enhance_image(file_path)

    # Pass relative paths to template for display
    input_img_url = file_path
    output_img_url = output_path

    return render_template("result.html",
                           input_img=input_img_url,
                           output_img=output_img_url)

if __name__ == "__main__":
    app.run(debug=True)
