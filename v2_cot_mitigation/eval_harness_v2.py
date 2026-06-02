import pandas as pd
import torch
from transformers import AutoTokenizer, AutoModelForCausalLM
import os
import re

def run_advanced_evaluation():
    """
    [Project 3] Executes localized CPU inference loop using Qwen2.5-1.5B-Instruct.
    This v2 harness processes the advanced matrix containing CoT defense layers
    and outputs evaluation tracking to a distinct v2 artifact.
    """
    print("🚀 [Project 3] Initializing v2 Localized Inference Loop (CoT Validation)...")
    
    # 1. Enforce strict local directory paths to isolate v2 artifacts
    matrix_path = "v2_cot_mitigation/logical_evaluation_matrix_v2.csv"
    output_path = "v2_cot_mitigation/eval_results_qwen_v2.csv"
    
    # Fallback to current directory if execution happens inside the v2 folder locally
    if not os.path.exists(matrix_path):
        matrix_path = "logical_evaluation_matrix_v2.csv"
        output_path = "eval_results_qwen_v2.csv"
        
    if not os.path.exists(matrix_path):
        print(f"❌ Error: Baseline matrix target '{matrix_path}' not found.")
        return

    df = pd.read_csv(matrix_path)
    
    # 2. Safely initialize model and tokenizer via Hugging Face cache
    model_name = "Qwen/Qwen2.5-1.5B-Instruct"
    print(f"📦 Loading weights and tokenizer for {model_name} onto local CPU memory...")
    
    try:
        tokenizer = AutoTokenizer.from_pretrained(model_name)
        model = AutoModelForCausalLM.from_pretrained(
            model_name,
            torch_dtype="auto",
            device_map="cpu"  # Enforced CPU routine to bypass WinError 1114 DLL conflicts
        )
    except Exception as e:
        print(f"❌ Framework initialization failed: {str(e)}")
        return

    generated_outputs = []
    
    print("\n⚡ Starting greedy decoding sequence across the 3x4 configuration matrix...")
    # 3. Execution loop over the matrix rows
    for idx, row in df.iterrows():
        print(f" -> Processing Task: {row['problem_id']} | Condition: {row['condition']}...")
        
        # Apply standard system instruction format for open-weight instruction models
        messages = [
            {"role": "system", "content": "You are a precise, objective logical reasoning assistant."},
            {"role": "user", "content": row['prompt']}
        ]
        text = tokenizer.apply_chat_template(messages, tokenize=False, add_generation_prompt=True)
        
        model_inputs = tokenizer([text], return_tensors="pt")
        
        # Greedy decoding parameters configuration (temperature=0.0 for deterministic tracking)
        with torch.no_grad():
            generated_ids = model.generate(
                **model_inputs,
                max_new_tokens=512,
                temperature=0.0,
                do_sample=False
            )
            
        # Extract generated tokens safely
        generated_ids = [
            output_ids[len(input_ids):] for input_ids, output_ids in zip(model_inputs.input_ids, generated_ids)
        ]
        response = tokenizer.batch_decode(generated_ids, skip_special_tokens=True)[0]
        generated_outputs.append(response)

    # 4. Bind outputs and write serialized execution results
    df['model_output'] = generated_outputs
    df.to_csv(output_path, index=False, encoding="utf-8")
    print(f"\n✅ Inference loop successfully terminated. Results cached at '{output_path}'.")

if __name__ == "__main__":
    run_advanced_evaluation()
