import sys
import os
import subprocess
sys.path.insert(0, os.path.abspath(os.path.join(os.path.dirname(__file__), "../src")))

from pathlib import Path

def test_run_pipeline_end_to_end():
    test_file = "data/sample_tickets.json"
    assert Path(test_file).exists()

    result = subprocess.run(
        f"python src/run_pipeline.py --file {test_file}",
        shell=True,
        capture_output=True
    )
    assert result.returncode == 0
    assert Path("data/sample_tickets_anonymized_clustered_scored.json").exists()
