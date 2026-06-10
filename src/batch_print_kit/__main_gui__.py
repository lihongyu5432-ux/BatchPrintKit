import sys
import tempfile
import traceback
from pathlib import Path

from batch_print_kit.gui import main
from batch_print_kit.single_instance import collect_launch_paths


if __name__ == "__main__":
    try:
        should_open, paths = collect_launch_paths(sys.argv[1:])
        if should_open:
            main([str(path) for path in paths])
    except Exception:
        log_path = Path(tempfile.gettempdir()) / "BatchPrintKit-error.log"
        log_path.write_text(traceback.format_exc(), encoding="utf-8")
        raise
