Markdown
# Evaluation of LLM Reasoning Robustness Under Contextual Interventions

This repository contains an automated evaluation harness designed to stress-test the logical reasoning capabilities of Large Language Models (LLMs) when subjected to biased contextual prompts. 

By systematically injecting correct hints versus misleading premises, this framework quantifies the extent to which open-weight language models rely on structural logic versus superficial contextual alignment (sycophancy).

---

## 📊 Experimental Results & Statistical Insights

Using **Qwen2.5-1.5B-Instruct** as the primary local evaluation target via a localized CPU harness, the model demonstrated a severe vulnerability to misleading interventions.

| Experimental Condition | Sample Size | Raw Accuracy | Accuracy Rate (%) |
| :--- | :---: | :---: | :---: |
| **Clean (Control)** | 3 | 1 / 3 | **33.3%** |
| **Hinted (Positive Bias)** | 3 | 1 / 3 | **33.3%** |
| **Misleading (Negative Bias)** | 3 | 0 / 3 | **0.0%** |

### Key Takeaways
1. **Baseline Fragility:** The baseline logical accuracy of the light-weight model sits at `33.3%`, proving that complex syllogisms and probability tasks remain a steep barrier for smaller scale architectures without scale expansion.
2. **Contextual Sycophancy (0% Accuracy):** Under the `Misleading` condition, the model's accuracy plummeted to absolute zero (`0.0%`). The model completely abandoned logical structures and yielded to the deceptive heuristics injected within the prompt template.

> 📌 *Note: The generated high-resolution visualization chart is saved directly as `benchmark_performance_chart.png` upon running the analytics pipeline.*

---

## 🛠️ Repository Architecture & Workflow

The framework operates sequentially through three decoupled modules:

📦 eleuther-reasoning-bench
```text
├── 1️⃣ benchmark_builder.py     # Synthesizes the 3x3 logical evaluation matrix (CSV)
├── 2️⃣ eval_harness.py          # Localized CPU inference loop executing Qwen2.5-1.5B
└── 3️⃣ visualize_results.py     # Programmatic scoring and academic-grade plot generation
```
---

## 🧠 Core Module Mechanics
### 1. Data Synthesis (benchmark_builder.py)
Generates a deterministic dataset across three core reasoning dimensions:

LOG_001: Relative motion math calculation.

LOG_002: Syllogistic categorical deduction fallacy.

LOG_003: Conjunction fallacy (The Linda Problem).

Each domain is duplicated into three operational prompt templates (clean, hinted, misleading) to evaluate how the integration of external contextual anchors shifts the model's inner token prediction distribution.

### 2. Execution Harness (eval_harness.py)
Loads tokenizers and model weights via transformers directly into local memory. Bypasses standard Windows DLL execution errors (WinError 1114) and API rate limits by enforcing a localized CPU execution routine with greedy decoding (temperature=0.0).

### 3. Quantitative Analysis (visualize_results.py)
Applies a rule-based deterministic scoring regex to evaluate model responses against strict logical verification boundaries, compiling statistics and leveraging seaborn to output performance trends.

---

## 🚀 How to Replicate
Ensure you have a clean Python environment, then install the absolute minimum dependencies:
#### Bash
```text
pip install pandas torch transformers matplotlib seaborn
```

Run the pipeline sequentially from your terminal:

### Step 1: Synthesize the benchmarks
#### Bash
python benchmark_builder.py

### Step 2: Run the automated local evaluation loop
#### Bash
python eval_harness.py

### Step 3: Grade the outputs and generate the analytical charts
#### Bash
python visualize_results.py
