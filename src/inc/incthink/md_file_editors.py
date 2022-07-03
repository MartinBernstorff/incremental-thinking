import logging
import re


def add_tag_and_write(filepath, content, tag):
    content = content + " " + tag

    with open(filepath, "w", encoding="utf8") as f:
        f.write(content)


def remove_tag_and_write(filepath, content):
    content = re.sub(r"#p\d+", "", content)

    with open(filepath, "w", encoding="utf8") as f:
        logging.info("Changed file {}".format(filepath))
        print("Changed file {}".format(filepath))
        f.write(content)


def increment_priority(filepath, number, content):
    number += 1

    if number > len(STEPS):  # noqa
        content = re.sub(r"#p\d+", "", content)
    else:
        content = re.sub(r"#p\d+", "#p{}".format(str(number)), content)

    with open(filepath, "w", encoding="utf8") as f:
        logging.info("Changed file {} for the {} time".format(filepath, number))
        print("Changed file {} for the {} time".format(filepath, number))
        f.write(content)
