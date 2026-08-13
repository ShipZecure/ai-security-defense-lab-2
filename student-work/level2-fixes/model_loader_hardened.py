# model_loader_hardened.py
# DataForge ML — Genomics Analysis Pipeline
# SECURITY PATCH: removed unsafe pickle loading
# Added pre-deployment integrity scanning and safetensors format
# Patched by: Damilola Aibinuola — 12/08/2026

import subprocess
import sys
from pathlib import Path

MODEL_REPO  = "verified-org/genomics-analyzer-v2"
MODEL_FILE  = "genomics_analyzer_v2.safetensors"
MODEL_PATH  = Path("/tmp") / MODEL_FILE


def scan_model_before_loading(model_path: Path) -> None:
    """
    Run Picklescan against the model file before loading.
    Raises an exception if any threat is detected.
    This function must pass before load_model() is allowed to continue.
    """
    result = subprocess.run(
        ["picklescan", "-p", str(model_path)],
        capture_output=True,
        text=True
    )
    if "FOUND" in result.stdout:
        raise RuntimeError(
            f"SECURITY ALERT: Model scan failed. "
            f"Dangerous payload detected in {model_path}. "
            f"Aborting load. Details: {result.stdout}"
        )
    print(f"[SCAN] {model_path.name} passed integrity check. Safe to load.")


def download_model() -> Path:
    """Download model weights from verified Hugging Face repository."""
    if not MODEL_PATH.exists():
        print(f"Downloading {MODEL_FILE} from verified source...")
        import requests
        response = requests.get(
            f"https://huggingface.co/{MODEL_REPO}/resolve/main/{MODEL_FILE}",
            stream=True
        )
        with open(MODEL_PATH, "wb") as f:
            for chunk in response.iter_content(chunk_size=8192):
                f.write(chunk)
    return MODEL_PATH


def load_model():
    """
    Load the genomics analysis model.
    PATCHED: scan runs before load — if scan fails, load never executes.
    PATCHED: safetensors format used instead of pickle.
    """
    model_path = download_model()

    # Security gate: scan must pass before load proceeds
    scan_model_before_loading(model_path)

    # Safe loading using safetensors — cannot execute arbitrary code
    from safetensors import safe_open
    tensors = {}
    with safe_open(str(model_path), framework="pt") as f:
        for key in f.keys():
            tensors[key] = f.get_tensor(key)

    return tensors


def analyze_sample(sample_data: dict) -> dict:
    """Run genomics analysis on a patient sample."""
    model = load_model()
    return {"status": "complete", "model_keys": list(model.keys())}