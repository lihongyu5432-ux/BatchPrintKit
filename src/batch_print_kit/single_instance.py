from __future__ import annotations

import json
import os
import tempfile
import time
import uuid
from pathlib import Path


HANDOFF_DIR = Path(tempfile.gettempdir()) / "batch_print_kit_handoff"
LOCK_PATH = HANDOFF_DIR / "collector.lock"


def collect_launch_paths(raw_args: list[str], *, wait_seconds: float = 0.9) -> tuple[bool, list[Path]]:
    """Merge near-simultaneous Explorer launches into one GUI process."""
    HANDOFF_DIR.mkdir(parents=True, exist_ok=True)
    _write_request(raw_args)

    lock_handle = _try_acquire_lock()
    if lock_handle is None:
        return False, []

    try:
        time.sleep(wait_seconds)
        return True, _read_pending_requests()
    finally:
        os.close(lock_handle)
        try:
            LOCK_PATH.unlink()
        except FileNotFoundError:
            pass


def _write_request(raw_args: list[str]) -> None:
    request_path = HANDOFF_DIR / f"{time.time_ns()}-{uuid.uuid4().hex}.json"
    payload = {"created_at": time.time(), "paths": raw_args}
    request_path.write_text(json.dumps(payload), encoding="utf-8")


def _try_acquire_lock() -> int | None:
    try:
        return os.open(str(LOCK_PATH), os.O_CREAT | os.O_EXCL | os.O_RDWR)
    except FileExistsError:
        return None


def _read_pending_requests() -> list[Path]:
    paths: list[Path] = []
    seen: set[Path] = set()
    cutoff = time.time() - 10

    for request_path in sorted(HANDOFF_DIR.glob("*.json")):
        try:
            payload = json.loads(request_path.read_text(encoding="utf-8"))
            if float(payload.get("created_at", 0)) < cutoff:
                request_path.unlink(missing_ok=True)
                continue
            for raw_path in payload.get("paths", []):
                path = Path(raw_path)
                key = path.expanduser().resolve() if path.exists() else path
                if key in seen:
                    continue
                seen.add(key)
                paths.append(path)
        finally:
            request_path.unlink(missing_ok=True)

    return paths
