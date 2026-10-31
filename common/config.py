"""Read pipeline settings from config.toml at the repo root."""

from __future__ import annotations

import os
import tomllib
from pathlib import Path

REPO_ROOT = Path(__file__).resolve().parent.parent
CONFIG_PATH = REPO_ROOT / "config.toml"

VOICE_MODES = ("placeholder", "recorder")


def load_config() -> dict:
    with CONFIG_PATH.open("rb") as f:
        config = tomllib.load(f)
    # VOICE=recorder on the command line overrides config.toml for one run.
    config["voice"] = os.environ.get("VOICE", config.get("voice", "placeholder"))
    if config["voice"] not in VOICE_MODES:
        raise ValueError(f"voice must be one of {VOICE_MODES}, got {config['voice']!r}")
    return config
