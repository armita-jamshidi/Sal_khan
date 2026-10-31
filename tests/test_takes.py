import json

from pipeline.takes import forget, load_takes, recorded_texts

NARRATION = """## hook
First line.

Second line.

## problem
Third line.
"""


def make_video(tmp_path, texts):
    (tmp_path / "narration.md").write_text(NARRATION)
    rec = tmp_path / "voiceovers" / "recorder"
    rec.mkdir(parents=True)
    takes = []
    for i, text in enumerate(texts):
        (rec / f"take{i}.mp3").write_bytes(b"audio")
        takes.append({"input_text": text, "input_data": {"input_text": text, "service": "recorder"},
                      "original_audio": f"take{i}.mp3", "final_audio": f"take{i}.mp3"})
    (rec / "cache.json").write_text(json.dumps(takes))
    return rec


def test_redo_one_line(tmp_path):
    rec = make_video(tmp_path, ["First line.", "Second line.", "Third line."])
    assert forget(tmp_path, "hook", 1) == ["Second line."]
    assert recorded_texts(load_takes(tmp_path)) == {"First line.", "Third line."}
    assert not (rec / "take1.mp3").exists() and (rec / "take0.mp3").exists()


def test_redo_whole_scene(tmp_path):
    make_video(tmp_path, ["First line.", "Second line.", "Third line."])
    assert sorted(forget(tmp_path, "hook", None)) == ["First line.", "Second line."]
    assert recorded_texts(load_takes(tmp_path)) == {"Third line."}


def test_redo_unrecorded_line_is_a_no_op(tmp_path):
    make_video(tmp_path, ["First line."])
    assert forget(tmp_path, "problem", 0) == []
    assert recorded_texts(load_takes(tmp_path)) == {"First line."}
