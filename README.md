# EnsLLM: Enhancing LLM Code Generation with Ensembles: A Similarity-Based Selection Approach

Ensemble learning has been widely used in machine learning to improve model robustness, accuracy, and generalization, but has not yet been applied to code generation tasks with large language models (LLMs). We propose an ensemble approach for LLMs in code generation, called EnsLLM. Instead of relying on the output of a single model, we generate multiple candidate programs from different LLMs and apply a structured voting mechanism to select the most reliable solution.
For voting, we compute syntactic and semantic similarity using CodeBLEU and behavioral equivalence using CrossHair’s differential behavior analysis. By aggregating these similarity scores, we select the program that best aligns with the consensus among the candidates. Through experiments, we show that EnsLLM consistently outperforms standalone LLMs on the well-known HumanEval and the more challenging LiveCodeBench datasets, achieving an accuracy of 90.2% and 50.2%, respectively. In comparison, the best-performing individual LLM (GPT-4o) reaches 83.5% and 43.4% on the same datasets.
Furthermore, even when restricted to free open-source models, EnsLLM achieves accuracies of 80.5% and 41.6%, demonstrating the viability of our approach in resource-constrained settings.

---

## Project Structure

This project now includes **two folders** and **three main Python files**:

### **Files**
- **EnsLLM.py**  
  Main ensemble script. Selects the best solution among multiple LLM-generated programs using similarity-based ranking.
- **behavioral_similarity.py**  
  Computes Behavioral Similarity (BSim) using CrossHair to compare program behavior.
- **codebleu_similarity.py**  
  Computes CodeBLEU similarity scores between generated solutions.

### **Folders**
- **data_collection/**  
  Contains scripts used to run LLMs and collect candidate programs for each HumanEval and LiveCodeBench problem. Use these scripts to generate multiple `.py` solutions from various models (Ollama, GPT-4o, Gemini, etc.).
- **examples/**  
  Contains sample folders and example solution sets for testing EnsLLM.

---

## Prerequisites

Install the following dependencies:

| Library | Purpose | Install |
|--------|---------|---------|
| **ollama** | Run local LLMs | https://github.com/ollama/ollama |
| **ollama-python** | Interface to Ollama models | `pip install ollama` |
| **datasets** | Load HumanEval dataset | `pip install datasets` |
| **human-eval** | Access HumanEval tasks | `pip install human-eval` |
| **openai** | Access GPT-4o & Copilot API | `pip install openai` |
| **google-generativeai** | Access Gemini API | `pip install google-generativeai` |
| **codebleu** | Compute CodeBLEU similarity | `pip install codebleu` |
| **crosshair-tool** | Compute behavioral similarity | `pip install crosshair-tool` |
| **jsonlines** | Work with `.jsonl` output files | `pip install jsonlines` |
| **torch** | Required for some dataset operations | `pip install torch` |
| **tqdm** | Progress bars | `pip install tqdm` |
| **requests** | Custom API requests | `pip install requests` |

---

## How to Run

### **1. Collecting Code from LLMs**

Use the scripts in the **data_collection/** folder to:

- Launch LLMs (via Ollama, OpenAI, Gemini, etc.)
- Generate a `.py` file for each output solution
- Save results in model-specific folders


### **2. Run EnsLLM to select the best solution**

`EnsLLM.py` needs **two arguments**:

- **`input_folder`** – path to the folder containing multiple `.py` solutions  
- **`function_name`** – the expected function name shared by all solutions

Edit these variables inside `EnsLLM.py`:

```python
input_folder = "examples/problems2/"
function_name = "has_close_elements"
```

Then run: `python EnsLLM.py`

EnsLLM will:

- **Load** all `.py` files from the specified `input_folder`
- **Compute** CodeBLEU similarity scores and Behavioral Similarity (BSim)
- **Combine** these similarity metrics using an ensemble-ranking strategy
- **Select and output** the best-ranked program based on overall similarity


### 📚 Citation

If you use **EnsLLM** in your research or work, please cite the following paper:

```bibtex
@article{mahmud2025enhancing,
  title={Enhancing llm code generation with ensembles: A similarity-based selection approach},
  author={Mahmud, Tarek and Duan, Bin and Pasareanu, Corina and Yang, Guowei},
  journal={arXiv preprint arXiv:2503.15838},
  year={2025}
}

## 🛠️ Fix for CodeBLEU "TypeError: an integer is required"

If you encounter this error when running CodeBLEU:
`TypeError: an integer is required`

this is caused by newer versions of **Tree-sitter** returning a `Language` object, while CodeBLEU still expects an integer pointer from older Tree-sitter APIs.

To resolve the issue, update the **two files** located in your CodeBLEU package:

```
troubleshoot_codebleu/
    ├── utils.py
    └── codebleu.py
```


Replace both files with the updated versions provided to you.

No additional configuration, installation, or modifications are required.  
Simply updating these two files is enough to fix the integer requirement error and make CodeBLEU work correctly with newer Tree-sitter versions.
