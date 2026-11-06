"""Manual motion pilot for Reachy Mini; never moves on startup."""

import argparse
import csv
from datetime import datetime
import json
import math
from pathlib import Path
import time
from urllib.request import ProxyHandler, build_opener


ROOT = Path(__file__).resolve().parent
CASES = {
    "1": ("still", 0, 0),
    "2": ("pitch_positive", 1, 0),
    "3": ("pitch_negative", -1, 0),
    "4": ("yaw_positive", 0, 1),
    "5": ("yaw_negative", 0, -1),
}
FIELDS = (
    "timestamp", "trial_id", "mode", "case", "pitch_delta_deg", "yaw_delta_deg",
    "move_seconds", "hold_seconds", "elapsed_seconds", "baseline_pose",
    "target_pose", "observed_pose", "return_pose", "status", "error", "memo",
)


def get_status():
    # Local control must not travel through a configured HTTP proxy.
    opener = build_opener(ProxyHandler({}))
    with opener.open("http://127.0.0.1:8000/api/daemon/status", timeout=5) as response:
        return json.load(response)


def require_ready(status):
    backend = status.get("backend_status") or {}
    if status.get("state") != "running" or not backend.get("ready"):
        raise RuntimeError("Robot is not ready. Check Reachy Mini Control.")
    if status.get("simulation_enabled") or status.get("mockup_sim_enabled"):
        raise RuntimeError("Simulation detected. This mode is for the real robot.")
    if status.get("error") or backend.get("error"):
        raise RuntimeError("Daemon reports an error. Inspect Control logs.")
    if backend.get("motor_control_mode") != "enabled":
        raise RuntimeError("Wake Up the robot in Control, then retry.")


def validate_baseline(pose):
    import numpy as np

    if pose.shape != (4, 4) or not np.isfinite(pose).all():
        raise RuntimeError("Invalid starting head pose.")
    cosine = float(np.clip((np.trace(pose[:3, :3]) - 1) / 2, -1, 1))
    if math.degrees(math.acos(cosine)) > 20:
        raise RuntimeError("Start with the head near its neutral orientation.")
    if np.linalg.norm(pose[:3, 3]) > 0.03:
        raise RuntimeError("Starting head translation exceeds the pilot limit.")


def execute_trial(robot, pitch, yaw, move_seconds, hold_seconds):
    from reachy_mini.utils import create_head_pose

    require_ready(get_status())
    baseline = robot.get_current_head_pose().copy()
    validate_baseline(baseline)
    target = baseline @ create_head_pose(pitch=pitch, yaw=yaw, degrees=True)
    data = {
        "baseline_pose": json.dumps(baseline.tolist()),
        "target_pose": json.dumps(target.tolist()),
    }
    moving = bool(pitch or yaw)
    if moving:
        robot.goto_target(head=target, duration=move_seconds, body_yaw=None)
    else:
        time.sleep(move_seconds)
    data["observed_pose"] = json.dumps(robot.get_current_head_pose().tolist())
    time.sleep(hold_seconds)
    require_ready(get_status())
    if moving:
        robot.goto_target(head=baseline, duration=move_seconds, body_yaw=None)
    else:
        time.sleep(move_seconds)
    data["return_pose"] = json.dumps(robot.get_current_head_pose().tolist())
    return data


def write_log(path, row):
    path.parent.mkdir(parents=True, exist_ok=True)
    header = not path.exists()
    with path.open("a", newline="", encoding="utf-8-sig") as stream:
        writer = csv.DictWriter(stream, fieldnames=FIELDS)
        if header:
            writer.writeheader()
        writer.writerow(row)


def run_menu(robot, args):
    mode = "preview" if args.preview else "robot"
    stamp = datetime.now().strftime("%Y%m%d_%H%M%S_%f")
    log_path = ROOT / "logs" / f"motion_{mode}_{stamp}.csv"
    print(f"Mode: {mode}\nLog after first trial: {log_path}")
    while True:
        print("\n1 Still | 2 Pitch+ | 3 Pitch- | 4 Yaw+ | 5 Yaw- | q Quit")
        choice = input("Choose: ").strip().lower()
        if choice == "q":
            return
        if choice not in CASES:
            continue
        name, pitch_sign, yaw_sign = CASES[choice]
        pitch, yaw = pitch_sign * args.angle, yaw_sign * args.angle
        print(f"{name}: pitch={pitch}, yaw={yaw}, move={args.move}s, hold={args.hold}s, return.")
        if input("Press Enter to execute; type anything to cancel: "):
            continue
        row = dict.fromkeys(FIELDS, "")
        row.update(
            timestamp=datetime.now().astimezone().isoformat(timespec="milliseconds"),
            trial_id=datetime.now().strftime("%Y%m%d_%H%M%S_%f"), mode=mode,
            case=name, pitch_delta_deg=pitch, yaw_delta_deg=yaw,
            move_seconds=args.move, hold_seconds=args.hold,
        )
        start = time.perf_counter()
        try:
            if args.preview:
                row["status"] = "preview_only"
            else:
                row.update(execute_trial(robot, pitch, yaw, args.move, args.hold))
                row["status"] = "sequence_completed"
        except (Exception, KeyboardInterrupt) as error:
            row["status"] = "interrupted" if isinstance(error, KeyboardInterrupt) else "failed"
            row["error"] = f"{type(error).__name__}: {error}"
        row["elapsed_seconds"] = round(time.perf_counter() - start, 4)
        if row["status"] not in ("failed", "interrupted"):
            try:
                row["memo"] = input("Observation (optional): ")
            except (KeyboardInterrupt, EOFError):
                write_log(log_path, row)
                return
        write_log(log_path, row)
        print(f"Saved: {row['status']} {row['error']}")
        if row["status"] in ("failed", "interrupted"):
            print("Stopped. No recovery motion was queued. Inspect robot and logs.")
            return


def main():
    parser = argparse.ArgumentParser(description=__doc__)
    mode = parser.add_mutually_exclusive_group()
    mode.add_argument("--robot", action="store_true", help="Allow manual real-robot trials")
    mode.add_argument("--check", action="store_true", help="Read daemon status only; no SDK connection or motion")
    parser.add_argument("--angle", type=float, default=5.0, help="Relative angle, 1 to 10 degrees")
    parser.add_argument("--move", type=float, default=1.5, help="Each outward/return motion, 1 to 5 seconds")
    parser.add_argument("--hold", type=float, default=1.0, help="Hold time, 0 to 10 seconds")
    args = parser.parse_args()
    for flag, value, low, high in (("angle", args.angle, 1, 10), ("move", args.move, 1, 5), ("hold", args.hold, 0, 10)):
        if not math.isfinite(value) or not low <= value <= high:
            parser.error(f"--{flag} must be between {low} and {high}")
    if args.check:
        print(json.dumps(get_status(), ensure_ascii=True, indent=2))
        return
    args.preview = not args.robot
    if args.preview:
        print("Offline preview: no connection and no movement.")
        run_menu(None, args)
        return
    require_ready(get_status())
    print("Stop Conversation, tracking, and Expression playback. Keep Control connected.")
    if input("Type READY when the robot is awake, near neutral, and idle: ").strip() != "READY":
        return
    from reachy_mini import ReachyMini

    with ReachyMini(connection_mode="localhost_only", spawn_daemon=False, media_backend="no_media") as robot:
        run_menu(robot, args)


if __name__ == "__main__":
    try:
        main()
    except (KeyboardInterrupt, EOFError):
        print("\nStopped.")
    except Exception as error:
        print(f"Stopped: {error}")
        raise SystemExit(1)
