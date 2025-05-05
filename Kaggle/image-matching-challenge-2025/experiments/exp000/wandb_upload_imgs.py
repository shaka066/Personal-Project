import os
import glob
import wandb


def main():
    # W&B 実験初期化
    exp_name = "image_matching_table"
    wandb.init(project="image-matching-challenge", name=exp_name)

    # 学習用画像フォルダパス
    DATA_DIR = "./data/train"

    # テーブル定義
    table = wandb.Table(columns=["dataset", "scene", "image_filename", "image"])

    # ディレクトリごとに画像を収集しテーブルに追加
    for dataset in os.listdir(DATA_DIR):
        ds_path = os.path.join(DATA_DIR, dataset)
        if not os.path.isdir(ds_path):
            continue
        for img_path in glob.glob(os.path.join(ds_path, "*.png")):
            try:
                image_filename = os.path.basename(img_path)
                scene = image_filename.split("_")[0]
                # 画像が破損している場合はスキップ
                img = wandb.Image(img_path)
                table.add_data(dataset, scene, image_filename, img)
            except Exception as e:
                print(f"Warning: Skipping corrupted image {img_path}: {e}")
                continue

    # W&B にテーブルをログ
    wandb.log({"train_image_table": table})


if __name__ == "__main__":
    main()
