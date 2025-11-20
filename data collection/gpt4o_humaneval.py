import os
import openai
from human_eval.data import read_problems

# Set your OpenAI API key (Alternatively, use os.environ["OPENAI_API_KEY"])
OPENAI_API_KEY = "api_key"

# Load HumanEval problems
problems = read_problems()

# Specify model name
model = "gpt-4o"

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
        # Generate solution using GPT-4o
        response = openai.ChatCompletion.create(
            model=model,
            messages=[{"role": "user", "content": problem_data["prompt"]}],
            api_key=OPENAI_API_KEY
        )

        # Extract model response
        solution = response["choices"][0]["message"]["content"]

        # Save response to file
        with open(file_name, "w", encoding="utf-8") as f:
            f.write(solution)

        print(f"Saved: {file_name}")

    except Exception as e:
        print(f"Error processing {problem_id}: {e}")
