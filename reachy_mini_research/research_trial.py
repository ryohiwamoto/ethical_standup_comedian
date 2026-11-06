"""Editable entry point for recording a Reachy Mini research trial."""

import argparse

from reachy_motion_controller import main as run_motion


# Select the condition and timings for the next take here.
CONDITION = "bow"  # "still" or "bow"
ANGLE_DEG = 10
MOVE_SECONDS = 3
HOLD_SECONDS = 3
SPEECH_TEXT = "Fuck off bitch."  # Set to "" for a silent trial.
SPEECH_PAUSE_SECONDS = 0.5


def main():
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--robot", action="store_true", help="Run on the real robot instead of previewing")
    args = parser.parse_args()

    cases = {"still": "still", "bow": "pitch_positive"}
    if CONDITION not in cases:
        parser.error('Set CONDITION to "still" or "bow" in research_trial.py')

    motion_args = [
        "--case", cases[CONDITION],
        "--angle", str(ANGLE_DEG),
        "--move", str(MOVE_SECONDS),
        "--hold", str(HOLD_SECONDS),
    ]
    if args.robot:
        motion_args.append("--robot")
    run_motion(motion_args, speech_text=SPEECH_TEXT, speech_pause=SPEECH_PAUSE_SECONDS)


if __name__ == "__main__":
    main()
