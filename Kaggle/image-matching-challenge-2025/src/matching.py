# src/matching.py
import torch
from cfg import CFG

try:
    import lightglue
    from lightglue import LightGlue, SuperPoint, ALIKED
except ImportError:
    raise ImportError("pip install lightglue")


class Matcher:
    def __init__(self, extractor="aliked"):
        if extractor == "superpoint":
            self.backbone = SuperPoint(pretrained="outdoor").eval().to(CFG.device)
        else:
            self.backbone = ALIKED(pretrained="outdoor").eval().to(CFG.device)
        self.matcher = LightGlue(features="aliked").to(CFG.device).eval()

    @torch.no_grad()
    def match(self, img0, img1):
        feat0 = self.backbone.extract(img0)
        feat1 = self.backbone.extract(img1)
        matches = self.matcher({"image0": feat0, "image1": feat1})
        return matches["matches0"], matches["matches1"], matches["scores"]
