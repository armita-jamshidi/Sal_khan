import subprocess

import pytest

from common.audio import has_audio, integrated_loudness, level_audio_file, level_video


def tone(path, volume_db, seconds=4):
    """A speech-band tone at a given volume, standing in for a recorded take."""
    subprocess.run(
        ["ffmpeg", "-y", "-loglevel", "error", "-f", "lavfi",
         "-i", f"sine=frequency=220:duration={seconds}", "-af", f"volume={volume_db}dB", str(path)],
        check=True,
    )
    return path


def test_quiet_and_loud_takes_end_up_level(tmp_path):
    quiet = tone(tmp_path / "quiet.mp3", -30)
    loud = tone(tmp_path / "loud.mp3", -3)
    assert integrated_loudness(loud) - integrated_loudness(quiet) > 20
    for take in (quiet, loud):
        level_audio_file(take, -16)
        assert integrated_loudness(take) == pytest.approx(-16, abs=1)


def test_silence_is_left_alone(tmp_path):
    silent = tmp_path / "silent.wav"
    subprocess.run(["ffmpeg", "-y", "-loglevel", "error", "-f", "lavfi",
                    "-i", "anullsrc=d=2", str(silent)], check=True)
    before = silent.read_bytes()
    level_audio_file(silent, -16)
    assert silent.read_bytes() == before


def test_video_mixed_to_youtube_loudness(tmp_path):
    src = tmp_path / "src.mp4"
    subprocess.run(
        ["ffmpeg", "-y", "-loglevel", "error", "-f", "lavfi", "-i", "color=c=black:s=64x64:d=4",
         "-f", "lavfi", "-i", "sine=frequency=220:duration=4", "-af", "volume=-25dB",
         "-shortest", "-c:v", "libx264", "-c:a", "aac", str(src)],
        check=True,
    )
    out = tmp_path / "out.mp4"
    level_video(src, out, -14)
    assert integrated_loudness(out) == pytest.approx(-14, abs=1)


def test_video_without_audio_is_copied(tmp_path):
    src = tmp_path / "mute.mp4"
    subprocess.run(["ffmpeg", "-y", "-loglevel", "error", "-f", "lavfi",
                    "-i", "color=c=black:s=64x64:d=1", "-c:v", "libx264", str(src)], check=True)
    assert not has_audio(src)
    out = tmp_path / "out.mp4"
    level_video(src, out, -14)
    assert out.read_bytes() == src.read_bytes()


def test_new_takes_are_leveled_and_cached_ones_are_not(tmp_path, monkeypatch):
    import manim_voiceover.services.recorder as recorder
    from manim_voiceover.services.recorder import RecorderService

    from common.voices import make_speech_service

    # The key listener needs a desktop session; this test never records, so skip that check.
    monkeypatch.setattr(recorder, "prompt_ask_missing_extras", lambda *args: None)

    def fake_record(self, text, cache_dir=None, path=None, **kwargs):
        name = text.split()[0] + ".mp3"
        if not (tmp_path / name).exists():  # a real take only happens when it isn't cached
            tone(tmp_path / name, -30)
        return {"input_text": text, "input_data": {"input_text": text}, "original_audio": name}

    monkeypatch.setattr(RecorderService, "generate_from_text", fake_record)
    service = make_speech_service("recorder", tmp_path, {"take_lufs": -16})
    service.generate_from_text("new take")
    assert integrated_loudness(tmp_path / "new.mp3") == pytest.approx(-16, abs=1)

    tone(tmp_path / "cached.mp3", -30)
    service.generate_from_text("cached take")
    assert integrated_loudness(tmp_path / "cached.mp3") < -25
