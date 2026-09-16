# Hiver AI Support Agent

A customer support agent built using Python and the free Groq API (openai/gpt-oss-20b). It works with the AmazonHelp dataset from Twitter to do three things:

1. Classify customer messages into support intents.

2. Retrieve past support answers to help draft a reply.

3. Decide if the message can be handled automatically or needs a human agent.

## Project Status

- [x] Project setup
- [x] Dataset exploration
- [x] Brand selection
- [x] Data cleaning
- [x] Conversation reconstruction
- [x] Intent taxonomy
- [x] Golden evaluation set
- [x] Majority baseline
- [x] TF-IDF baseline
- [x] Historical retrieval
- [x] LLM classification
- [x] Grounded reply generation
- [x] Escalation policy
- [x] Evaluation harness
- [x] LLM judge
- [x] Intent failure analysis
- [x] Escalation failure analysis
- [x] Week 1 scope freeze


# 1. Quick Start & Code Reproduction

Reviewers can check all results using our saved golden evaluation files (data/golden/) without running the heavy 3-million-row dataset.

### Setup Steps

Clone the repository and enter the project:

```bash
cd hiver-ai-support-agent
```

Create a virtual environment:
```bash
python -m venv .venv
```

On Windows PowerShell:
```bash
.venv\Scripts\Activate.ps1
```

Install dependencies:
```bash
pip install -r requirements.txt
```

Create a .env file and add your Groq API Key:
```bash
GROQ_API_KEY=your_groq_api_key_here
GROQ_MODEL=openai/gpt-oss-20b
```

# How to Run Evaluations

Reproducing Reply Evaluation

Run the LLM-as-a-judge evaluation:
```bash
python -m src.evaluation.run_llm_judge
```

Analyze the results:
```bash
python -m src.evaluation.analyze_llm_judgments
```

Reproducing Escalation Evaluation

Run the escalation evaluation:
```bash
python -m src.evaluation.evaluate_escalation
```

Run error analysis:
```bash
python -m src.evaluation.analyze_escalation_errors
```

Analyze escalation performance by intent:
```bash
python -m src.evaluation.analyze_escalation_by_intent
```

The evaluation scripts use the pre-generated files in data/golden/, so reviewers do not need to process the complete raw dataset to inspect the reported results.


## 2. System Architecture

The pipeline consists of four main stages:

```
Customer Message
       |
       v
Intent Classification
       |
       v
Historical Retrieval
       |
       v
Grounded Reply Generation
       |
       v
Escalation Decision
```

Intent Classification:

The LLM classifier maps each message to one of the eight AmazonHelp-specific intents.


Historical Retrieval:

Historical support examples are embedded using all-MiniLM-L6-v2 and indexed using FAISS.

The retriever returns similar historical customer/support interactions.


Reply Generation:

The retrieved historical examples are provided to the LLM as grounding context.


The generator is instructed to:

- stay grounded in historical support behavior,
- avoid inventing policies or guarantees,
- avoid claiming that an action has already been completed,
- produce a concise customer-facing response.


Escalation:

The current escalation layer is deterministic and rule-based.

It detects explicit high-risk or unresolved signals such as:

- account security problems,
- unauthorized financial activity,
- delivered-but-not-received packages,
- repeated or unresolved issues.


# 3. Problem Framing & Scope

## What "Good" Means for This Brand (AmazonHelp)
For an e-commerce support channel like AmazonHelp on Twitter, a "good" AI agent must:
- **Accurately classify intent** immediately so customers are routed correctly (e.g., distinguishing between a lost package and a tech query).
- **Maintain strict grounding** by relying purely on past human-agent responses, preventing hallucinations or unauthorized promises regarding refunds and guarantees.
- **Safely escalate** high-risk, emotional, or unresolved security issues to human agents before automated replies can cause brand damage or customer frustration.

## What We Chose Not to Build (Scope Boundaries)
To keep this focused as a robust Week 1 implementation, we explicitly chose **not** to build:
- **Full Autonomous Write Actions:** The agent drafts replies and assesses routing, but it does not execute live backend actions like issuing automated refunds, modifying orders, or resetting user credentials.
- **Multi-Turn Conversation Memory:** The current architecture evaluates and responds to single customer tweets/messages independently rather than maintaining long, complex conversational state across days.
- **Complex Real-Time Integrations:** We avoided live API integrations with third-party logistics or live database writes, relying instead on historical text retrieval via FAISS and static evaluation datasets.


## 4. Evaluation Results (Separated by Task)

A. Intent Classification Results
Tested on the 200-example golden set:
    Majority Baseline Accuracy: 31.50% (Macro-F1: 0.0599)
    TF-IDF + Logistic Regression Baseline Accuracy: 35.00% (Macro-F1: 0.1263)
    LLM Classifier Accuracy: 76.00% (Macro-F1: 0.6833)



