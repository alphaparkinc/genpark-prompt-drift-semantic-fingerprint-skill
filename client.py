"""Prompt Drift Semantic Fingerprint.
100% Python Standard Library.
"""
import re
import hashlib

class PromptDriftSemanticFingerprint:
    """Prompt template drift & structural fingerprint sentinel."""

    @staticmethod
    def compute_fingerprint(template_text: str) -> dict:
        vars_found = sorted(list(set(re.findall(r'\{\{\s*([a-zA-Z0-9_\.]+)\s*\}\}|\{([a-zA-Z0-9_]+)\}', template_text))))
        flat_vars = [v[0] or v[1] for v in vars_found if v[0] or v[1]]

        normalized = re.sub(r'\s+', ' ', template_text.strip().lower())
        content_hash = hashlib.sha256(normalized.encode("utf-8")).hexdigest()
        structure_hash = hashlib.sha256(",".join(flat_vars).encode("utf-8")).hexdigest()[:16]

        return {
            "content_hash": content_hash,
            "structure_hash": structure_hash,
            "variables": flat_vars,
            "char_count": len(template_text),
            "word_count": len(template_text.split())
        }

    @classmethod
    def detect_drift(cls, baseline_template: str, current_template: str) -> dict:
        b_fp = cls.compute_fingerprint(baseline_template)
        c_fp = cls.compute_fingerprint(current_template)

        is_identical = b_fp["content_hash"] == c_fp["content_hash"]
        b_vars = set(b_fp["variables"])
        c_vars = set(c_fp["variables"])

        missing_vars = sorted(list(b_vars - c_vars))
        added_vars = sorted(list(c_vars - b_vars))
        has_variable_drift = len(missing_vars) > 0 or len(added_vars) > 0

        return {
            "is_identical": is_identical,
            "has_variable_drift": has_variable_drift,
            "missing_variables": missing_vars,
            "added_variables": added_vars,
            "baseline_hash": b_fp["content_hash"][:12],
            "current_hash": c_fp["content_hash"][:12]
        }
