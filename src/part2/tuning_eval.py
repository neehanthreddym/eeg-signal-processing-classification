import time
import numpy as np
import pandas as pd
from mne.decoding import CSP
from typing import Any, Dict, List
from src.part2.experiment_tracking import make_config_id, compute_fold_metrics
from src.part2.model_factory import make_classifier_from_config

# Subject-level LOSO evaluation for one config
def evaluate_subject_loso_for_config(
    subject_id: str,
    epochs_subject_loso,
    config: Dict[str, Any],
    experiment_group: str,
    clf_tmin: float,
    clf_tmax: float,
) -> List[Dict[str, Any]]:
    """
    Evaluate one config for one subject using LOSO over runs.
    Returns fold-level rows.
    """
    if epochs_subject_loso.metadata is None:
        raise ValueError(f"{subject_id}: epochs_subject_loso is missing metadata.")

    required_cols = {"label_name", "run_label"}
    missing_cols = required_cols - set(epochs_subject_loso.metadata.columns)
    if missing_cols:
        raise ValueError(f"{subject_id}: missing metadata columns: {missing_cols}")

    config_id = make_config_id(config)

    epochs_clf = epochs_subject_loso.copy().crop(
        tmin=clf_tmin,
        tmax=clf_tmax,
    )

    X_all = epochs_clf.get_data()
    meta = epochs_clf.metadata.copy()

    y_all = np.where(meta["label_name"].values == "left", 0, 1)
    runs_all = meta["run_label"].values

    fold_rows: List[Dict[str, Any]] = []

    for held_out_run in sorted(pd.unique(runs_all)):
        train_mask = runs_all != held_out_run
        test_mask = runs_all == held_out_run

        X_train = X_all[train_mask]
        X_test = X_all[test_mask]
        y_train = y_all[train_mask]
        y_test = y_all[test_mask]

        fold_start = time.perf_counter()

        csp = CSP(
            n_components=int(config["n_components"]),
            reg=None,
            log=True,
            norm_trace=False,
        )
        X_train_csp = csp.fit_transform(X_train, y_train)
        X_test_csp = csp.transform(X_test)

        clf = make_classifier_from_config(config)
        clf.fit(X_train_csp, y_train)
        y_pred = clf.predict(X_test_csp)

        fit_time_sec = time.perf_counter() - fold_start
        metrics = compute_fold_metrics(y_test, y_pred)

        fold_rows.append({
            "experiment_group": experiment_group,
            "config_id": config_id,
            "model_name": config["model_name"],
            "subject_id": subject_id,
            "held_out_run": held_out_run,
            "n_components": int(config["n_components"]),
            "lda_solver": config.get("lda_solver"),
            "lda_shrinkage": config.get("lda_shrinkage"),
            "svm_kernel": config.get("svm_kernel"),
            "svm_c": config.get("svm_c"),
            "n_train_trials": int(len(y_train)),
            "n_test_trials": int(len(y_test)),
            "train_left": int((y_train == 0).sum()),
            "train_right": int((y_train == 1).sum()),
            "test_left": int((y_test == 0).sum()),
            "test_right": int((y_test == 1).sum()),
            "fit_time_sec": fit_time_sec,
            **metrics,
        })

    return fold_rows