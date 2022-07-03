#!/bin/bash
MARKDOWN_DIR=$HOME'/Library/Mobile Documents/iCloud~md~obsidian/Documents/Life Lessons/'
INC_THINK_DIR="$HOME/Dropbox/Projects/Programming/Git/incremental-thinking/"
SYNC_SH_SCRIPT=$HOME/Dropbox/Projects/Programming/Git/Bear-Markdown-Export-master/update_bear_markdown.sh

$SYNC_SH_SCRIPT

cd $INC_THINK_DIR
source .venv/bin/activate
python application/main.py -r $MARKDOWN_DIR

$SYNC_SH_SCRIPT