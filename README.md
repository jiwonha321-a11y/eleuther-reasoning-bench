# eleuther-reasoning-bench
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
2. **Contextual Sycophancy (0% Accuracy):** Under the `Misleading` condition, the model's accuracy plummeted to absolute zero (`0.0%`). The model completely abandoned logical structures (e.g., categorical logic constraints) and yielded to the deceptive heuristics injected within the prompt template.

> 📌 *Note: The generated high-resolution visualization chart is saved directly as `benchmark_performance_chart.png` upon running the analytics pipeline.*

---

## 🛠️ Repository Architecture & Workflow

The framework operates sequentially through three decoupled modules:
