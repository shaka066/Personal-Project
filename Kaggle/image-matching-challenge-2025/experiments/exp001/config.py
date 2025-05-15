# src/cfg.py
from pathlib import Path
from dataclasses import dataclass

ROOT = Path(__file__).resolve().parents[1]  # imc2025/
DATA_DIR = ROOT / "data"
RESULTS_DIR = ROOT / "results"
SRC_DIR = ROOT / "src"


@dataclass
class CFG:
    seed: int = 42
    device: str = "cuda"  # "cpu" でも可
    img_ext: str = ".png"
    train_csv: Path = DATA_DIR / "train_label.csv"
    threshold_csv: Path = DATA_DIR / "train_threshholds.csv"
    num_workers: int = 4
