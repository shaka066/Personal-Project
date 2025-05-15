# src/dataset.py
from pathlib import Path
import pandas as pd
from torch.utils.data import Dataset
from cfg import CFG


class SceneDataset(Dataset):
    """
    単一 Scene 内の画像ペア or Triplet を返す軽量 Dataset
    """

    def __init__(self, scene_dir: Path, pairs_df: pd.DataFrame, transform=None):
        self.scene_dir = scene_dir
        self.pairs_df = pairs_df
        self.transform = transform

    def __len__(self):
        return len(self.pairs_df)

    def __getitem__(self, idx):
        row = self.pairs_df.iloc[idx]
        img1_path = self.scene_dir / row.img1
        img2_path = self.scene_dir / row.img2

        # Pillow → Tensor
        import torchvision.transforms as T

        to_tensor = T.ToTensor()
        img1 = to_tensor(
            T.functional.pil_to_tensor(
                T.functional.pil_to_tensor(open_image(img1_path))
            )
        )
        img2 = to_tensor(
            T.functional.pil_to_tensor(
                T.functional.pil_to_tensor(open_image(img2_path))
            )
        )

        if self.transform:
            img1, img2 = self.transform(img1, img2)

        return dict(img1=img1, img2=img2, id_pair=(row.img1, row.img2))


def build_pairs_csv(scene_id: str):
    """
    シーンごとのペアを作成（最初はダミー。公式 pairs があれば置き換え）
    """
    # TODO: epipolar/overlap 情報がある場合はフィルタリング
    pass
