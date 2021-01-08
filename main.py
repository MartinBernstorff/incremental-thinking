#!/usr/bin/env python3
"""Temporary promotions: A script for incrementing promotion tags from markdown files

Usage:
    promote.py [-r DIR]

Options:
    -r DIR          Recursively visit DIR, accumulating cards from `.md` files.
    
"""

import logging
import hashlib
import tempfile
import html
import os
import curses
import shutil
import re
import json
import random
import textwrap
from pprint import pprint
from docopt import docopt
from time import sleep
import fileinput
import webbrowser
import urllib.parse
from os import system
import sys
from prompt_toolkit import prompt
from prompt_toolkit.shortcuts import checkboxlist_dialog
from prompt_toolkit.completion import WordCompleter

logging.basicConfig(level = logging.INFO, filename = "my.log")

def my_handler(type, value, tb):
    logging.exception("Uncaught exception: {0}".format(str(value)))

# Install exception handler
sys.excepthook = my_handler

CONFIG = {
            'version_log': '.mdvlog',
            'updated_only': False,
            'checkbox': False
        }
VERSION = "0.0.1"
VERSION_LOG = {}
STEPS = [1, 1, 7, 28, 360]

def prob_generator(number):
    return 1 / (number+0.2)

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

def gen_bear_url(filepath):
    with open(filepath, "r", encoding="utf8") as f:
        content = f.read()
        file_title = re.findall(r'# .*', content)[0][2:].strip()

        bear_base = "bear://x-callback-url/open-note?title="
        
        return bear_base + file_title

def open_in_bear(file_path):
    url = gen_bear_url(file_path)

    webbrowser.open(url)

def next(filepath, number, content):
    number += 1

    if number > len(STEPS):
        content = re.sub(r'#p\d+', "", content)
    else:
        content = re.sub(r'#p\d+', "#p{}".format(str(number)), content)
    
    with open(filepath, "w", encoding="utf8") as f:
        logging.info("Changed file {} for the {} time".format(filepath, number))
        print("Changed file {} for the {} time".format(filepath, number))
        f.write(content)

def add_tag(filepath, content, tag):
    content = content + " " + tag
    
    with open(filepath, "w", encoding="utf8") as f:
        f.write(content)

def main_window(win, filepath, number, content):
    uid = re.findall(r'<!-- {BearID:.+} -->', content)[0]
    number = int(re.findall(r'#p\d+', content)[0][-1])

    content_string = content.replace(uid, "")
    content_string = re.sub(r'<!-- .* -->', "", content_string)
    
    win.nodelay(False)
    key=""
    win.clear()                

    win.addstr(content_string.strip() + "\n\n––––––––––––––\n\n")
    win.addstr("[O]pen | [N]ext | [P]rivate | [W]ork | [R]emove tag | [D]elete\n")
    win.addstr("Link: {}".format(gen_bear_url(filepath)))

    opened = 0

    while 1:          
        try:                 
            key = win.getkey()                     
        
            if str(key) == "o":
                open_in_bear(filepath)
                opened +=1
            elif str(key) == "n":
                win.addstr("Next, opened = {}".format(opened))
                if opened == 0:
                    next(filepath, number, content)
                return
            elif str(key) == "p":
                add_tag(filepath, content, "#private")
                return
            elif str(key) == "w":
                add_tag(filepath, content, "#work")
                return
            elif str(key) == "d":
                if os.path.exists(filepath):
                    os.remove(filepath)
                    return
                else:
                    print("Error in filename")
            elif str(key) == "r":
                remove_tag(filepath, content)
                return
        except Exception as e:
           # No input   
           pass

def remove_tag(filepath, content):
    content = re.sub(r'#p\d+', "", content)
    
    with open(filepath, "w", encoding="utf8") as f:
        logging.info("Changed file {}".format(filepath))
        print("Changed file {}".format(filepath))
        f.write(content)

def check_priority(filepath, excluded_tags):
    with open(filepath, "r", encoding="utf8") as f:
        content = f.read()

        if "#p0" in content.lower():
            logging.info("{} containts #p0")
            for tag in excluded_tags:
                if tag.lower() in content.lower():
                    logging.info("Skipped {} since it matched {}".format(filepath, tag))
                    return

            number = int(re.findall(r'#p\d+', content)[0][-1])

            curses.wrapper(main_window, filepath, number, content)
            return
        else:
            logging.info("Skipped {}".format(filepath))
            return
    
def process_file(filepath, excluded_tags):
    with open(filepath, "r", encoding="utf8") as f:
        content = f.read()

        for tag in excluded_tags:
            if tag.lower() in content.lower():
                logging.info("Skipped {} since it matched {}".format(filepath, tag))
                return

        priority_tag = re.compile(r'#p\d+')

        if priority_tag.search(content) is not None:
            number = int(re.findall(r'#p\d+', content)[0][-1])

            if number > len(STEPS):
                content = re.sub(r'#p\d+', "", content)
                content = re.sub(r'#promoted',"",content)

                with open(filepath, "w", encoding="utf8") as f:
                    logging.info("Changed file {} for the {} time".format(filepath, number))
                    print("Changed file {} for the {} time".format(filepath, number))
                    f.write(content)
            else:
                if decide(prob_generator(STEPS[number-1])):
                    curses.wrapper(main_window, filepath, number, content)
                
            


def files_from_dir(dirname):
    """Walk a directory and produce the records found there, one by one."""
    global VERSION_LOG
    global CONFIG
    
    if CONFIG["checkbox"] == True:
        excluded_tags = []
        checkboxlist_dialog(
            title="Exclude hashtags",
            text="Which hashtags do you want to exclude?",
            values=[
                ("#private", "#private"),
                ("#work", "#work"),
                ("#life", "#life")
            ],
            ok_text="Submit"
        ).run()
    else:
        excluded_tags = ["#private"]

    for parent_dir, _, files in os.walk(dirname):
        random.shuffle(files)
        for fn in files:
            if fn.endswith(".md") or fn.endswith(".markdown"):
                filepath = os.path.join(parent_dir, fn)
                check_priority(filepath, excluded_tags)

        for fn in files:
            if fn.endswith(".md") or fn.endswith(".markdown"):
                filepath = os.path.join(parent_dir, fn)
                process_file(filepath, excluded_tags)

def main():
    """Run the thing."""
    apply_arguments(docopt(__doc__, version=VERSION))

    initial_dir = os.getcwd()
    recur_dir = os.path.abspath(os.path.expanduser(CONFIG['recur_dir']))
    version_log = os.path.abspath(os.path.expanduser(CONFIG['version_log']))

    load_version_log(version_log)

    with tempfile.TemporaryDirectory() as tmpdirname:
        os.chdir(tmpdirname) # genanki is very opinionated about where we are.
        files_from_dir(recur_dir)

        os.chdir(initial_dir)

    json.dump(VERSION_LOG, open(version_log, 'w'))


if __name__ == "__main__":
    main()