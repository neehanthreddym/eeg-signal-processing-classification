from sklearn.discriminant_analysis import LinearDiscriminantAnalysis
from sklearn.svm import SVC
from typing import Any, Dict

# Classifier builder from config
def make_classifier_from_config(config: Dict[str, Any]):
    """Create classifier from one config dictionary."""
    model_name = config["model_name"].lower()

    if model_name == "lda":
        solver = config["lda_solver"]
        shrinkage = config["lda_shrinkage"]

        if solver == "svd":
            return LinearDiscriminantAnalysis(solver="svd")

        return LinearDiscriminantAnalysis(
            solver=solver,
            shrinkage=shrinkage,
        )

    if model_name == "svm":
        return SVC(
            kernel=config["svm_kernel"],
            C=float(config["svm_c"]),
        )

    raise ValueError(f"Unsupported model_name: {config['model_name']}")