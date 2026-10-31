"""Speech services behind the voice switch in config.toml.

    placeholder -> gTTS robot voice. If Google can't be reached (offline, or a
                   locked-down network), it falls back to an offline voice:
                   espeak-ng on Linux, or the built-in `say` on macOS.
    recorder    -> you read each narration line into the mic.

The offline voice sounds worse than gTTS but has the same job: give every line
a realistic length so the animation timing is right before you record.
"""

from __future__ import annotations

import shutil
import subprocess
import tempfile
from pathlib import Path

from manim import logger
from manim_voiceover.helper import remove_bookmarks
from manim_voiceover.services.base import SpeechService, initialize_speech_service

PLACEHOLDER_ENGINES = ("auto", "gtts", "offline")


def offline_tts_command() -> list[str] | None:
    """The first offline text-to-speech program on this machine, or None."""
    for program in ("espeak-ng", "espeak"):
        if shutil.which(program):
            return [program, "-v", "en-us", "-s", "165"]
    if shutil.which("say"):
        return ["say"]
    return None


class OfflineService(SpeechService):
    """Placeholder voice that needs no network: espeak-ng or macOS `say`."""

    def __init__(self, **kwargs):
        self.command = offline_tts_command()
        if self.command is None:
            raise RuntimeError(
                "No offline voice found. Install espeak-ng (apt install espeak-ng / "
                "brew install espeak-ng), or set voice = \"recorder\"."
            )
        initialize_speech_service(self, kwargs)

    def generate_from_text(self, text, cache_dir=None, path=None, **kwargs):
        cache_dir = Path(cache_dir or self.cache_dir)
        input_text = remove_bookmarks(text)
        input_data = {"input_text": input_text, "service": "offline"}
        cached = self.get_cached_result(input_data, cache_dir)
        if cached is not None:
            return cached

        audio_path = str(path) if path else self.get_audio_basename(input_data) + ".mp3"
        with tempfile.TemporaryDirectory() as tmp:
            # espeak writes wav, `say` writes aiff; ffmpeg turns either into mp3.
            raw = Path(tmp) / ("speech.aiff" if self.command[0] == "say" else "speech.wav")
            out_flag = ["-o", str(raw)] if self.command[0] == "say" else ["-w", str(raw)]
            subprocess.run([*self.command, *out_flag, input_text], check=True, capture_output=True)
            subprocess.run(
                ["ffmpeg", "-y", "-loglevel", "error", "-i", str(raw), str(cache_dir / audio_path)],
                check=True,
            )
        return {"input_text": text, "input_data": input_data, "original_audio": audio_path}


class PlaceholderService(SpeechService):
    """gTTS, switching to OfflineService for the rest of the run if gTTS fails."""

    def __init__(self, engine: str = "auto", lang: str = "en", tld: str = "com", **kwargs):
        if engine not in PLACEHOLDER_ENGINES:
            raise ValueError(f"placeholder_engine must be one of {PLACEHOLDER_ENGINES}, got {engine!r}")
        initialize_speech_service(self, kwargs)
        self.engine = engine
        self.lang, self.tld = lang, tld
        self._gtts = None
        self._offline = None

    def gtts(self):
        if self._gtts is None:
            from manim_voiceover.services.gtts import GTTSService

            self._gtts = GTTSService(lang=self.lang, tld=self.tld, cache_dir=self.cache_dir)
        return self._gtts

    def offline(self):
        if self._offline is None:
            self._offline = OfflineService(cache_dir=self.cache_dir)
        return self._offline

    def generate_from_text(self, text, cache_dir=None, path=None, **kwargs):
        if self.engine == "offline":
            return self.offline().generate_from_text(text, cache_dir, path)
        try:
            return self.gtts().generate_from_text(text, cache_dir, path, **kwargs)
        except Exception as error:
            if self.engine == "gtts":
                raise
            logger.warning(f"gTTS failed ({error}); using the offline placeholder voice instead.")
            for empty in Path(self.cache_dir).glob("*.mp3"):  # gTTS leaves a 0-byte file behind
                if empty.stat().st_size == 0:
                    empty.unlink()
            self.engine = "offline"
            return self.offline().generate_from_text(text, cache_dir, path)


def make_speech_service(voice: str, cache_dir: Path, settings: dict):
    """The single switch between the robot placeholder voice and your mic."""
    if voice == "placeholder":
        return PlaceholderService(
            engine=settings.get("placeholder_engine", "auto"),
            lang=settings.get("gtts_lang", "en"),
            tld=settings.get("gtts_tld", "com"),
            cache_dir=str(cache_dir),
        )
    if voice == "recorder":
        from manim_voiceover.services.recorder import RecorderService

        # Without a device number, manim-voiceover asks which mic to use for every scene.
        return RecorderService(device_index=settings.get("recorder_device"), cache_dir=str(cache_dir))
    raise ValueError(f"unknown voice mode {voice!r}")
