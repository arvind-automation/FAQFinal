import os
import shutil
from pathlib import Path

ROOT = Path(__file__).resolve().parent.parent
LOGO_ASSETS = ROOT / "assets" / "arvind-gcc-logo.png"
LOGO_DEST = ROOT / "app" / "static" / "images" / "arvind-gcc-logo.png"


def _find_logo_source() -> Path | None:
    env_path = os.getenv("LOGO_SOURCE_PATH", "").strip()
    if env_path:
        source = Path(env_path)
        if source.is_file():
            return source
    if LOGO_ASSETS.is_file():
        return LOGO_ASSETS
    return None


def ensure_logo():
    src = _find_logo_source()
    if not src:
        return

    if LOGO_DEST.is_file() and LOGO_DEST.stat().st_mtime >= src.stat().st_mtime:
        return

    LOGO_DEST.parent.mkdir(parents=True, exist_ok=True)
    shutil.copy2(src, LOGO_DEST)
