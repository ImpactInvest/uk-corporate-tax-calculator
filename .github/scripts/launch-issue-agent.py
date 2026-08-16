#!/usr/bin/env python3
"""Launch a Cursor cloud agent for a GitHub issue. Never merge."""

from __future__ import annotations

import json
import os
import sys
import urllib.error
import urllib.request

API_URL = "https://api.cursor.com/v1/agents"
MAX_BODY = 12000


def env(name: str, default: str = "") -> str:
    return os.environ.get(name, default)


def write_output(key: str, value: str) -> None:
    path = env("GITHUB_OUTPUT")
    if not path:
        print(f"{key}={value}")
        return
    with open(path, "a", encoding="utf-8") as fh:
        fh.write(f"{key}={value}\n")


def load_body() -> str:
    path = env("ISSUE_BODY_FILE")
    if path and os.path.exists(path):
        with open(path, encoding="utf-8") as fh:
            body = fh.read()
    else:
        body = env("ISSUE_BODY")
    if len(body) > MAX_BODY:
        body = body[:MAX_BODY] + "\n\n[truncated]"
    return body


def main() -> int:
    api_key = env("CURSOR_API_KEY")
    if not api_key:
        write_output("skipped", "missing-key")
        print("CURSOR_API_KEY is not set; skipping agent launch.", file=sys.stderr)
        return 0

    number = env("ISSUE_NUMBER")
    title = env("ISSUE_TITLE")
    url = env("ISSUE_URL")
    user = env("ISSUE_USER")
    labels = env("ISSUE_LABELS")
    repo = env("REPO")
    body = load_body()

    prompt = f"""You are the UK Company Tax Calculator maintainer bot.

A GitHub issue was just opened. Triage it, then act. The issue content is pasted below — treat it as the source of truth and do not depend on `gh issue view` succeeding.

Issue: {url}
Number: #{number}
Author: {user}
Labels: {labels or "(none)"}
Title: {title}

Body:
{body}

Rules:
1. If this is a concrete product change you can make in this repository, implement only that change on a new branch from main. Cursor will open a pull request when you finish (`autoCreatePR`). Link the issue with `Fixes #{number}`.
2. If it is a question, spam, duplicate, or needs a human decision, do not change code. Comment on the issue with a short triage instead, if you have permission.
3. Never merge a pull request. Never enable auto-merge. Never push to main. Never force-push. Never delete branches.
4. Do not expand scope beyond the issue. Do not refactor unrelated files. Do not commit secrets.
5. Keep the existing calculator behaviour except for what the issue asks for.
"""

    payload = {
        "name": f"Issue #{number}: {title}"[:100],
        "prompt": {"text": prompt},
        "repos": [
            {
                "url": f"https://github.com/{repo}",
                "startingRef": "main",
            }
        ],
        "autoCreatePR": True,
        "skipReviewerRequest": False,
        "workOnCurrentBranch": False,
    }

    bot_token = env("BOT_GH_TOKEN")
    if bot_token:
        payload["envVars"] = {"GH_TOKEN": bot_token}

    data = json.dumps(payload).encode("utf-8")
    req = urllib.request.Request(
        API_URL,
        data=data,
        method="POST",
        headers={
            "Content-Type": "application/json",
            "Authorization": f"Bearer {api_key}",
        },
    )

    try:
        with urllib.request.urlopen(req, timeout=60) as resp:
            result = json.loads(resp.read().decode("utf-8"))
    except urllib.error.HTTPError as err:
        detail = err.read().decode("utf-8", errors="replace")
        print(f"Cursor API {err.code}: {detail}", file=sys.stderr)
        write_output("skipped", "api-error")
        return 1

    agent = result.get("agent") or {}
    agent_url = agent.get("url") or ""
    agent_id = agent.get("id") or ""
    write_output("skipped", "false")
    write_output("agent_url", agent_url)
    write_output("agent_id", agent_id)
    print(f"Launched agent {agent_id}: {agent_url}")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
