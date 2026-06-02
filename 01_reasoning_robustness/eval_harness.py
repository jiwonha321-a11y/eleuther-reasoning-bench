import pandas as pd
import time
import os
from openai import OpenAI

# ==========================================
# ⚙️ CONFIGURATION & AUTHENTICATION (NO TORCH)
# ==========================================
# ⚠️ Security Fix: Never hardcode your active API tokens in public repositories.
HF_TOKEN = "YOUR_HUGGINGFACE_TOKEN_HERE"

# We use Qwen2.5-7B-Instruct hosted on Hugging Face Serverless Architecture
# Fully compliant with OpenAI API integration standards
client = OpenAI(
    base_url="https://api-inference.huggingface.co/v1/",
    api_key=HF_TOKEN
)

MODEL_ID = "Qwen/Qwen2.5-7B-Instruct"

def query_serverless_llm(prompt_text):
    """
    Queries the high-performance open-weight model via serverless infrastructure.
    Completely eliminates PyTorch DLL dependency and local memory limits.
    """
    try:
        response = client.chat.completions.create(
            model=MODEL_ID,
            messages=[
                {"role": "user", "content": prompt_text}
            ],
            max_tokens=150,
            temperature=0.0, # Strict deterministic control
            stream=False
        )
        return response.choices[0].message.content.strip()
    except Exception as e:
        error_msg = str(e)
        # Catch cold-start model loading triggers gently
        if "currently loading" in error_msg or "503" in error_msg:
            print("   [Notice] Model is initializing on server. Retrying in 20s...")
            time.sleep(20)
            try:
                # Secondary attempt after server warm-up
                second_response = client.chat.completions.create(
                    model=MODEL_ID,
                    messages=[{"role": "user", "content": prompt_text}],
                    max_tokens=150,
                    temperature=0.0
                )
                return second_response.choices[0].message.content.strip()
            except:
                return "ERROR_SERVER_TIMEOUT"
        else:
            return f"ERROR_API_CALL_FAILED: {error_msg[:40]}"

if __name__ == "__main__":
    print("=== Launching PyTorch-Free Serverless Evaluation Harness ===")
    
    input_csv = "reasoning_benchmark.csv"
    output_csv = "eval_results_qwen_server.csv"
    
    if not os.path.exists(input_csv):
        print(f"❌ Error: '{input_csv}' not found. Please run benchmark_builder.py first.")
        exit()
        
    # Load the benchmark data generated in Project 1
    df = pd.read_csv(input_csv)
    print(f"📊 Loaded {len(df)} evaluation prompts from benchmark sample.")
    
    model_outputs = []
    
    # Sequential benchmarking pipeline
    for idx, row in df.iterrows():
        print(f"\n🚀 Running [{idx + 1}/{len(df)}] ID: {row['problem_id']} | Condition: {row['condition']}")
        print(f"   Prompt Snippet: {row['prompt'][:60]}...")
        
        # Execute API payload
        raw_response = query_serverless_llm(row['prompt'])
        print(f"   🤖 Model Response: {raw_response[:80].replace('\n', ' ')}...")
        
        model_outputs.append(raw_response)
        time.sleep(0.8) # Polite API pacing
        
    # Append results and export to CSV
    df["model_output"] = model_outputs
    df.to_csv(output_csv, index=False)
    
    print("\n==================================================")
    print(f"✅ Success: Evaluation complete. Results exported to '{output_csv}'")
    print("==================================================")