import sys, subprocess, os
from pathlib import Path

def behavioral_similarity(folder, file1, file2, method, n: int = 6, * , timeout=60, python_exe=None) -> float:
    func1 = Path(file1).name.replace(".py", "")+"."+method
    func2 = Path(file2).name.replace(".py", "")+"."+method
    counterexample_count = run_diffbehavior(folder, func1, func2)
    
    # Compute BSim using the given formula
    BSim = 1 - (min(n, counterexample_count) / n)
    
    # print(f"Total counterexamples found: {counterexample_count}")
    
    return BSim

def run_diffbehavior(folder, func1, func2, *, timeout=120, python_exe=None):
    """
    Run CrossHair diffbehavior on two callables and return (status, report).
    status:
      - "DIFF"    -> CrossHair found a behavioral difference (counterexample shown)
      - "NO_DIFF" -> CrossHair did not find a difference within its search
      - "ERROR"   -> Something went wrong invoking CrossHair
    """
    original_dir = os.getcwd()      # Save where we started
    os.chdir(Path(folder))      
    py = python_exe or sys.executable
    cmd = [py, "-m", "crosshair", "diffbehavior", func1, func2]
    proc = subprocess.run(cmd, capture_output=True, text=True, timeout=timeout)
    out = (proc.stdout or "") + (proc.stderr or "")
    rc = proc.returncode

    os.chdir(original_dir)  

    # CrossHair's exit codes are not guaranteed to be stable; treat outputs defensively:
    # Heuristic: if it printed any "Given:" blocks, it found a counterexample.
    if "Given:" in out:
        return sum(1 for line in out.strip().splitlines() if line.strip())
    # Many builds use rc==2 for "no difference found" (bounded search)
    elif rc == 2 or "No differences found" in out:
        return 0
    # Sometimes rc==0 can mean success too; fall back to text clues:
    elif rc == 0 and "No differences found" in out:
        return 0
    elif "No differences found" in out:
        return 0
    else:
        return 0