import os
import random
from pathlib import Path
from typing import List


def filepaths_from_dir(path: Path, suffix: str = None) -> List:
    """Walk a directory and produce the records found there, one by one."""
    dir_path = Path(path)
    if suffix:
        return [f for f in dir_path.glob(pattern=f"*.{suffix}")]
    else:
        return [f for f in dir_path.glob(pattern=f"*")]
