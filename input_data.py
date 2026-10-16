"""Read explicit local files or URLs without network activity at import time."""
from pathlib import Path
from urllib.parse import urlparse
from urllib.request import urlopen


def read_text(source: str) -> str:
    if urlparse(source).scheme in {"http", "https"}:
        with urlopen(source, timeout=20) as response:
            return response.read().decode("utf-8-sig")
    return Path(source).read_text(encoding="utf-8-sig")