B. Reply Quality Results (LLM Judge)
Evaluated across 96 generated replies (scored from 1 to 5):
    Relevance: 3.81 / 5
    Helpfulness: 3.76 / 5
    Groundedness: 4.96 / 5
    Safety: 5.00 / 5
    Clarity: 4.97 / 5
    Overall Judge Score: 4.50 / 5


C. Escalation Policy Results
Tested against the 200-sample golden set using our rule-based escalation policy:
    Accuracy: 64.50%
    Precision: 48.15%
    Recall: 18.57%
    F1 Score: 26.80%
    Unsafe Auto-handle Rate: 81.43%


## 5. What Is Misleading About Our Headline Numbers?
The 4.50 / 5.00 overall reply-quality score should not be interpreted as evidence that the system is production-ready.

First, the score comes from an LLM judge evaluating 96 replies rather than independent human ratings. Human agreement with the judge was therefore not measured.

Second, the current retrieval evaluation does not yet have strong near-duplicate or retrieval-leakage controls between the golden examples and the historical retrieval corpus.

Third, the overall score hides differences between dimensions. Groundedness, safety, and clarity scored highly, while relevance and helpfulness were lower.

Finally, reply quality and escalation quality measure different parts of the system. The 4.50 / 5.00 reply score does not imply that escalation decisions are equally reliable. The current escalation recall is 18.57%.

Therefore, the 4.50 / 5.00 result should be treated as an evaluation signal for the current implementation, not as a production-readiness metric.


## 6. Top 5 Failure Modes

1. Delivery Delays & Missing Items

    Example: "parcel was delivered opened and an Item was missing."

    Why it fails: Simple rules miss emotional or serious complaints about physical delivery and treat them like normal messages.

2. Account Login & Password Lockouts

    Example: "Can't sign in or reset password..."

    Why it fails: Security issues do not trigger our current rules properly.

3. Repeated Frustration

    Example: "4th time package delivered to wrong place."

    Why it fails: The system looks at single messages and cannot track how many times a customer has already complained.

4. Refund and Payment Delays

    Example: "Waiting since months for my payments..."

    Why it fails: Payment dispute words are not given enough weight in rules.

5. False Escalations on Normal Complaints

    Example: "Can you help me make an A-Z claim..."

    Why it fails: Some normal questions trigger escalation rules too early.


## 7. What I Would Do Next (With One More Week)

1. Expand escalation signals using the missed cases identified during failure analysis.
2. Add retrieval-confidence signals to escalation decisions.
3. Re-evaluate escalation precision, recall, F1, and unsafe auto-handle rate after policy changes.
4. Add more hard and boundary examples to the golden set.
5. Add near-duplicate removal and stronger evaluation-corpus separation to reduce retrieval leakage.
6. Investigate the lower relevance and helpfulness scores in generated replies.
7. Validate the LLM judge against independent human ratings.
8. Improve handling of multi-intent messages such as delivery + refund.
9. Validate and calibrate intent confidence instead of treating the LLM confidence value as a probability.


# 8. Key Architectural Decision Log 

1. AmazonHelp brand selection: Selected AmazonHelp because the dataset contains a large number of support interactions and provides clear e-commerce support categories.

2. Eight-intent taxonomy: Used a small taxonomy derived from observed AmazonHelp conversations rather than adopting a generic intent dataset.

3. Majority baseline: Added a trivial baseline to establish the minimum expected performance.

4. TF-IDF + Logistic Regression baseline: Added a simple traditional NLP baseline before evaluating the LLM classifier.

5. Groq API (openai/gpt-oss-20b): Chosen because it is fast and free for developer use.

6. LLM-as-a-Judge: Used to score responses automatically instead of manual grading.

7. Stratified Sampling for Golden Set: Collected 200 samples matching the natural intent distribution.

8. Rule-Based Escalation: Used clear rules first to see where the baseline fails.

9. Data-Driven Error Scripts: Built custom python scripts to find out why escalations failed.

10. Clean Monorepo Structure: Kept agent code (src/agent/) separate from evaluation files (src/evaluation/).

11. Environment Config: Used .env to keep API keys secure.

12. Pre-packaged Artifacts: Stored results in CSVs so reviewers don't need the 3M-row dataset.

13. CLI Error Handling: Added proper terminal checks for Windows PowerShell.


## 9. Golden Set Documentation

Sampling: 200 customer queries were picked to match real-world intent counts:

Delivery: 63
Feedback / Praise: 35
Technical: 30
Order / Product: 22
Return / Refund: 19
Account / Security: 12
Prime: 10
Payment: 9

Labelling: Evaluated using baseline models and automated checks (we did not use unverified human sheets).
