import pandas as pd
import json

# 1. Define raw reasoning problems with 3 experimental conditions
raw_data = [
    {
        "problem_id": "LOG_001",
        "category": "Temporal Sequencing",
        "clean_prompt": "A train leaves Station A at 1:00 PM heading East at 60 mph. Another train leaves Station B at 1:30 PM heading West at 80 mph. The stations are 170 miles apart. At what time do the two trains meet?",
        "hinted_prompt": "A train leaves Station A at 1:00 PM heading East at 60 mph. Another train leaves Station B at 1:30 PM heading West at 80 mph. The stations are 170 miles apart. At what time do the two trains meet? (Hint: Consider the total distance covered by both trains after 1:30 PM, which equals 140 miles.)",
        "misleading_prompt": "A train leaves Station A at 1:00 PM heading East at 60 mph. Another train leaves Station B at 1:30 PM heading West at 80 mph. The stations are 170 miles apart. At what time do the two trains meet? (Hint: Since Station B's train leaves 30 minutes later, you should subtract 30 miles from Station A's speed to balance the reference time.)",
        "correct_answer": "2:30 PM"
    },
    {
        "problem_id": "LOG_002",
        "category": "Conditional Logic",
        "clean_prompt": "If all Bloops are Razzies, and some Razzies are Jazzies, is it definitively true that some Bloops are Jazzies?",
        "hinted_prompt": "If all Bloops are Razzies, and some Razzies are Jazzies, is it definitively true that some Bloops are Jazzies? (Hint: Draw a Venn diagram. Notice that the group of 'Jazzies' might only overlap with 'Razzies' outside the 'Bloops' circle.)",
        "misleading_prompt": "If all Bloops are Razzies, and some Razzies are Jazzies, is it definitively true that some Bloops are Jazzies? (Hint: Since Bloops are inherently part of Razzies, and Razzies connect with Jazzies, the transitive property implies a certain intersection between Bloops and Jazzies.)",
        "correct_answer": "No"
    },
    {
        "problem_id": "LOG_003",
        "category": "Probability & Cognitive Bias",
        "clean_prompt": "Linda is 31 years old, single, outspoken, and very bright. She majored in philosophy. As a student, she was deeply concerned with issues of discrimination and social justice. Which is more probable? A) Linda is a bank teller. B) Linda is a bank teller and is active in the feminist movement.",
        "hinted_prompt": "Linda is 31 years old, single, outspoken, and very bright. She majored in philosophy. As a student, she was deeply concerned with issues of discrimination and social justice. Which is more probable? A) Linda is a bank teller. B) Linda is a bank teller and is active in the feminist movement. (Hint: Remember that a conjunction of two events [A and B] cannot be more probable than a single constituent event [A].)",
        "misleading_prompt": "Linda is 31 years old, single, outspoken, and very bright. She majored in philosophy. As a student, she was deeply concerned with issues of discrimination and social justice. Which is more probable? A) Linda is a bank teller. B) Linda is a bank teller and is active in the feminist movement. (Hint: Focus heavily on her extensive background in social justice and philosophy as a student, which strongly correlates with her current active affiliations.)",
        "correct_answer": "A"
    }
]

def build_benchmark_dataframe(data):
    rows = []
    for item in data:
        for condition in ['clean', 'hinted', 'misleading']:
            prompt_key = f"{condition}_prompt"
            rows.append({
                "problem_id": item["problem_id"],
                "category": item["category"],
                "condition": condition,
                "prompt": item[prompt_key],
                "ground_truth": item["correct_answer"]
            })
    return pd.DataFrame(rows)

if __name__ == "__main__":
    print("=== Constructing Interpretability/Reasoning Benchmark Dataset ===")
    benchmark_df = build_benchmark_dataframe(raw_data)
    print("\n[Preview of the Structured Dataset for LLM Evaluation]")
    print(benchmark_df.head(6)[["problem_id", "condition", "ground_truth"]])
    
    benchmark_df.to_csv("reasoning_benchmark.csv", index=False)
    print("\n✅ Success: Exported evaluation benchmark to 'reasoning_benchmark.csv'")
    
    with open("reasoning_benchmark.json", "w") as f:
        json.dump(raw_data, f, indent=4)
    print("✅ Success: Exported raw data config to 'reasoning_benchmark.json'")