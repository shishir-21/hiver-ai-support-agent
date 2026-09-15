import joblib
import pandas as pd

from sklearn.feature_extraction.text import TfidfVectorizer
from sklearn.linear_model import LogisticRegression


GOLDEN_FILE = "data/golden/amazon_golden_200_annotated.csv"
MODEL_FILE = "data/processed/intent_classifier.joblib"


class IntentClassifier:

    def __init__(self):
        self.vectorizer = TfidfVectorizer(
            ngram_range=(1, 2),
            min_df=2,
            max_features=10000,
            sublinear_tf=True,
        )

        self.model = LogisticRegression(
            max_iter=1000,
            random_state=42,
        )

    def train(self):
        df = pd.read_csv(GOLDEN_FILE)

        X = df["customer_text"].fillna("")
        y = df["intent"]

        X_tfidf = self.vectorizer.fit_transform(X)

        self.model.fit(X_tfidf, y)

    def predict(self, text):
        X = self.vectorizer.transform([text])

        intent = self.model.predict(X)[0]

        probabilities = self.model.predict_proba(X)[0]

        confidence = float(probabilities.max())

        return intent, confidence

    def save(self):
        joblib.dump(
            {
                "vectorizer": self.vectorizer,
                "model": self.model,
            },
            MODEL_FILE,
        )

    def load(self):
        data = joblib.load(MODEL_FILE)

        self.vectorizer = data["vectorizer"]
        self.model = data["model"]
        