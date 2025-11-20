import os
import json
from datasets import load_dataset
from lcb_runner.runner import custom_evaluator

# Step 1: Load dataset
dataset = load_dataset(
    "livecodebench/code_generation_lite", 
    version_tag="release_v2", 
    split="test", 
    trust_remote_code=True
)
problems = dataset

model = "gpt4o"

# Helper to extract function definition
def extract_function_definition(code_str):
    lines = code_str.splitlines()
    func_lines = []
    recording = False
    indent_level = None
    for line in lines:
        if not recording and line.strip().startswith("def "):
            recording = True
            indent_level = len(line) - len(line.lstrip(' '))
            func_lines.append(line)
            continue
        if recording:
            if line.strip() == "":
                # keep blank lines in function body
                func_lines.append(line)
                continue
            current_indent = len(line) - len(line.lstrip(' '))
            if indent_level is not None and current_indent > indent_level:
                func_lines.append(line)
                continue
            else:
                break
    return "\n".join(func_lines)

# Step 2: Extract functions from solution files
extracted_records = []
for problem in problems:
    qid = problem["question_id"]
    sol_file = os.path.join(model, "livecodebench", qid, "solution.py")
    if not os.path.isfile(sol_file):
        continue
    with open(sol_file, "r", encoding="utf-8") as f:
        code = f.read()
    func_def = extract_function_definition(code)
    extracted_records.append({"question_id": qid, "code_list": [func_def]})

# Step 3: Save extracted solutions in JSONL format
output_path = "extracted_solutions.jsonl"
with open(output_path, "w", encoding="utf-8") as out_f:
    for record in extracted_records:
        json.dump(record, out_f)
        out_f.write("\n")

# Step 4: Evaluate to compute pass@1
results = custom_evaluator.evaluate_json(output_path, scenario="codegeneration", version_tag="release_v2")

# Step 5: Compute and print pass@1 score
pass1_values = [res.get("pass@1", 0) for res in results]
pass1_score = sum(pass1_values) / len(pass1_values) if pass1_values else 0.0
print(f"Final Pass@1: {pass1_score:.3f}")
