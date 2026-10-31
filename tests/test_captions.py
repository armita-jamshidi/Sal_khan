import subprocess

from common.captions import Cue, read_srt, stitch_captions, write_srt

SCENE_SRT = """1
00:00:00,000 --> 00:00:02,500
Every March, thousands of students open an envelope.

2
00:00:02,600 --> 00:00:04,000
How does one computer decide? [TODO-VERIFY: check the month]
"""


def clip(path, seconds):
    subprocess.run(["ffmpeg", "-y", "-loglevel", "error", "-f", "lavfi",
                    "-i", f"color=c=black:s=64x64:d={seconds}", "-c:v", "libx264", str(path)], check=True)
    return path


def test_read_strips_todo_verify(tmp_path):
    path = tmp_path / "a.srt"
    path.write_text(SCENE_SRT)
    cues = read_srt(path)
    assert [c.text for c in cues] == ["Every March, thousands of students open an envelope.",
                                      "How does one computer decide?"]
    assert (cues[1].start, cues[1].end) == (2.6, 4.0)


def test_round_trip(tmp_path):
    cues = [Cue(0, 1.25, "One."), Cue(3661.5, 3662, "Two\nlines.")]
    write_srt(cues, tmp_path / "x.srt")
    assert read_srt(tmp_path / "x.srt") == cues


def test_second_scene_is_shifted_by_first_clip(tmp_path):
    first = clip(tmp_path / "Hook.mp4", 5)
    second = clip(tmp_path / "Problem.mp4", 3)
    no_voice = clip(tmp_path / "Outro.mp4", 2)  # no .srt: still counts toward later offsets
    last = clip(tmp_path / "End.mp4", 2)
    (tmp_path / "Hook.srt").write_text(SCENE_SRT)
    (tmp_path / "Problem.srt").write_text("1\n00:00:00,500 --> 00:00:01,500\nApplicants rank programs.\n")
    (tmp_path / "End.srt").write_text("1\n00:00:00,000 --> 00:00:01,000\nThanks.\n")

    out = tmp_path / "video.srt"
    assert stitch_captions([first, second, no_voice, last], out) == 4
    cues = read_srt(out)
    assert abs(cues[2].start - 5.5) < 0.05
    assert abs(cues[3].start - 10.0) < 0.05
    assert out.read_text().startswith("1\n00:00:00,000 --> 00:00:02,500\n")
