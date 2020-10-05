#!/usr/bin/env python3
"""Temporary promotions: A script for incrementing promotion tags from markdown files

Usage:
    promote.py [-r DIR]

Options:
    -r DIR          Recursively visit DIR, accumulating cards from `.md` files.
    
"""

import hashlib
import tempfile
import os
import shutil
import re
import json
import random
from pprint import pprint
from docopt import docopt
import fileinput

CONFIG = {
            'version_log': '.mdvlog',
            'updated_only': False
        }
VERSION = "0.0.1"
VERSION_LOG = {}

def prob_generator(number):
    return 1

def decide(prob):
    return random.random() < prob

def apply_arguments(arguments):
    global CONFIG
    if arguments.get('-r') is not None:
        CONFIG['recur_dir'] = arguments.get('-r')
    if arguments.get('-d') is not None:
        CONFIG['destination'] = arguments.get('-d')

def load_version_log(version_log):
    global VERSION_LOG
    if os.path.exists(version_log):
        VERSION_LOG = json.load(open(version_log, 'r'))

def process_file(filepath):
    with open(filepath, "r", encoding="utf8") as f:
        content = f.read()

        priority_tag = re.compile(r'###### .*')
    
        if priority_tag.search(content) is not None:
            content = re.sub(r'###### .*\n{1}', "", content)

            with open(filepath, "w", encoding="utf8") as f:
                f.write(content)


def files_from_dir(dirname):
    """Walk a directory and produce the records found there, one by one."""
    global VERSION_LOG
    global CONFIG
    for parent_dir, _, files in os.walk(dirname):
        for fn in files:
            if fn.endswith(".md") or fn.endswith(".markdown"):
                filepath = os.path.join(parent_dir, fn)
                process_file(filepath)

def main():
    """Run the thing."""
    apply_arguments(docopt(__doc__, version=VERSION))

    initial_dir = os.getcwd()
    recur_dir = os.path.abspath(os.path.expanduser(CONFIG['recur_dir']))
    version_log = os.path.abspath(os.path.expanduser(CONFIG['version_log']))

    load_version_log(version_log)

    with tempfile.TemporaryDirectory() as tmpdirname:
        os.chdir(tmpdirname) # genanki is very opinionated about where we are.

        file_iterator = files_from_dir(recur_dir)

        os.chdir(initial_dir)

    json.dump(VERSION_LOG, open(version_log, 'w'))


if __name__ == "__main__":
    exit(main())