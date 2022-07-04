import re
from typing import Dict, Iterable

from inc.incthink.utils import convert_prob_to_bool


def process_file(
    filepath,
    blacklist_tags: Iterable = None,
    whitelist_tags: Iterable = None,
    tag_prefix: str = "#p",
    dry_run=True,
    iteration2intervals: Dict = {
        0: {"inbox_interval": 7, "wait_interval": 0},
        2: {"inbox_interval": 7, "wait_interval": 28},
        1: {"inbox_interval": 7, "wait_interval": 7},
        3: {"inbox_interval": 7, "wait_interval": 165},
        4: {"inbox_interval": 7, "wait_interval": 365},
        5: {"inbox_interval": 7, "wait_interval": 725},
    },
    inbox_tag: str = "#^.inbox",
):
    """Process file.

    Args:
        filepath (str): Path to file.
        blacklist_tags (Iterable, optional): Tags to blacklist. Defaults to None.
        whitelist_tags (Iterable, optional): Tags to whitelist. Defaults to None.
        tag_prefix (str, optional): Tag prefix. Defaults to "p".
        dry_run (bool, optional): Whether to run the function without modifying the file. Defaults to True.

    Raises:
        ValueError
    """

    with open(filepath, "r", encoding="utf8") as f:
        f_content = f.read()

        tag_pattern = re.compile(rf"{tag_prefix}\d+")
        tag_matches = tag_pattern.findall(f_content)

        if len(tag_matches) > 1:
            raise ValueError(f"More than one tag matches {tag_pattern}")
        elif len(tag_matches) == 0:
            raise ValueError(f"No tag matches {tag_pattern}")
        elif len(tag_matches) == 1:
            tag = tag_matches[0]
            iteration = int(tag.replace(tag_prefix, ""))

            if inbox_tag not in f_content:
                f_content = process_in_queue(
                    iteration2intervals=iteration2intervals,
                    inbox_tag=inbox_tag,
                    f_content=f_content,
                    tag=tag,
                    iteration=iteration,
                )
            elif inbox_tag in f_content:
                f_content = process_in_inbox(
                    tag_prefix=tag_prefix,
                    iteration2intervals=iteration2intervals,
                    inbox_tag=inbox_tag,
                    f_content=f_content,
                    tag=tag,
                    iteration=iteration,
                )

            if not dry_run:
                with open(filepath, "w", encoding="utf8") as f:
                    f.write(f_content)
            else:
                return f_content


def process_in_inbox(
    tag_prefix,
    iteration2intervals,
    inbox_tag,
    f_content,
    tag,
    iteration,
):
    demote_prob = 1 / (1 + iteration2intervals[iteration]["wait_interval"])

    if convert_prob_to_bool(demote_prob):
        f_content = f_content.replace(inbox_tag, "")
        f_content = f_content.replace(tag, f"{tag_prefix}{iteration+1}")

    return f_content


def process_in_queue(iteration2intervals, inbox_tag, f_content, tag, iteration):
    promote_prob = 1 / (1 + iteration2intervals[iteration]["wait_interval"])

    if convert_prob_to_bool(promote_prob):
        f_content = f_content.replace(tag, f"{tag} {inbox_tag}")

    return f_content
