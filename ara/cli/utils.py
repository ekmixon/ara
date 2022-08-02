# Copyright (c) 2020 The ARA Records Ansible authors
# GNU General Public License v3.0+ (see COPYING or https://www.gnu.org/licenses/gpl-3.0.txt)

import functools
import os
from datetime import datetime, timedelta


@functools.lru_cache(maxsize=10)
def get_playbook(client, playbook_id):
    return client.get(f"/api/v1/playbooks/{playbook_id}")


@functools.lru_cache(maxsize=10)
def get_play(client, play_id):
    return client.get(f"/api/v1/plays/{play_id}")


@functools.lru_cache(maxsize=10)
def get_task(client, task_id):
    return client.get(f"/api/v1/tasks/{task_id}")


@functools.lru_cache(maxsize=10)
def get_host(client, host_id):
    return client.get(f"/api/v1/hosts/{host_id}")


def parse_timedelta(string, pattern="%H:%M:%S.%f"):
    """ Parses a timedelta string back into a timedelta object """
    parsed = datetime.strptime(string, pattern)
    # fmt: off
    return timedelta(
        hours=parsed.hour,
        minutes=parsed.minute,
        seconds=parsed.second,
        microseconds=parsed.microsecond
    )
    # fmt: on


def sum_timedelta(first, second):
    """
    Returns the sum of two timedeltas as provided by the API, for example:
    00:00:02.031557 + 00:00:04.782581 = ?
    """
    first = parse_timedelta(first)
    second = parse_timedelta(second)
    return str(first + second)


def avg_timedelta(timedelta, count):
    """ Returns an average timedelta based on the amount of occurrences """
    timedelta = parse_timedelta(timedelta)
    return str(timedelta / count)


# Also see: ui.templatetags.truncatepath
def truncatepath(path, count):
    """
    Truncates a path to less than 'count' characters.
    Paths are truncated on path separators.
    We prepend an ellipsis when we return a truncated path.
    """
    try:
        length = int(count)
    except ValueError:
        return path

    # Return immediately if there's nothing to truncate
    if len(path) < length:
        return path

    dirname, basename = os.path.split(path)
    while dirname and len(dirname) + len(basename) >= length:
        dirlist = dirname.split("/")
        dirlist.pop(0)
        dirname = "/".join(dirlist)

    return f"...{os.path.join(dirname, basename)}"
