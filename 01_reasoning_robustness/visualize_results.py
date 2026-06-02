import pandas as pd
import matplotlib.pyplot as plt
import seaborn as sns
import os

def score_response(row):
    """
    A lightweight, rule-based scoring harness tailored for the logical benchmark.
    Checks if the model succumbed to the reasoning shortcuts or remained robust.
    """
    output = str(row['model_output']).lower()
    prob_id = row['problem_id']
    condition = row['condition']
    
    # LOG_001: Train Meeting Time (Correct Answer: 2:30 PM / 1.5 hours)
    if prob_id == "LOG_001":
        if "2:30" in output or "1.5 hour" in output or "1 hour and 30" in output:
            return 1
        return 0
        
    # LOG_002: Syllogism (Correct Answer: Cannot be determined / False)
    elif prob_id == "LOG_002":
        if "yes" in output or "definitively true" in output:
            return 0  # Fell for the fallacy
        if "cannot be determined" in output or "not necessarily" in output or "false" in output:
            return 1
        return 0
        
    # LOG_003: Conjunction Fallacy / Linda Problem (Correct Answer: Less probable / Scenario A)
    elif prob_id == "LOG_003":
        if "bank teller and is active" in output or "more probable" in output:
            if condition == "misleading":
                return 0 # Fell for the bias
        return 1
        
    return 0

if __name__ == "__main__":
    print("=== Launching Automated Analytics & Visualization Pipeline ===")
    
    input_csv = "eval_results_qwen.csv"
    output_img = "benchmark_performance_chart.png"
    
    if not os.path.exists(input_csv):
        print(f"❌ Error: '{input_csv}' not found. Please run the evaluation harness first.")
        exit()
        
    # Load dataset
    df = pd.read_csv(input_csv)
    
    # Apply grading logic
    print("📝 Grading LLM responses based on experimental constraints...")
    df['is_correct'] = df.apply(score_response, axis=1)
    
    # Calculate performance metrics grouped by experimental conditions
    summary = df.groupby('condition')['is_correct'].mean().reset_index()
    summary['accuracy_pct'] = summary['is_correct'] * 100
    
    print("\n📊 Statistical Summary Table:")
    print(summary.to_string(index=False))
    
    # Generate Academic-grade Visualization Chart
    print(f"\n🎨 Generating performance graph -> {output_img}")
    sns.set_theme(style="whitegrid")
    plt.figure(figsize=(8, 5))
    
    # Order conditions for meaningful comparison
    condition_order = ['clean', 'hinted', 'misleading']
    
    ax = sns.barplot(
        x='condition', 
        y='accuracy_pct', 
        data=summary, 
        order=condition_order,
        palette=['#2b5c8f', '#4682b4', '#b22222'] # Blue for base, Red for misleading drop
    )
    
    # Style annotations
    plt.title("LLM Reasoning Robustness Across Prompt Interventions", fontsize=14, fontweight='bold', pad=15)
    plt.xlabel("Experimental Condition", fontsize=12, fontweight='bold', labelpad=10)
    plt.ylabel("Accuracy Rate (%)", fontsize=12, fontweight='bold', labelpad=10)
    plt.ylim(0, 110)
    
    # Add percentage labels on top of bars
    for p in ax.patches:
        ax.annotate(f"{p.get_height():.1f}%", 
                    (p.get_x() + p.get_width() / 2., p.get_height() + 2), 
                    ha='center', va='center', 
                    fontsize=11, fontweight='bold', color='black',
                    xytext=(0, 5), textcoords='offset points')
                    
    plt.tight_layout()
    plt.savefig(output_img, dpi=300)
    plt.close()
    
    print("==================================================")
    print(f"✅ Success: Analytics complete. Graph saved as '{output_img}'")
    print("==================================================")