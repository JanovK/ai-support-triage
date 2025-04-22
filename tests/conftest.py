import pytest
import subprocess
import spacy.util

@pytest.fixture(scope="session", autouse=True)
def ensure_spacy_model():
    model_name = "en_core_web_sm"
    if not spacy.util.is_package(model_name):
        subprocess.run(["python", "-m", "spacy", "download", model_name], check=True)
