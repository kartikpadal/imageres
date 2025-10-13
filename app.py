from flask import Flask, render_template, request, url_for
from werkzeug.utils import secure_filename
import os
import uuid
from superres_model import enhance_image

app = Flask(__name__)
UPLOAD_FOLDER = "static/uploads"
RESULT_FOLDER = "static/results"

app.config["UPLOAD_FOLDER"] = UPLOAD_FOLDER
app.config["RESULT_FOLDER"] = RESULT_FOLDER
app.config["MAX_CONTENT_LENGTH"] = 16 * 1024 * 1024

os.makedirs(UPLOAD_FOLDER, exist_ok=True)
os.makedirs(RESULT_FOLDER, exist_ok=True)

@app.route("/")
def index():
    return render_template("index.html")

@app.route("/enhance", methods=["POST"])
def enhance():
    if "image" not in request.files:
        return "Error: No image uploaded", 400

    file = request.files["image"]
    if file.filename == "":
        return "Error: No selected file", 400

    # Save uploaded image
    filename = secure_filename(f"{uuid.uuid4()}_{file.filename}")
    file_path = os.path.join(app.config["UPLOAD_FOLDER"], filename)
    file.save(file_path)

    # Enhance image
    output_path = enhance_image(file_path)

    # Convert filesystem paths to URLs Flask can serve
    input_img_url = url_for("static", filename=f"uploads/{filename}")
    # Extract only the filename from output_path
    output_filename = os.path.basename(output_path)
    output_img_url = url_for("static", filename=f"results/{output_filename}")

    return render_template("result.html",
                           input_img=input_img_url,
                           output_img=output_img_url)

if __name__ == "__main__":
    app.run(debug=True)
