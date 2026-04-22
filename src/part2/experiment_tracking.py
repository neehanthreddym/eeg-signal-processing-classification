import hashlib
import json
from pathlib import Path
from typing import Any, Dict, List

import numpy as np
import pandas as pd
from sklearn.metrics import accuracy_score, balanced_accuracy_score, f1_score, confusion_matrix

PROJECT_ROOT = Path(__file__).resolve().parents[2]
RESULTS_DIR = PROJECT_ROOT / "results" / "part2" / "tuning"
RESULTS_DIR.mkdir(parents=True, exist_ok=True)

def make_config_id(config: Dict[str, Any]) -> str:
    """Stable short ID for a hyperparameter config."""
    config_json = json.dumps(config, sort_keys=True, default=str)
    return hashlib.md5(config_json.encode()).hexdigest()[:10]


def append_rows_csv(path: Path, rows: List[Dict[str, Any]]) -> None:
    """Append rows to CSV, creating file if needed."""
    if not rows:
        return

    df = pd.DataFrame(rows)
    if path.exists():
        df.to_csv(path, mode="a", header=False, index=False)
    else:
        df.to_csv(path, index=False)


def compute_fold_metrics(y_true, y_pred) -> Dict[str, float]:
    """Compute standard fold-level metrics."""
    acc = accuracy_score(y_true, y_pred)
    bal_acc = balanced_accuracy_score(y_true, y_pred)
    f1_macro = f1_score(y_true, y_pred, average="macro")

    tn, fp, fn, tp = confusion_matrix(y_true, y_pred, labels=[0, 1]).ravel()

    tpr_left = tn / (tn + fp) if (tn + fp) > 0 else np.nan
    tpr_right = tp / (tp + fn) if (tp + fn) > 0 else np.nan

    return {
        "accuracy": acc,
        "balanced_accuracy": bal_acc,
        "f1_macro": f1_macro,
        "tn": tn,
        "fp": fp,
        "fn": fn,
        "tp": tp,
        "tpr_left": tpr_left,
        "tpr_right": tpr_right,
    }

def summarize_experiments(fold_df: pd.DataFrame) -> pd.DataFrame:
    """Aggregate fold-level results into one row per config."""
    grouped = fold_df.groupby(
        ["experiment_group", "config_id", "model_name",
         "n_components", "lda_solver", "lda_shrinkage",
         "svm_kernel", "svm_c"],
        dropna=False
    )

    summary_df = grouped.agg(
        n_subjects=("subject_id", "nunique"),
        n_folds=("accuracy", "count"),
        mean_accuracy=("accuracy", "mean"),
        std_accuracy=("accuracy", "std"),
        mean_balanced_accuracy=("balanced_accuracy", "mean"),
        std_balanced_accuracy=("balanced_accuracy", "std"),
        mean_f1_macro=("f1_macro", "mean"),
        std_f1_macro=("f1_macro", "std"),
        mean_tpr_left=("tpr_left", "mean"),
        mean_tpr_right=("tpr_right", "mean"),
    ).reset_index()

    return summary_df.sort_values(
        by=["model_name", "mean_balanced_accuracy", "mean_accuracy"],
        ascending=[True, False, False]
    )