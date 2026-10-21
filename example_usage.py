"""Example usage for Prompt Drift Semantic Fingerprint."""
from client import PromptDriftSemanticFingerprint
import json

base = "Translate {{ source_text }} to {{ target_language }} accurately."
prod = "Translate {{ source_text }} to {{ target_language }} in a {{ tone }} tone."

drift = PromptDriftSemanticFingerprint.detect_drift(base, prod)
print(json.dumps(drift, indent=2))
