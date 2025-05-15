# src/features.py
from pathlib import Path
import torch
from cfg import CFG
from utils import ensure_dir

try:
    import kornia.feature as KF
except ImportError:
    raise ImportError("pip install kornia kornia-rs kornia-moons")


class FeatureExtractor:
    """SuperPoint / ALIKED / D2-Net などを簡易に切り替え"""

    def __init__(self, name="aliked", **kwargs):
        self.name = name.lower()
        if self.name == "aliked":
            self.model = KF.ALiKE.from_pretrained("outdoor").to(CFG.device).eval()
        elif self.name == "superpoint":
            self.model = KF.SuperPoint().to(CFG.device).eval()
        else:
            raise ValueError(f"unknown extractor: {self.name}")

    @torch.no_grad()
    def __call__(self, img_tensor):
        # img_tensor: (1,H,W) float32 0–1
        return self.model(img_tensor)


def extract_and_cache(image_path: Path, cache_dir: Path, extractor: FeatureExtractor):
    ensure_dir(cache_dir)
    cache_file = cache_dir / (image_path.stem + ".npz")
    if cache_file.exists():
        return cache_file
    import cv2, numpy as np

    img = cv2.imread(str(image_path), cv2.IMREAD_GRAYSCALE) / 255.0
    tensor = torch.from_numpy(img).float().unsqueeze(0).to(CFG.device)
    feats = extractor(tensor)
    np.savez_compressed(cache_file, **{k: v.cpu().numpy() for k, v in feats.items()})
    return cache_file
