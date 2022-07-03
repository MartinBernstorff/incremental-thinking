import re
import urllib.parse
import webbrowser


def create_bear_url(filepath):
    with open(filepath, "r", encoding="utf8") as f:
        content = f.read()
        file_title = re.findall(r"# .*", content)[0][2:].strip()

        bear_base = "bear://x-callback-url/open-note?title="

        return bear_base + file_title + "&show_window=yes&new_window=yes&edit=yes"


def create_obsidian_url(filepath):
    obsidian_base = "obsidian://open?path="

    uri = urllib.parse.quote(filepath, safe="")

    return obsidian_base + uri


def open_in_obsidian(filepath):
    url = create_obsidian_url(filepath)

    webbrowser.open(url)


def open_in_bear(file_path):
    url = create_bear_url(file_path)

    webbrowser.open(url)
