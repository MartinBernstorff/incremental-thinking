#!/bin/bash
$HOME/Dropbox/Projects/Programming/Git/Bear-Markdown-Export-master/update_bear_markdown.sh

cd "$HOME/Dropbox/Projects/Programming/Git/incremental-thinking/"

python3 main.py -r $HOME'/Library/Mobile Documents/iCloud~md~obsidian/Documents/Life Lessons/'

$HOME/Dropbox/Projects/Programming/Git/Bear-Markdown-Export-master/update_bear_markdown.sh