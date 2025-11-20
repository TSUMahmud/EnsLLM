import os
import google.generativeai as genai
from human_eval.data import read_problems

# Set your Gemini API key
GEMINI_API_KEY = "api_key"
genai.configure(api_key=GEMINI_API_KEY)

# Load HumanEval problems
problems = read_problems()

# Specify model name
model = "gemini-1.5-pro"

# Ensure model-specific directory exists
os.makedirs(model, exist_ok=True)

# Iterate over all problems
for problem_id, problem_data in problems.items():
    file_name = os.path.join(model, f"{problem_data['task_id']}.txt")
    
    # Skip if file already exists
    if os.path.exists(file_name):
        print(f"Skipping {file_name}, already exists.")
        continue

    try:
        # Generate solution using Gemini API
        model_gen = genai.GenerativeModel(model)
        response = model_gen.generate_content(problem_data["prompt"])

        # Extract model response
        solution = response.text.strip()

        # Save response to file
        with open(file_name, "w", encoding="utf-8") as f:
            f.write(solution)

        print(f"Saved: {file_name}")

    except Exception as e:
        print(f"Error processing {problem_id}: {e}")
