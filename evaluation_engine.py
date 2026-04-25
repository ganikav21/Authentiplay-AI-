from sklearn.metrics import accuracy_score, confusion_matrix, f1_score, precision_score, recall_score


def predict(similarity_score, threshold=50.0):
    return 1 if float(similarity_score) >= float(threshold) else 0


def evaluate_model(predictions, labels):
    if not labels:
        return {
            "accuracy": 0.0,
            "precision": 0.0,
            "recall": 0.0,
            "f1": 0.0,
            "confusion_matrix": [],
        }

    return {
        "accuracy": round(float(accuracy_score(labels, predictions)), 4),
        "precision": round(float(precision_score(labels, predictions, zero_division=0)), 4),
        "recall": round(float(recall_score(labels, predictions, zero_division=0)), 4),
        "f1": round(float(f1_score(labels, predictions, zero_division=0)), 4),
        "confusion_matrix": confusion_matrix(labels, predictions).tolist(),
    }
