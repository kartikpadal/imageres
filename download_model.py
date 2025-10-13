import os
import requests
from tqdm import tqdm

# URL of the pretrained EDSR model (x3 upscaling)
MODEL_URL = "https://github.com/Saafke/EDSR_Tensorflow/raw/master/models/EDSR_x3.pb"

# where we’ll save it
MODEL_DIR = "models"
MODEL_PATH = os.path.join(MODEL_DIR, "EDSR_x3.pb")

def download_model():
    """Download the EDSR_x3.pb model if it’s not already present."""
    os.makedirs(MODEL_DIR, exist_ok=True)

    if os.path.exists(MODEL_PATH):
        print("✅ Model already exists:", MODEL_PATH)
        return

    print("⬇️  Downloading EDSR_x3.pb (super-resolution model)...")

    response = requests.get(MODEL_URL, stream=True)
    total = int(response.headers.get("content-length", 0))

    with open(MODEL_PATH, "wb") as file, tqdm(
        desc="Downloading",
        total=total,
        unit="B",
        unit_scale=True,
        unit_divisor=1024,
    ) as bar:
        for chunk in response.iter_content(chunk_size=1024):
            if chunk:
                size = file.write(chunk)
                bar.update(size)

    print("✅ Download complete:", MODEL_PATH)

if __name__ == "__main__":
    download_model()
