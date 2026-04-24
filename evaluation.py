import json
from sklearn.metrics import accuracy_score, precision_score, recall_score, confusion_matrix

# import your pipeline
from step3_safe_fingerprint import run_pipeline   # adjust if needed

THRESHOLD = 0.7

with open("dataset.json", "r") as f:
    dataset = json.load(f)

predictions = []
labels = []

for pair in dataset:
    video_a = pair["video_a"]
    video_b = pair["video_b"]
    label = pair["label"]

    score = run_pipeline(video_a, video_b)

    pred = 1 if score > THRESHOLD else 0

    print(f"\nComparing:")
    print(f"A: {video_a}")
    print(f"B: {video_b}")
    print(f"Score: {score:.2f} → Prediction: {pred} | Actual: {label}")

    predictions.append(pred)
    labels.append(label)

# Metrics
accuracy = accuracy_score(labels, predictions)
precision = precision_score(labels, predictions, zero_division=0)
recall = recall_score(labels, predictions, zero_division=0)
cm = confusion_matrix(labels, predictions)

print("\n📊 RESULTS:")
print(f"Accuracy: {accuracy:.2f}")
print(f"Precision: {precision:.2f}")
print(f"Recall: {recall:.2f}")
print(f"Confusion Matrix:\n{cm}")