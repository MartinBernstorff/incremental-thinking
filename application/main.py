#!/usr/bin/env python3
"""Temporary promotions: A script for incrementing promotion tags from markdown
files.

Usage:
    main.py [-r DIR]

Options:
    -r DIR          Recursively visit DIR, accumulating cards from `.md` files.
"""

import argparse
import logging
import os

from wasabi import msg

from inc.incthink.file_processing import process_file
from inc.incthink.filesystem_handling import filepaths_from_dir

# Setup logging
logging.basicConfig(
    level=logging.INFO,
    filename="logs/incremental_thinking.log",
    filemode="w",
    format="%(asctime)s %(message)s",
)


def main(args):
    """Run the thing."""

    recur_dir = os.path.abspath(os.path.expanduser(args.recur_dir))

    msg.info(f"Started new session with {recur_dir}")

    files = filepaths_from_dir(recur_dir, suffix="md")

    for f_path in files:
        process_file(filepath=f_path, write_files=args.write_files)


if __name__ == "__main__":
    parser = argparse.ArgumentParser()
    parser.add_argument(
        "-r",
        help="Recursively visit DIR, processing `.md` files.",
        dest="recur_dir",
    )
    parser.add_argument("--write_files", dest="write_files", action="store_false")
    args = parser.parse_args()

    main(args=args)
