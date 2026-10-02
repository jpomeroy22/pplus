import subprocess
import sys
from pathlib import Path

# Could not get my test cases to run properly, used AI assitance to help with the code below. 
# --- start AI code ---
TEST_DIR = Path(__file__).parent
PPLUS = TEST_DIR.parent.parent / "src" / "pplus.py"
OUT_DIR = TEST_DIR / "output"
OUT_DIR.mkdir(exist_ok=True)

for test_file in sorted(TEST_DIR.glob("*.pp")):
    result = subprocess.run(
        [sys.executable, str(PPLUS), str(test_file)],
        capture_output=True, text=True, encoding="utf-8"
    )
    output = result.stdout + result.stderr + f"[exit code {result.returncode}]\n"
    (OUT_DIR / f"{test_file.stem}.out").write_text(output, encoding="utf-8")
    print(f"=== {test_file.name} ===\n{output}")

repl_input = (TEST_DIR / "repl_input.txt").read_text(encoding="utf-8")
result = subprocess.run(
    [sys.executable, str(PPLUS)],
    input=repl_input, capture_output=True, text=True, encoding="utf-8"
)
output = result.stdout + result.stderr
(OUT_DIR / "repl.out").write_text(output, encoding="utf-8")
print(f"=== repl ===\n{output}")
# --- end AI code ---