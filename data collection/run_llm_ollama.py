from human_eval.data import write_jsonl, read_problems
import ollama


problems = read_problems()
model = "llama3.2"


for problem in problems:
    file_name = model+"/"+problems[problem]['task_id']+".txt"


    response = ollama.chat(model=model, messages=[
      {
        'role': 'user',
        'content': problems[problem]['prompt'],
      },
    ])


    f = open(file_name, "w", encoding='utf-8')
    f.write(response['message']['content'])
    f.close()
    print(file_name)