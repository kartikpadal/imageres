import cv2
import os
from datetime import datetime

# Path to the pretrained model file we downloaded
MODEL_PATH = os.path.join("models", "EDSR_x3.pb")

def enhance_image(input_path, output_folder="static/results"):
    """
    Loads the EDSR super-resolution model and enhances the given image.
    Returns the path to the saved high-resolution image.
    """
    if not os.path.exists(MODEL_PATH):
        raise FileNotFoundError(f"Model not found at {MODEL_PATH}. Run download_model.py first.")
    if not os.path.exists(input_path):
        raise FileNotFoundError(f"Input image not found: {input_path}")

    # Load the image
    img = cv2.imread(input_path)
    if img is None:
        raise ValueError(f"Could not read image: {input_path}")

    # Initialize the OpenCV super-resolution model
    sr = cv2.dnn_superres.DnnSuperResImpl_create()
    sr.readModel(MODEL_PATH)
    sr.setModel("edsr", 3)  # model type + upscale factor

    # Apply super-resolution
    print("🧠 Enhancing image, please wait...")
    result = sr.upsample(img)

    # Save result image
    os.makedirs(output_folder, exist_ok=True)
    timestamp = datetime.now().strftime("%Y%m%d%H%M%S")
    output_path = os.path.join(output_folder, f"enhanced_{timestamp}.png")
    cv2.imwrite(output_path, result)
    print(f"✅ Enhanced image saved to: {output_path}")

    return output_path

# Quick test (you can run this file directly to test with a sample image)
if __name__ == "__main__":
    test_input = "static/uploads/sample.jpg"  # put a small test image here
    if os.path.exists(test_input):
        enhance_image(test_input)
    else:
        print("No test image found — upload via Flask app later.")
