import cv2
import os
import uuid

# Use your downloaded model
MODEL_PATH = os.path.join("models", "EDSR_x4.pb")

def enhance_image(input_path, output_folder="static/results"):
    if not os.path.exists(MODEL_PATH):
        raise FileNotFoundError(f"Model not found at {MODEL_PATH}. Place the EDSR_x4.pb file there.")
    if not os.path.exists(input_path):
        raise FileNotFoundError(f"Input image not found: {input_path}")

    # Load image
    img = cv2.imread(input_path)
    if img is None:
        raise ValueError(f"Could not read image: {input_path}")

    # Initialize super-resolution model
    sr = cv2.dnn_superres.DnnSuperResImpl_create()
    sr.readModel(MODEL_PATH)
    sr.setModel("edsr", 4)  # EDSR x4

    # Enhance
    print("Enhancing image...")
    result = sr.upsample(img)
    if result is None:
        raise ValueError("Upsample failed. Make sure opencv-contrib-python is installed.")

    # Save result
    os.makedirs(output_folder, exist_ok=True)
    output_path = os.path.join(output_folder, f"enhanced_{uuid.uuid4().hex}.png")
    cv2.imwrite(output_path, result)
    print(f"Enhanced image saved to: {output_path}")

    return output_path

# Optional quick test
if __name__ == "__main__":
    test_image = "static/uploads/sample.jpg"
    if os.path.exists(test_image):
        enhance_image(test_image)
    else:
        print("Place a sample image at static/uploads/sample.jpg")
