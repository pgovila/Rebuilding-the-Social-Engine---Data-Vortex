import joblib

# ─────────────────────────────────────────────────────────────────────────────
# 1. TEST THE UNIFIED MERGED 1-FILE BUNDLE (semantic_model_bundle.pkl)
# ─────────────────────────────────────────────────────────────────────────────
bundle_path = r"c:/Users/abc/Downloads/Unstop Competitions/Data Vortex/Round 2/semantic_model_bundle.pkl"

print("=" * 80)
print("TESTING MERGED 1-FILE BUNDLE (semantic_model_bundle.pkl):")
print("=" * 80)
try:
    bundle = joblib.load(bundle_path)
    print("SUCCESS: Merged bundle loaded cleanly!")
    print("Keys in bundle:", list(bundle.keys()))
    print("Sentiment classes:", bundle["sentiment_classes"])
    print("Topic classes:", bundle["topic_classes"])

    # Test inference directly with the bundle
    test_samples = [
        "My 2FA verification code is not working and I am locked out!",
        "The new interface update looks really nice and responsive."
    ]
    X_test = bundle["vectorizer"].transform(test_samples)
    print("\nLive Inference Test:")
    for text, sent, topic in zip(
        test_samples,
        bundle["sentiment_model"].predict(X_test),
        bundle["topic_model"].predict(X_test)
    ):
        print(f"  Post: '{text}'")
        print(f"    -> Sentiment: [{sent}] | Topic: [{topic}]")

except Exception as e:
    print(f"Failed to load bundle: {e}")

print("\n" + "=" * 80)
print("TESTING INDIVIDUAL PKL FILES:")
print("=" * 80)

# 2. Sentiment Classifier
file_path = r"c:/Users/abc/Downloads/Unstop Competitions/Data Vortex/Round 2/sentiment_classifier_model.pkl"
try:
    data = joblib.load(file_path)
    print("\n1. Sentiment Classifier loaded:")
    print(type(data))
except Exception as e:
    print(f"Joblib failed with error: {e}")

# 3. TF-IDF Vectorizer
file_path_1 = r"c:/Users/abc/Downloads/Unstop Competitions/Data Vortex/Round 2/tfidf_vectorizer.pkl"
try:
    data = joblib.load(file_path_1)
    print("\n2. TF-IDF Vectorizer loaded:")
    print(type(data))
except Exception as e:
    print(f"Joblib failed with error: {e}")

# 4. Topic Classifier
file_path_2 = r"c:/Users/abc/Downloads/Unstop Competitions/Data Vortex/Round 2/topic_classifier_model.pkl"
try:
    data = joblib.load(file_path_2)
    print("\n3. Topic Classifier loaded:")
    print(type(data))
except Exception as e:
    print(f"Joblib failed with error: {e}")

print("\n" + "=" * 80)