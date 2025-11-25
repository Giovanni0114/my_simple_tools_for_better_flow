#!/usr/bin/python3

import time
import sys
import argparse
import subprocess
from pathlib import Path


class Size:
    def __init__(self, s: str) -> None:
        if "GB" in s:
            self.size = int(float(s.replace("GB", "").strip()) * 1024 * 1024 )
        elif "MB" in s:
            self.size = int(float(s.replace("MB", "").strip()) * 1024)
        elif "KB" in s:
            self.size = int(float(s.replace("KB", "").strip()))
        elif all(c.isdigit() for c in s):
            self.size = int(s)
        else:
            self.size = 0

    def size(self) -> int:
        return self.size

class Notifier:
    def __init__(self, enable: bool, stalled_threshold: int, repos : list[Path]) -> None:
        self.enable = enable
        self.stalled_threshold = stalled_threshold
        self.stalled_last_id = {p:0 for p in repos}

    def handle(self, repo, stalled):
        if not self.enable:
            return
        self._stalled(repo, stalled)
        self._resumed(repo, stalled)


    def _execute_notify_send(self, summary: str, body: str, last_id = 0, critical = True) -> None:
        cmd = ["notify-send", summary, body, "-p"]
        if last_id != 0:
            cmd += ["-r", f"{last_id}"]

        if critical:
            cmd += ["--urgency=critical"]

        result = subprocess.run(cmd, capture_output=True, text=True)
        if result.returncode != 0:
            print(f" * Failed to execute {cmd[0]} on {path}: {result.stderr}", file=sys.stderr)

        return int(result.stdout.strip())

    def _stalled(self, repo, stalled) -> None:
        if stalled < self.stalled_threshold:
            return

        summary = f"Repository Sync Stalled: {repo.name}"
        body = f"The repository at {repo.name} has not changed size for {stalled} checks."
        self.stalled_last_id[repo] = self._execute_notify_send(summary, body, self.stalled_last_id[repo])

    def _resumed(self, repo, stalled) -> None:
        if stalled != 0 or self.stalled_last_id[repo] == 0:
            return

        summary = f"Repository Sync Resumed: {repo.name}"
        body = f"The repository at {repo.name} has resumed synchronization."
        self._execute_notify_send(summary, body, self.stalled_last_id[repo], False)
        self.stalled_last_id[repo] = 0

def print_red(message: str) -> None:
    print(f"\033[91m{message}\033[0m")

def print_yellow(message: str) -> None:
    print(f"\033[93m{message}\033[0m")

def print_green(message: str) -> None:
    print(f"\033[92m{message}\033[0m")

def clear_console() -> None:
    subprocess.run("clear")

def get_directory_size(path: Path) -> int:
    cmd = ["du", "-s", str(path)]

    result = subprocess.run(cmd, capture_output=True, text=True)
    if result.returncode != 0:
        print(f" * Failed to execute {cmd[0]} on {path}: {result.stderr}", file=sys.stderr)

    size_str = result.stdout.split()[0]
    return int(size_str)

def size_to_human_readable_size(size: int) -> str:
    for unit in ['KB', 'MB', 'GB', 'TB']:
        if size < 1024:
            return f"{size:.2f}{unit}"
        size /= 1024

def sec_to_human_readable(sec: float) -> str:
    if sec < 60:
        return f"{sec:.2f}sec"
    elif sec < 3600:
        minutes = sec / 60
        seconds = sec % 60
        return f"{minutes:.2f}min {seconds:.2f}sec"
    else:
        hours = sec / 3600
        minutes = (sec % 3600) / 60
        return f"{hours:.2f}hr {minutes:.2f}min"

def parse_args() -> argparse.Namespace:
    parser = argparse.ArgumentParser(description="Monitor synchronization status of git folders repositories.")
    parser.add_argument(
        "-r",
        "--repos",
        nargs="+",
        type=Path,
        required=True,
        help="List of repository paths to monitor."
    )

    parser.add_argument(
        "-s",
        "--sizes",
        nargs="+",
        type=Size,
        default=[],
        help="Write desired size of directory, if known, 0 ignored, GB/MB/KB accepted (def KB is assuemmd)"
    )

    parser.add_argument(
        "-i",
        "--interval",
        type=int,
        default=5,
        help="Interval in seconds between synchronization checks. Default is 5 seconds."
    )

    parser.add_argument(
        "--stalled-threshold",
        type=int,
        default=5,
        help="Number of consecutive checks with no size change to consider synchronization stalled. Default is 3."
    )

    parser.add_argument(
        "--notify",
        action="store_true",
        help="Enable desktop notifications for stalled synchronization."
    )

    return parser.parse_args()

if __name__ == "__main__":
    clear_console()

    args = parse_args()

    repos = args.repos
    interval = args.interval

    print(f"Monitoring synchronization status for repositories: {[r.name for r in repos]}")
    print(f"Checking every {interval} seconds.")

    sizes = {p:get_directory_size(p) for p in repos}
    goal_sizes = {a:b for a,b in zip(repos, [p.size for p in args.sizes])}
    stalled = {p:0 for p in repos}
    notifier = Notifier(args.notify, args.stalled_threshold, repos)

    while True:
        sum_time = 0
        for repo in repos:
            size = get_directory_size(repo)
            delta = size - sizes[repo]

            percent = 0

            if delta > 0:
                if repo in goal_sizes and goal_sizes[repo] > 0:
                    goal_size = goal_sizes[repo]
                    percent = (size / goal_size) * 100
                    speed = delta/interval
                    estiamte = "N/A"

                    if speed > 0 and percent < 100:
                        seconds = (goal_size - size) / speed
                        sum_time += seconds
                        estimate = sec_to_human_readable(seconds)

                    if percent >= 100:
                        print_yellow(f"[{repo.name}] reached goal size of {size_to_human_readable_size(goal_size)} but still growing; delta={delta}; speed={speed}KB/s;")
                    else:
                        print(f"[{repo.name}] size={size_to_human_readable_size(size)}({percent:.2f}%); delta={delta}; speed={speed}KB/s; estimate={estimate};")
                else:
                    print(f"[{repo.name}] size={size_to_human_readable_size(size)}; delta={delta}; speed={delta/interval}KB/s;")

                stalled[repo] = 0
                sizes[repo] = size
            else:
                stalled[repo] += 1
                if percent >= 100:
                    print_green(f"[{repo.name}] reached goal size of {size_to_human_readable_size(goal_size)}")
                if stalled[repo] >= args.stalled_threshold:
                    print_red(f"[{repo.name}] stalled for {stalled[repo]} cycles on {size_to_human_readable_size(size)}")
                else:
                    print_yellow(f"[{repo.name}] stalled for {stalled[repo]} cycles on {size_to_human_readable_size(size)}")

            notifier.handle(repo, stalled[repo])

        if len(repos) > 1:
            print("----------------------------")
            print(f"  * SUM estimate time: {sec_to_human_readable(sum_time)}")

        time.sleep(interval)
        clear_console()

