import subprocess
import sys

# sys.executable = wahi Python jo main.py chala raha hai (venv ho ya na ho)
PYTHON = sys.executable


def run_step(script_name, message):
    """Ek script chalata hai. Fail ho to poora program ruk jata hai."""
    print(f"\n=== {message} ===")
    result = subprocess.run([PYTHON, script_name])
    if result.returncode != 0:
        print(f"\n{script_name} mein error aaya, isliye yahin ruk gaye.")
        sys.exit(1)


if __name__ == "__main__":
    run_step("fetch_data.py", "Step 1: YouTube se data nikal rahe hain")
    run_step("visualize.py", "Step 2: Dashboard bana rahe hain")
    print("\nSab kuch ho gaya! charts/dashboard.html browser mein khul gaya hoga.")
