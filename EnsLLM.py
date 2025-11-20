import os
import json
import re
import ast
import inspect
import itertools
from typing import List, Dict
from codebleu import calc_codebleu
import subprocess
from behavioral_similarity import *

def get_code(file_path: str) -> str:
    with open(file_path, "r", encoding="utf-8") as f:
        return f.read()

def file_has_function(file_path: str, function: str) -> bool:
    with open(file_path, "r", encoding="utf-8") as f:
        return function in f.read()

def check_for_valid_code(folder_path: str, function: str) -> Dict[str, str]:

    extracted_solutions = []
    
    for filename in os.listdir(folder_path):
        if filename.endswith(".py"):
            file_path = os.path.join(folder_path, filename)
            process = subprocess.run(
                ["python", file_path],
                capture_output=True,
                text=True
            )

            return_code = process.returncode

            # print("Return code:", return_code)

            if return_code != 0:
                print(file_path + " : Script failed with an error")
                # Output and errors
                stdout = process.stdout
                stderr = process.stderr
                print("STDOUT:", stdout)
                print("STDERR:", stderr)
            else:
                if file_has_function(file_path, function) == True:
                    extracted_solutions.append(file_path)
                else:
                    print(file_path + " : Doesn't have the function")
    
    return extracted_solutions

def codebleu_similarity(func1_code: str, func2_code: str) -> float:
    syntax_weight = 0.5
    dataflow_weight = 0.5

    codebleu_score = calc_codebleu(
        [func1_code],
        func2_code,
        lang="python",
        # weights=(syntax_weight, 0, dataflow_weight, 0)
    )

    SSim = codebleu_score["codebleu"]
    # print(codebleu_score)
    return SSim

def compute_pairwise_similarity(folder_path, solutions: Dict[str, str], function: str, lambda_val: float = 0.5) -> Dict[str, float]:
    # filenames = list(solutions.keys())
    similarity_scores = {filename: 0.0 for filename in solutions}

    for (file1, file2) in itertools.combinations(solutions, 2):
        print("Pairwise similarity between: " + file1 + " and" + file2)
        code1, code2 = get_code(file1), get_code(file2)

        codebleu_score = codebleu_similarity(code1, code2)
        print(f"Syntactic Similarity (SSim): {codebleu_score:.4f}")

        bsim_score = behavioral_similarity(folder_path, file1, file2, function)
        print(f"Behavioral Similarity (BSim): {bsim_score:.4f}")

        similarity = lambda_val * codebleu_score + (1 - lambda_val) * bsim_score
        
        similarity_scores[file1] += similarity
        similarity_scores[file2] += similarity

    return similarity_scores

def EnsLLM(folder_path: str, function: str, lambda_val: float = 0.5):
    # Step 1: Extract solutions
    solutions = check_for_valid_code(folder_path, function)
    if len(solutions)==0:
        print("No valid solutions found in the folder.")
        return

    # Step 2: Compute pairwise similarity scores
    similarity_scores = compute_pairwise_similarity(folder_path, solutions, function, lambda_val)

    # Step 3: Rank solutions and select the best one
    best_solution_file = max(similarity_scores, key=similarity_scores.get)
    best_solution_code = get_code(best_solution_file)

    # Step 4: Save the best solution
    best_solution_path = os.path.join(folder_path, "best_program.py")
    with open(best_solution_path, "w", encoding="utf-8") as f:
        f.write(best_solution_code)

    print(f"Best solution saved as {best_solution_path} (from {best_solution_file})")


# input_folder = "examples/programs2";
# function_name = "separate_paren_groups"

input_folder = "examples/programs2";
function_name = "has_close_elements"


EnsLLM(input_folder, function_name, lambda_val=0.5)

