from __future__ import annotations

import tempfile
import unittest
from pathlib import Path
from unittest import mock

from batch_print_kit import single_instance


class SingleInstanceTests(unittest.TestCase):
    def test_collect_launch_paths_deduplicates_requests(self) -> None:
        with tempfile.TemporaryDirectory() as temp:
            handoff = Path(temp)
            with mock.patch.object(single_instance, "HANDOFF_DIR", handoff), mock.patch.object(
                single_instance, "LOCK_PATH", handoff / "collector.lock"
            ):
                first = handoff / "a.pdf"
                second = handoff / "b.pdf"
                first.write_text("a", encoding="utf-8")
                second.write_text("b", encoding="utf-8")

                single_instance._write_request([str(first)])
                should_open, paths = single_instance.collect_launch_paths(
                    [str(first), str(second)],
                    wait_seconds=0,
                )

                self.assertTrue(should_open)
                self.assertEqual([path.name for path in paths], ["a.pdf", "b.pdf"])


if __name__ == "__main__":
    unittest.main()
