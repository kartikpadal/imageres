import os
import requests
from tqdm import tqdm

# ✅ Direct model mirror (works more reliably than GitHub raw)
MODEL_URL = "https://huggingface.co/datasets/lamhoangtung/opencv-superres/resolve/main/LapSRN_x8.pb"

MODEL_DIR = "models"
MODEL_PATH = os.path.join(MODEL_DIR, "LapSRN_x8.pb")

os.makedirs(MODEL_DIR, exist_ok=True)

def download_model():
    print("⬇️ Downloading LapSRN_x8.pb (super-resolution model)...")

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
    size_mb = os.path.getsize(MODEL_PATH) / (1024 * 1024)
    print(f"📦 File size: {size_mb:.2f} MB")

if __name__ == "__main__":
    download_model()
