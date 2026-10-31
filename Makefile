# Usage:
#   make test                 run every video's tests
#   make preview VIDEO=01     fast low-quality cut (placeholder voice by default)
#   make final VIDEO=01       full 1080p60 render, stitched with ffmpeg
#   make style                render the shared style reel
#   make voice-check          render a 15s clip that tests the voice setup
# Override the voice for one run with VOICE=recorder or VOICE=placeholder.

PYTHON ?= .venv/bin/python
VIDEO ?= 01

.PHONY: setup test preview final style voice-check clean

setup:
	python3 -m venv .venv
	$(PYTHON) -m pip install -r requirements.txt

test:
	$(PYTHON) -m pytest

preview:
	$(PYTHON) -m pipeline.render $(VIDEO) --quality low

final:
	$(PYTHON) -m pipeline.render $(VIDEO) --quality final

style:
	$(PYTHON) -m manim -ql common/style_preview.py StylePreview -o style_preview

voice-check:
	$(PYTHON) -m manim -ql common/voice_check.py VoiceCheck -o voice_check

clean:
	rm -rf media build
