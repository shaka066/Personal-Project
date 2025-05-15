# src/evaluate.py
import numpy as np
import pandas as pd


def mean_average_accuracy(df_pred: pd.DataFrame, df_gt: pd.DataFrame, k=20):
    """
    簡易な mAA 計算（公式のスクリプトがあれば置き換える）
    """
    score_list = []
    for gid, sub in df_pred.groupby("scene_id"):
        gt = set(df_gt[df_gt.scene_id == gid].pair_id)
        hits = 0
        for rank, pid in enumerate(sub.pair_id.head(k), 1):
            if pid in gt:
                hits += 1 / rank
        score_list.append(hits / min(len(gt), k))
    return np.mean(score_list)


def evaluate_submission(sub_csv: str, gt_csv: str):
    sub = pd.read_csv(sub_csv)
    gt = pd.read_csv(gt_csv)
    mAA = mean_average_accuracy(sub, gt)
    # TODO: cluster score 実装
    return mAA
