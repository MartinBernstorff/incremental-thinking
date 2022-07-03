#!/usr/bin/env python3
"""Temporary promotions: A script for incrementing promotion tags from markdown
files.

Usage:
    main.py [-r DIR]

Options:
    -r DIR          Recursively visit DIR, accumulating cards from `.md` files.
"""

import curses
import logging
import os
import re
import sys
import webbrowser
from typing import Iterable

from docopt import docopt

from inc.incthink.file_editor_handling import create_obsidian_url, open_in_bear
from inc.incthink.filesystem_handling import filepaths_from_dir
from inc.incthink.logging import my_handler
from inc.incthink.md_file_editors import (
    add_tag_and_write,
    increment_priority,
    remove_tag_and_write,
)
from inc.incthink.utils import convert_prob_to_bool, prob_generator

# Setup logging
logging.basicConfig(
    level=logging.INFO,
    filename="logs/incremental_thinking.log",
    filemode="w",
    format="%(asctime)s %(message)s",
)

# Install exception handler
sys.excepthook = my_handler

CFG = {"version_log": ".mdvlog", "updated_only": False, "checkbox": True}
VERSION = "0.0.1"
VERSION_LOG = {}
STEPS = [1, 1, 7, 28, 360]


def apply_arguments(arguments):
    global CFG
    if arguments.get("-r") is not None:
        CFG["recur_dir"] = arguments.get("-r")
    if arguments.get("-d") is not None:
        CFG["destination"] = arguments.get("-d")


def main_window(win, filepath, number, content):  # noqa
    uid_string = re.findall(r"<!-- {BearID:.+} -->", content)[0]
    uid = re.findall(r"{BearID:.+}", content)[0][8:-1]

    number = int(re.findall(r"#p\d+", content)[0][-1])

    content_string = content.replace(uid_string, "")
    content_string = re.sub(r"<!-- .* -->", "", content_string)

    win.nodelay(False)
    key = ""
    win.clear()
    win.scrollok(True)

    win.addstr(content_string.strip() + "\n\n––––––––––––––\n\n")
    win.addstr("[O]pen | [N]ext | [P]rivate | [W]ork | [R]emove tag | [D]elete\n")
    win.addstr("Link: {}".format(create_obsidian_url(filepath)))

    opened = 0

    while 1:
        try:
            key = win.getkey()

            if str(key) == "o":
                open_in_bear(filepath)
                opened += 1
            elif str(key) == "b":
                open_in_bear(filepath)
                opened += 1
            elif str(key) == "n":
                logging.info("Next, opened = {}".format(opened))
                if opened == 0:
                    increment_priority(filepath, number, content)
                return
            elif str(key) == "p":
                add_tag_and_write(filepath, content, "#private")
                return
            elif str(key) == "w":
                add_tag_and_write(filepath, content, "#work")
                return
            elif str(key) == "d":
                if os.path.exists(filepath):
                    os.remove(filepath)
                    url = "bear://x-callback-url/trash?id={}&show_window=no".format(uid)
                    webbrowser.open(url)
                    return
                else:
                    print("Error in filename")

            elif str(key) == "r":
                remove_tag_and_write(filepath, content)
                return
        except Exception as e:
            raise e


def check_priority(filepath, excluded_tags, must_tags):
    with open(filepath, "r", encoding="utf8") as f:
        content = f.read()

        if "#p0" in content.lower():
            logging.info("{} contains #p0".format(filepath))

            for tag in excluded_tags:
                logging.info("Checking {} for excluded_tag {}".format(filepath, tag))
                if tag.lower() in content.lower():
                    logging.info("Skipped {} since it matched {}".format(filepath, tag))
                    return
                else:
                    logging.info(
                        "Didn't skip {} since it didn't match {}".format(filepath, tag),
                    )

            for tag in must_tags:
                logging.info("Checking {} for must_tag {}".format(filepath, tag))
                if tag.lower() not in content.lower():
                    logging.info(
                        "Skipped {} since it didn't match {}".format(filepath, tag),
                    )
                    return
                else:
                    logging.info(
                        "Didn't skip {} since it matched {}".format(filepath, tag),
                    )

            number = int(re.findall(r"#p\d+", content)[0][-1])

            curses.wrapper(main_window, filepath, number, content)
            return
        else:
            logging.info("Skipped {} since it didn't contain #p0".format(filepath))
            return


def process_file(filepath, blacklist_tags: Iterable, whitelist_tags: Iterable):
    with open(filepath, "r", encoding="utf8") as f:
        f_content = f.read()

        p_tag = re.compile(r"#p\d+")

        # Handle tag updating
        if p_tag.search(f_content) is not None:
            p_int = int(re.findall(r"#p\d+", f_content)[0][-1])

            if p_int > len(STEPS):
                f_content = re.sub(r"#p\d+", "", f_content)
                f_content = re.sub(r"#promoted", "", f_content)

                with open(filepath, "w", encoding="utf8") as f:
                    logging.info(
                        "Changed file {} for the {} time".format(filepath, p_int),
                    )
                    print("Changed file {} for the {} time".format(filepath, p_int))
                    f.write(f_content)
            else:
                if convert_prob_to_bool(prob_generator(STEPS[p_int - 1])):
                    curses.wrapper(main_window, filepath, p_int, f_content)


def main():
    """Run the thing."""
    apply_arguments(docopt(__doc__, version=VERSION))
    recur_dir = os.path.abspath(os.path.expanduser(CFG["recur_dir"]))

    logging.info("------ Started new session ------")

    files = filepaths_from_dir(recur_dir)

    for f_path in files:
        process_file(filepath=f_path)


if __name__ == "__main__":
    main()
