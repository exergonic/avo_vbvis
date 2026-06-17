import json
import sys


def read_json_input():
    raw = sys.stdin.read()
    if not raw.strip():
        return {}

    try:
        return json.loads(raw)
    except json.JSONDecodeError as exc:
        raise SystemExit(f"Failed to parse JSON input: {exc}") from exc


def write_json_output(data):
    json.dump(data, sys.stdout)
    sys.stdout.write("\n")
    sys.stdout.flush()
