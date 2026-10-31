import shutil

import pytest

from common.voices import OfflineService, PlaceholderService, make_speech_service

needs_offline_voice = pytest.mark.skipif(
    not (shutil.which("espeak-ng") or shutil.which("espeak") or shutil.which("say")),
    reason="no offline text-to-speech program installed",
)


@needs_offline_voice
def test_offline_voice_writes_mp3(tmp_path):
    service = OfflineService(cache_dir=str(tmp_path))
    data = service.generate_from_text("Applicants rank programs.")
    audio = tmp_path / data["original_audio"]
    assert audio.suffix == ".mp3" and audio.stat().st_size > 0


@needs_offline_voice
def test_placeholder_falls_back_when_gtts_fails(tmp_path, monkeypatch):
    service = PlaceholderService(engine="auto", cache_dir=str(tmp_path))

    class BrokenGTTS:
        def generate_from_text(self, *args, **kwargs):
            raise Exception("gTTS gave an error")

    monkeypatch.setattr(service, "gtts", lambda: BrokenGTTS())
    data = service.generate_from_text("Programs rank applicants.")
    assert data["input_data"]["service"] == "offline"
    assert service.engine == "offline"


def test_gtts_only_does_not_fall_back(tmp_path, monkeypatch):
    service = PlaceholderService(engine="gtts", cache_dir=str(tmp_path))

    class BrokenGTTS:
        def generate_from_text(self, *args, **kwargs):
            raise Exception("gTTS gave an error")

    monkeypatch.setattr(service, "gtts", lambda: BrokenGTTS())
    with pytest.raises(Exception, match="gTTS"):
        service.generate_from_text("Hello.")


def test_unknown_engine_rejected(tmp_path):
    with pytest.raises(ValueError):
        PlaceholderService(engine="robot", cache_dir=str(tmp_path))


def test_switch_picks_service(tmp_path):
    service = make_speech_service("placeholder", tmp_path, {"placeholder_engine": "offline"})
    assert isinstance(service, PlaceholderService) and service.engine == "offline"
    with pytest.raises(ValueError):
        make_speech_service("robot", tmp_path, {})
