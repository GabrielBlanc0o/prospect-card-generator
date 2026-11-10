import json
import os
import shutil
import subprocess

TIMEOUT_SECONDS = 120


class ClaudeCLIError(RuntimeError):
    pass


def call_claude(system_prompt, user_prompt, model="claude-opus-5", json_schema=None):
    """Run a prompt through the Claude Code CLI (`claude -p`) using the
    user's logged-in subscription instead of the Anthropic API.

    If json_schema is given, the CLI's own structured-output validation is
    used (--output-format json --json-schema) and the validated object is
    returned. This is deliberately not plain-text + formatting instructions:
    Claude Code's built-in assistant behavior (markdown reports, skill-trigger
    asides) bleeds through a custom --system-prompt too often for that to be
    reliable — schema validation enforces the shape regardless.
    Without a schema, the raw text response is returned.
    """

    env = os.environ.copy()
    env.pop("ANTHROPIC_API_KEY", None)

    # On Windows, "claude" resolves to a .cmd shim that subprocess.run
    # won't find via PATH without shell=True — resolve the real path instead.
    claude_path = shutil.which("claude") or "claude"

    args = [
        claude_path, "-p",
        "--model", model,
        "--system-prompt", system_prompt,
        "--tools", "",
        "--disable-slash-commands",
        "--safe-mode",
        "--no-session-persistence",
    ]

    if json_schema is not None:
        args += ["--output-format", "json", "--json-schema", json.dumps(json_schema)]
    else:
        args += ["--output-format", "text"]

    try:
        result = subprocess.run(
            args,
            input=user_prompt,
            capture_output=True,
            text=True,
            encoding="utf-8",
            errors="replace",
            timeout=TIMEOUT_SECONDS,
            env=env,
        )
    except FileNotFoundError as error:
        raise ClaudeCLIError(
            "Claude Code CLI ('claude') not found on PATH. Install it first."
        ) from error
    except subprocess.TimeoutExpired as error:
        raise ClaudeCLIError(
            f"Claude Code CLI timed out after {TIMEOUT_SECONDS}s."
        ) from error

    if result.returncode != 0:
        stderr = result.stderr.strip()
        if "login" in stderr.lower() or "authentic" in stderr.lower():
            raise ClaudeCLIError(
                "Claude Code is not logged in. Run 'claude /login' yourself, then retry."
            )
        raise ClaudeCLIError(f"Claude Code CLI failed (exit {result.returncode}): {stderr}")

    if json_schema is None:
        return result.stdout.strip()

    try:
        payload = json.loads(result.stdout)
    except json.JSONDecodeError as error:
        raise ClaudeCLIError(f"Claude Code CLI returned invalid JSON: {error}") from error

    if payload.get("is_error"):
        raise ClaudeCLIError(f"Claude Code CLI reported an error: {payload.get('result')}")

    structured = payload.get("structured_output")
    if structured is None:
        raise ClaudeCLIError("Claude Code CLI did not return structured_output.")

    return structured
