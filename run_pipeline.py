"""
Runs the full enhanced pipeline end-to-end:
  1. Employee EDA + SQLite module (original)
  2. Superstore EDA + SQLite + Visualization module (new)
  3. Pipeline architecture diagram generation

Usage:
    python run_pipeline.py
"""
import subprocess
import sys
import os

THIS_DIR = os.path.dirname(os.path.abspath(__file__))
SCRIPTS = os.path.join(THIS_DIR, "scripts")

STEPS = [
    "01_employee_solution.py",
    "02_superstore_solution.py",
    "03_generate_pipeline_diagram.py",
]

for step in STEPS:
    print(f"\n{'#'*90}\n# RUNNING: {step}\n{'#'*90}")
    result = subprocess.run([sys.executable, step], cwd=SCRIPTS)
    if result.returncode != 0:
        print(f"Step {step} failed with exit code {result.returncode}")
        sys.exit(result.returncode)

print("\nPipeline complete. See outputs/charts, outputs/exports, and db/ for results.")
