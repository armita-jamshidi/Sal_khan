import pytest

from common.config import load_config


def test_default_voice_is_valid(monkeypatch):
    monkeypatch.delenv("VOICE", raising=False)
    assert load_config()["voice"] in ("placeholder", "recorder")


def test_env_overrides_voice(monkeypatch):
    monkeypatch.setenv("VOICE", "recorder")
    assert load_config()["voice"] == "recorder"


def test_bad_voice_rejected(monkeypatch):
    monkeypatch.setenv("VOICE", "robot")
    with pytest.raises(ValueError):
        load_config()
