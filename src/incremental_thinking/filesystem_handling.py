import os
import random
from pathlib import Path


def filepaths_from_dir(path: Path):
    """Walk a directory and produce the records found there, one by one."""
    dir_path = Path(path)
    filepaths = [f for f in dir_path.glob(pattern=r"+.md")]
