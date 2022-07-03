import os
from pathlib import Path

from inc.incthink.filesystem_handling import filepaths_from_dir


def test_paths_from_dir():
    base_path = os.path.abspath(os.curdir)
    path = Path(base_path) / "application"

    results = filepaths_from_dir(path)

    assert len(results) == 3
