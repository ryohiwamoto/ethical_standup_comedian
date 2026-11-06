"""Offline checks: no physical robot is connected or moved."""

from pathlib import Path
import tempfile
import unittest
from unittest.mock import patch

import reachy_motion_controller as controller


class MotionControllerTests(unittest.TestCase):
    def test_motion_returns_to_baseline_without_turning_body(self):
        import numpy as np

        class FakeRobot:
            def __init__(self):
                self.pose = np.eye(4)
                self.calls = []

            def get_current_head_pose(self):
                return self.pose.copy()

            def goto_target(self, **kwargs):
                self.calls.append(kwargs)
                self.pose = kwargs["head"].copy()

        robot = FakeRobot()
        angle = np.deg2rad(5)
        cosine, sine = np.cos(angle), np.sin(angle)
        relative_pose = np.array([
            [cosine, -sine, 0, 0],
            [sine, cosine, 0, 0],
            [0, 0, 1, 0],
            [0, 0, 0, 1],
        ])
        ready = {"state": "running", "backend_status": {"ready": True, "motor_control_mode": "enabled"}}
        with patch.object(controller, "get_status", return_value=ready), \
             patch.object(controller, "create_relative_head_pose", return_value=relative_pose) as create_pose, \
             patch.object(controller.time, "sleep"):
            data = controller.execute_trial(robot, 0, 5, 1.5, 1)
        create_pose.assert_called_once_with(0, 5)
        self.assertEqual(len(robot.calls), 2)
        self.assertTrue(all(call["body_yaw"] is None for call in robot.calls))
        np.testing.assert_allclose(robot.calls[0]["head"], relative_pose)
        np.testing.assert_allclose(robot.pose, np.eye(4))
        self.assertNotEqual(data["target_pose"], data["baseline_pose"])

    def test_fault_does_not_queue_return_motion(self):
        import numpy as np

        robot = unittest.mock.Mock()
        robot.get_current_head_pose.return_value = np.eye(4)
        robot.goto_target.side_effect = RuntimeError("motion rejected")
        ready = {"state": "running", "backend_status": {"ready": True, "motor_control_mode": "enabled"}}
        with patch.object(controller, "get_status", return_value=ready), \
             patch.object(controller, "create_relative_head_pose", return_value=np.eye(4)):
            with self.assertRaisesRegex(RuntimeError, "motion rejected"):
                controller.execute_trial(robot, 5, 0, 1.5, 1)
        self.assertEqual(robot.goto_target.call_count, 1)

    def test_rejects_disabled_motors_and_backend_errors(self):
        for backend in ({"ready": True, "motor_control_mode": "disabled"},
                        {"ready": True, "motor_control_mode": "enabled", "error": "fault"}):
            with self.assertRaises(RuntimeError):
                controller.require_ready({"state": "running", "backend_status": backend})

    def test_preview_does_not_contact_daemon_and_logs_one_trial(self):
        with tempfile.TemporaryDirectory() as folder:
            with patch.object(controller, "ROOT", Path(folder)), \
                 patch.object(controller, "get_status", side_effect=AssertionError("Network accessed")), \
                 patch("sys.argv", ["controller"]), \
                 patch("builtins.input", side_effect=["2", "", "looks fine", "q"]):
                controller.main()
            import csv
            with next((Path(folder) / "logs").glob("*.csv")).open(encoding="utf-8-sig", newline="") as stream:
                rows = list(csv.DictReader(stream))
            self.assertEqual(len(rows), 1)
            self.assertEqual(rows[0]["status"], "preview_only")
            self.assertEqual(rows[0]["memo"], "looks fine")

    def test_status_check_never_enters_motion_menu(self):
        with patch("sys.argv", ["controller", "--check"]), \
             patch.object(controller, "get_status", return_value={"state": "running"}), \
             patch.object(controller, "run_menu", side_effect=AssertionError("Motion menu opened")):
            controller.main()

    def test_invalid_numeric_arguments_are_rejected(self):
        for value in ("nan", "inf", "0", "11"):
            with patch("sys.argv", ["controller", "--angle", value]):
                with self.assertRaises(SystemExit) as result:
                    controller.main()
                self.assertEqual(result.exception.code, 2)


if __name__ == "__main__":
    unittest.main()
