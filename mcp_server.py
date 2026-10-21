"""MCP Server for Prompt Drift Semantic Fingerprint.
100% Python Standard Library JSON-RPC.
"""
import sys
import json
from client import PromptDriftSemanticFingerprint

def main():
    while True:
        line = sys.stdin.readline()
        if not line:
            break
        try:
            req = json.loads(line)
            method = req.get("method")
            msg_id = req.get("id")

            if method == "tools/list":
                resp = {
                    "jsonrpc": "2.0",
                    "id": msg_id,
                    "result": {
                        "tools": [
                            {
                                "name": "compute_fingerprint",
                                "description": "Compute structural and content fingerprint of prompt template",
                                "inputSchema": {
                                    "type": "object",
                                    "properties": {
                                        "template_text": {"type": "string"}
                                    },
                                    "required": ["template_text"]
                                }
                            },
                            {
                                "name": "detect_drift",
                                "description": "Detect variable and structural drift between baseline and current prompt",
                                "inputSchema": {
                                    "type": "object",
                                    "properties": {
                                        "baseline_template": {"type": "string"},
                                        "current_template": {"type": "string"}
                                    },
                                    "required": ["baseline_template", "current_template"]
                                }
                            }
                        ]
                    }
                }
            elif method == "tools/call":
                call_name = req.get("params", {}).get("name")
                args = req.get("params", {}).get("arguments", {})
                if call_name == "compute_fingerprint":
                    res = PromptDriftSemanticFingerprint.compute_fingerprint(args.get("template_text", ""))
                elif call_name == "detect_drift":
                    res = PromptDriftSemanticFingerprint.detect_drift(
                        args.get("baseline_template", ""),
                        args.get("current_template", "")
                    )
                else:
                    res = {"error": "Unknown tool"}
                resp = {
                    "jsonrpc": "2.0",
                    "id": msg_id,
                    "result": {"content": [{"type": "text", "text": json.dumps(res, indent=2)}]}
                }
            else:
                resp = {"jsonrpc": "2.0", "id": msg_id, "error": {"code": -32601, "message": "Method not found"}}
            sys.stdout.write(json.dumps(resp) + "\n")
            sys.stdout.flush()
        except Exception as e:
            sys.stdout.write(json.dumps({"jsonrpc": "2.0", "error": {"code": -32000, "message": str(e)}}) + "\n")
            sys.stdout.flush()

if __name__ == "__main__":
    main()
