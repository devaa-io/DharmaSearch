"""Small I/O helpers shared by DharmaSearch build commands."""

from __future__ import annotations

import os
import tempfile
from pathlib import Path


def write_text_atomic(path: Path, content: str) -> None:
    """Replace a generated file only after its complete contents are on disk."""
    path.parent.mkdir(parents=True, exist_ok=True)
    try:
        destination_mode = path.stat().st_mode & 0o7777
    except FileNotFoundError:
        destination_mode = 0o644
    handle = tempfile.NamedTemporaryFile(
        mode="w", encoding="utf-8", dir=path.parent, prefix=f".{path.name}.", delete=False
    )
    temporary = Path(handle.name)
    try:
        with handle:
            handle.write(content)
            handle.flush()
            os.fsync(handle.fileno())
        os.chmod(temporary, destination_mode)
        os.replace(temporary, path)
    finally:
        temporary.unlink(missing_ok=True)
