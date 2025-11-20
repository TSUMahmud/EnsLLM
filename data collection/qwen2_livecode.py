import ollama
import os
from datasets import load_dataset

# Ensure output directory exists
output_dir = "qwen2_livecode_outputs"
os.makedirs(output_dir, exist_ok=True)

# Load the LiveCodeBench dataset (code_generation_lite)
dataset = load_dataset("livecodebench/code_generation_lite", version_tag="release_v2", trust_remote_code=True)
problems = dataset["test"]  # Use the test split

# Define Ollama call function
def call_qwen2(prompt):
    response = ollama.chat(
        model="qwen2",  # Using Qwen2 model
        messages=[{"role": "user", "content": prompt}]
    )
    return response["message"]["content"]

# Iterate through dataset and query Qwen2
for problem in problems:
    problem_id = problem.get("question_id", "Unknown")
    content = problem.get("question_content", "No content")

    # Make sure the filename is safe for the filesystem
    safe_problem_id = str(problem_id).replace("/", "_")
    file_name = os.path.join(output_dir, f"{safe_problem_id}.txt")

    # Create a prompt suitable for Qwen2
    prompt = f"""
    Here is a programming problem:
    {content}

    Analyze the problem and predict its category based on difficulty, required programming skills, and complexity.
    """

    try:
        # Call Qwen2 API
        output = call_qwen2(prompt)

        # Save Qwen2 output to file
        with open(file_name, "w", encoding="utf-8") as f:
            f.write(f"Problem ID: {problem_id}\n")
            f.write(f"Problem Content:\n{content}\n\n")
            f.write(f"Qwen2 Analysis:\n{output}\n")

    except Exception as e:
        print(f"An error occurred with problem ID {problem_id}: {str(e)}")

print("Qwen2 processing completed. Results saved in 'qwen2_outputs/' directory.")
