#!/usr/bin/env python3
"""Minimal, non-persistent OpenRouter chat-completions client."""
import getpass
import json
import os
import sys
import urllib.error
import urllib.request

MODEL_ID = "stealth/ox-alpha"
ENDPOINT = "https://openrouter.ai/api/v1/chat/completions"
DEFAULT_PROMPT = "Reply with exactly: OX_ALPHA_OK"


def main() -> int:
    prompt = " ".join(sys.argv[1:]).strip() or DEFAULT_PROMPT
    api_key = os.environ.get("OPENROUTER_API_KEY")
    if not api_key:
        try:
            api_key = getpass.getpass("OpenRouter API key (hidden input, not saved): ")
        except (EOFError, KeyboardInterrupt):
            print("STATUS=READY_FOR_MANUAL_KEY")
            return 4
    if not api_key:
        print("STATUS=READY_FOR_MANUAL_KEY")
        return 4

    payload = json.dumps({
        "model": MODEL_ID,
        "messages": [{"role": "user", "content": prompt}],
        "max_tokens": 512,
    }).encode("utf-8")
    request = urllib.request.Request(
        ENDPOINT,
        data=payload,
        headers={
            "Authorization": f"Bearer {api_key}",
            "Content-Type": "application/json",
            "HTTP-Referer": "https://openrouter.ai",
            "X-Title": "Ox Alpha Local Client",
        },
        method="POST",
    )
    try:
        with urllib.request.urlopen(request, timeout=300) as response:
            result = json.load(response)
    except urllib.error.HTTPError as exc:
        if exc.code in (429, 500, 502, 503, 504):
            print(f"STATUS=FAILED_HTTP_{exc.code}")
            print("RETRYABLE=yes")
        elif exc.code == 401:
            print("STATUS=FAILED_HTTP_401")
            print("HINT=Check the manually supplied key; it was not saved.")
        elif exc.code == 402:
            print("STATUS=FAILED_HTTP_402")
            print("HINT=Account balance or free-model policy may have changed.")
        else:
            print(f"STATUS=FAILED_HTTP_{exc.code}")
        return 1
    except Exception as exc:
        print("STATUS=FAILED")
        print(f"ERROR_TYPE={type(exc).__name__}")
        return 1

    choices = result.get("choices") or []
    content = ((choices[0].get("message") or {}).get("content") if choices else None)
    print(f"MODEL={result.get('model')}")
    print("ASSISTANT=" + (content or ""))
    if result.get("usage") is not None:
        print("USAGE=" + json.dumps(result["usage"], ensure_ascii=False, separators=(",", ":")))
    if result.get("cost") is not None:
        print("COST=" + json.dumps(result["cost"], ensure_ascii=False, separators=(",", ":")))
    print("STATUS=PASS" if content else "STATUS=FAILED_EMPTY_RESPONSE")
    return 0 if content else 1


if __name__ == "__main__":
    sys.exit(main())
