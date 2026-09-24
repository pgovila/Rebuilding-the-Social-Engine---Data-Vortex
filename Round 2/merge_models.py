"""
Script to bundle the 3 individual .pkl artifacts into 1 single .pkl file
for streamlined submission.

Bundles:
  - tfidf_vectorizer.pkl
  - sentiment_classifier_model.pkl
  - topic_classifier_model.pkl

Output:
  - semantic_model_bundle.pkl
"""
from pathlib import Path
import joblib

def merge_pkl_files(
    vectorizer_path="tfidf_vectorizer.pkl",
    sentiment_model_path="sentiment_classifier_model.pkl",
    topic_model_path="topic_classifier_model.pkl",
    output_bundle_path="semantic_model_bundle.pkl"
):
    print("Loading individual artifacts...")
    vectorizer = joblib.load(vectorizer_path)
    sentiment_model = joblib.load(sentiment_model_path)
    topic_model = joblib.load(topic_model_path)

    bundle = {
        "vectorizer": vectorizer,
        "sentiment_model": sentiment_model,
        "topic_model": topic_model,
        "sentiment_classes": list(sentiment_model.classes_),
        "topic_classes": list(topic_model.classes_),
        "metadata": {
            "competition": "Data Vortex Round 2 - Aaruush '26",
            "task": "Rebuilding the Semantic Understanding Layer",
            "sentiment_classes": list(sentiment_model.classes_),
            "topic_classes": list(topic_model.classes_),
            "serialization": "joblib (compress=3)",
        }
    }

    target = Path(output_bundle_path)
    joblib.dump(bundle, target, compress=3)
    file_size_mb = target.stat().st_size / (1024 * 1024)
    print(f"\n[SUCCESS] Bundled 3 artifacts into: {target.resolve()}")
    print(f"File size: {target.stat().st_size:,} bytes (~{file_size_mb:.2f} MB)")
    print("Keys available in bundle:", list(bundle.keys()))

    # Verification
    loaded = joblib.load(target)
    assert "vectorizer" in loaded
    assert "sentiment_model" in loaded
    assert "topic_model" in loaded
    print("Verification assertion passed: Bundle reloaded and validated cleanly!")

if __name__ == "__main__":
    merge_pkl_files()
