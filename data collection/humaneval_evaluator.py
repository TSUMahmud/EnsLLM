import os
import re
import json
import ast
from typing import List, Dict
from human_eval.data import read_problems
from human_eval.evaluation import evaluate_functional_correctness


def extract_code(text: str) -> List[str]:
    pattern = r"```python(.*?)```"
    matches = re.findall(pattern, text, re.DOTALL)
    
    return [match.strip() for match in matches] if matches else [text.strip()]


def extract_function_code(full_code: str) -> str:
    tree = ast.parse(full_code)
    for node in ast.walk(tree):
        if isinstance(node, ast.FunctionDef):
            return ast.unparse(node)  # Extract only the function definition
    raise ValueError("No function definition found in the provided code.")


def save_solutions_to_jsonl(solutions: List[Dict[str, str]], file_path: str) -> None:
    with open(file_path, "w") as f:
        for entry in solutions:
            f.write(json.dumps(entry) + "\n")


# Read all HumanEval problems
problems = read_problems()
solutions = []

# Iterate over each problem in HumanEval
for problem_id, problem_data in problems.items():
    prompt = problem_data["prompt"]
    entry_point = problem_data["entry_point"]
    print(f"Processing: {problem_id} - {entry_point}")

    # Retrieve solution code stored in HumanEval/id/{problem_id}.py
    solution_path = f"HumanEval/id/{problem_id}.py"
    
    if os.path.exists(solution_path):
        with open(solution_path, "r", encoding="utf-8") as f:
            full_code = f.read()
        
        # Extract only the function definition
        function_code = extract_function_code(full_code)
        
        # Store extracted function for evaluation
        solutions.append({"task_id": problem_id, "completion": function_code})
    else:
        print(f"Solution file for {problem_id} not found!")

# Save all solutions to a JSONL file
jsonl_path = "model_solutions.jsonl"
save_solutions_to_jsonl(solutions, jsonl_path)

# Evaluate solutions using HumanEval
results = evaluate_functional_correctness(jsonl_path, k=1)

# Print pass@1 score
print(f"\nFinal pass@1 score: {results['pass@1']:.4f}")
