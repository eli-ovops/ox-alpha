#!/usr/bin/env python3
"""Read the public OpenRouter model catalog and enforce the free-model gate."""
import json
import sys
import urllib.request

MODEL_ID = "stealth/ox-alpha"
CATALOG_URL = "https://openrouter.ai/api/v1/models"


def main() -> int:
    try:
        request = urllib.request.Request(CATALOG_URL, headers={"User-Agent": "ox-alpha-local/1.0"})
        with urllib.request.urlopen(request, timeout=20) as response:
            catalog = json.load(response)
    except Exception as exc:
        print("STATUS=FAILED")
        print(f"ERROR_TYPE={type(exc).__name__}")
        return 1

    model = next((item for item in catalog.get("data", []) if item.get("id") == MODEL_ID), None)
    if model is None:
        print("MODEL_FOUND=no")
        print(f"MODEL_ID={MODEL_ID}")
        print("STATUS=BLOCKED_MODEL_UNAVAILABLE")
        return 2

    pricing = model.get("pricing") or {}
    prompt_price = pricing.get("prompt")
    completion_price = pricing.get("completion")
    print("MODEL_FOUND=yes")
    print(f"MODEL_ID={MODEL_ID}")
    print(f"PROMPT_PRICE={prompt_price}")
    print(f"COMPLETION_PRICE={completion_price}")
    print(f"CONTEXT_LENGTH={model.get('context_length')}")
    if prompt_price != "0" or completion_price != "0":
        print("STATUS=BLOCKED_MODEL_NOT_FREE")
        return 3
    print("STATUS=PASS")
    return 0


if __name__ == "__main__":
    sys.exit(main())
