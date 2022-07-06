#!/bin/zsh
SCRIPT_DIR=${0:a:h}
UPDATE_BEAR_FILE="/Users/au484925/Dropbox/Projects/Programming/Git/Bear-Markdown-Export-master/update_bear_markdown.sh"
MD_DIR="/Users/au484925/Library/Mobile Documents/iCloud~md~obsidian/Documents/Life Lessons/"

echo "Updating incremental thinking..."

echo "Updating Bear Markdown..."
$UPDATE_BEAR_FILE
echo "Done updating Bear Markdown."

# Run the script
echo "Updating tags..."

cd $SCRIPT_DIR
source .venv/bin/activate
echo $MD_DIR
python application/main.py -r $MD_DIR
deactivate

echo "Done updating tags."

echo "Updating Bear Markdown...."
$UPDATE_BEAR_FILE
echo "Done updating incremental Bear Markdown."