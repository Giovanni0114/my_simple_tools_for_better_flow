#!/usr/bin/python3

import subprocess
import json
import os

DEBUG = False

current_filename = os.path.basename(os.getcwd())

cmd = [
    "ssh",
    "-x",
    "gerrit.neo.volvocars.net",
    "gerrit",
    "query",
    "--format=JSON",
    f"project:car-sw/artinfo/{current_filename}/{current_filename}",
    # "project:car-sw/artinfo/dhu-fault-proxy/dhu-fault-proxy",
    "status:open",
]

git_cmd = [
    'git',
    'show'
]

def get_current_change_id():
    result = subprocess.run(
        git_cmd,
        stdout=subprocess.PIPE,
        stderr=subprocess.PIPE,
        text=True,
        check=True,
    )

    for line in result.stdout.splitlines():
        if "Change" in line:
            return line.split(":")[1].strip()

    return "unknown"

def get_gerrit_reviews():
    result = subprocess.run(
        cmd,
        stdout=subprocess.PIPE,
        stderr=subprocess.PIPE,
        text=True,
        check=True,
    )
    changes = []
    stats = None

    for line in result.stdout.splitlines():
        obj = json.loads(line)
        if obj.get("type") == "stats":
            stats = obj
        else:
            changes.append(obj)

    return changes, stats


if __name__ == "__main__":
    changes, stats = get_gerrit_reviews()
    change_id = get_current_change_id()

    print(f"Found {len(changes)} open changes")
    # print(" DEBUG: Stats:", stats)
    # print(f" DEBUG: Change-id: {change_id}")

    for rev in changes:
        print(f"  * {rev['number']}: {rev['subject']} {'[current]' if rev['id'] == change_id else ''}")
        # print(f"    * {rev['id']}")


