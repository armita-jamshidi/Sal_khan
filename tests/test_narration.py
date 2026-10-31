from common.narration import load_narration, todo_verify_notes

SAMPLE = """# Narration

<!-- editor note, not spoken -->

## hook
Every year, thousands of students open an envelope.

How does one computer decide all of this
fairly? [TODO-VERIFY: check the number]

## problem
Applicants rank programs.
"""


def test_scenes_and_lines(tmp_path):
    path = tmp_path / "narration.md"
    path.write_text(SAMPLE)
    scenes = load_narration(path)
    assert list(scenes) == ["hook", "problem"]
    assert scenes["hook"] == [
        "Every year, thousands of students open an envelope.",
        "How does one computer decide all of this fairly?",
    ]
    assert scenes["problem"] == ["Applicants rank programs."]


def test_todo_verify_notes_are_listed(tmp_path):
    path = tmp_path / "narration.md"
    path.write_text(SAMPLE)
    assert todo_verify_notes(path) == ["[TODO-VERIFY: check the number]"]
