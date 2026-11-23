"""Validate the monitoring configuration."""

import json
import sys
from pathlib import Path


def validate_config(config):
    errors = []

    service = config.get("service")
    if not isinstance(service, str) or not service.strip():
        errors.append("service must be a non-empty string")

    port = config.get("port")
    if isinstance(port, bool) or not isinstance(port, int) or not 1 <= port <= 65535:
        errors.append("port must be between 1 and 65535")

    interval = config.get("interval_seconds")
    interval_ok = (
        isinstance(interval, int) and not isinstance(interval, bool) and interval > 0
    )
    if not interval_ok:
        errors.append("interval_seconds must be a positive integer")

    timeout = config.get("timeout_seconds")
    timeout_ok = (
        isinstance(timeout, (int, float))
        and not isinstance(timeout, bool)
        and timeout > 0
    )
    if not timeout_ok:
        errors.append("timeout_seconds must be a positive number")

    if interval_ok and timeout_ok and timeout >= interval:
        errors.append("timeout_seconds must be less than interval_seconds")

    return errors


if __name__ == "__main__":
    path = Path(__file__).resolve().parent.parent / "config" / "monitoring.json"
    problems = validate_config(json.loads(path.read_text(encoding="utf-8")))
    if problems:
        for problem in problems:
            print(problem)
        sys.exit(1)
    print("Configuration valid")
