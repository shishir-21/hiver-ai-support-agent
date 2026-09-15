# Baseline Results

Evaluation protocol:

- Dataset: 200 human-labelled AmazonHelp golden examples
- Evaluation: 5-fold stratified cross-validation
- Random seed: 42
- Metric 1: Accuracy
- Metric 2: Macro-F1

## Results

| Baseline | Accuracy | Macro-F1 |
|---|---:|---:|
| Majority Class | 31.50% | 0.0599 |
| TF-IDF + Logistic Regression | 35.00% | 0.1263 |

## Interpretation

The majority-class baseline predicts `delivery_issue` for every
example.

TF-IDF + Logistic Regression performs better than the majority
baseline, showing that customer text contains useful signals for
intent classification.

However, the performance is still limited, especially across the
less frequent intents. This motivates using historical support
examples and semantic retrieval rather than relying only on lexical
features.
