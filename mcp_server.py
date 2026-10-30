# -*- coding: utf-8 -*-
import sys, json
from client import OpenClawGenParkSeoAudit

client = OpenClawGenParkSeoAudit()

TOOLS = [
    {
        "name": "calculate_readability_metrics",
        "description": "Calculates Flesch Reading Ease and Flesch-Kincaid Grade Level.",
        "inputSchema": {
            "type": "object",
            "properties": {"text": {"type": "string"}},
            "required": ["text"]
        }
    },
    {
        "name": "audit_keyword_density_and_stuffing",
        "description": "Audits keyword density and flags search engine keyword stuffing penalties.",
        "inputSchema": {
            "type": "object",
            "properties": {
                "text": {"type": "string"},
                "target_keywords": {"type": "array", "items": {"type": "string"}},
                "max_safe_density_pct": {"type": "number"}
            },
            "required": ["text", "target_keywords"]
        }
    },
    {
        "name": "compute_internal_linking_page_rank_penalty",
        "description": "Calculates crawl depth decay and internal link equity score.",
        "inputSchema": {
            "type": "object",
            "properties": {
                "crawl_depth": {"type": "integer"},
                "internal_inlinks_count": {"type": "integer"}
            },
            "required": ["crawl_depth", "internal_inlinks_count"]
        }
    }
]

def handle_request(req):
    method = req.get("method")
    rid = req.get("id")
    if method == "tools/list":
        return {"jsonrpc": "2.0", "id": rid, "result": {"tools": TOOLS}}
    elif method == "tools/call":
        params = req.get("params", {})
        tname = params.get("name")
        args = params.get("arguments", {})
        if tname == "calculate_readability_metrics":
            res = client.calculate_readability_metrics(args["text"])
            return {"jsonrpc": "2.0", "id": rid, "result": {"content": [{"type": "text", "text": json.dumps(res, indent=2)}]}}
        elif tname == "audit_keyword_density_and_stuffing":
            res = client.audit_keyword_density_and_stuffing(args["text"], args["target_keywords"], args.get("max_safe_density_pct", 3.5))
            return {"jsonrpc": "2.0", "id": rid, "result": {"content": [{"type": "text", "text": json.dumps(res, indent=2)}]}}
        elif tname == "compute_internal_linking_page_rank_penalty":
            res = client.compute_internal_linking_page_rank_penalty(args["crawl_depth"], args["internal_inlinks_count"])
            return {"jsonrpc": "2.0", "id": rid, "result": {"content": [{"type": "text", "text": json.dumps(res, indent=2)}]}}
        return {"jsonrpc": "2.0", "id": rid, "error": {"code": -32601, "message": "Method not found"}}
    return {"jsonrpc": "2.0", "id": rid, "error": {"code": -32600, "message": "Invalid Request"}}

def main():
    for line in sys.stdin:
        if not line.strip(): continue
        try:
            req = json.loads(line)
            resp = handle_request(req)
            sys.stdout.write(json.dumps(resp) + "\n")
            sys.stdout.flush()
        except Exception as e:
            sys.stdout.write(json.dumps({"jsonrpc": "2.0", "id": None, "error": {"code": -32700, "message": str(e)}}) + "\n")
            sys.stdout.flush()

if __name__ == "__main__":
    main()
