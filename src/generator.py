import os, uuid
import numpy as np
from PIL import Image, ImageDraw

class SurgicalPhantomGenerator:
    def __init__(self, output_dir="data/raw"):
        self.output_dir = output_dir
        os.makedirs(self.output_dir, exist_ok=True)

    def _apply_noise(self, arr: np.ndarray, noise_sigma: float) -> np.ndarray:
        noise = np.random.normal(0, noise_sigma, arr.shape)
        out = arr.astype(float) + noise
        return np.clip(out, 0, 255).astype(np.uint8)

    def generate_hip_ap(self, pelvic_tilt_deg: float) -> np.ndarray:
        W, H = 512, 512
        img = Image.new("L", (W, H), color=30)
        draw = ImageDraw.Draw(img)
        cx, cy = W // 2, H // 2

        tilt_factor = np.cos(np.radians(pelvic_tilt_deg))
        brim_h = int(120 * tilt_factor)

        draw.arc([cx-150, cy-100, cx+150, cy-100+brim_h], start=0, end=180, fill=200, width=15)
        draw.ellipse([cx-130, cy+60, cx-90, cy+100], fill=240)
        draw.ellipse([cx+90, cy+60, cx+130, cy+100], fill=240)

        return np.array(img)

    def create_one(self, noise_sigma: float = 15.0) -> dict:
        pelvic_tilt = float(np.round(np.random.normal(12, 5), 2))
        image_id = str(uuid.uuid4())
        filename = f"{image_id}.png"
        path = os.path.join(self.output_dir, filename)

        base = self.generate_hip_ap(pelvic_tilt)
        final = self._apply_noise(base, noise_sigma=noise_sigma)
        Image.fromarray(final).save(path)

        return {
            "image_id": image_id,
            "anatomy": "Hip",
            "view_type": "AP",
            "pelvic_tilt": pelvic_tilt,
            "noise_sigma": noise_sigma,
            "local_path": path,
            "filename": filename,
        }

