"""Run local-model jobs only while the machine is otherwise idle.

Every chunk (default 25 trials) it measures how many CPU cores *other* processes are using
(total busy time from /proc/stat minus the time used by ollama and this project's runner). If that
exceeds --max-foreign-cores, it waits; otherwise it runs the next chunk. Chunks are resumable runner
invocations, so stopping and restarting this script at any time loses nothing.

  nohup .venv/bin/python -m run.idle_supervisor > logs_supervisor.txt 2>&1 &
"""
import argparse
import os
import subprocess
import sys
import time
from datetime import datetime
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
CLK = os.sysconf("SC_CLK_TCK")

JOBS = [  # (description, runner args); priority order from the approach paper: S1, S2, S3
    ("S1 decisions", ["--bank", "trials", "--tag", "main", "--sub-exp", "S1"]),
    ("S2 decisions", ["--bank", "trials", "--tag", "main", "--sub-exp", "S2"]),
    ("S3 decisions", ["--bank", "trials", "--tag", "main", "--sub-exp", "S3a", "S3b"]),
    ("checks", ["--bank", "checks", "--tag", "checks"]),
]
EXT_JOBS = [
    ("S1 fallback-extension decisions", ["--bank", "trials", "--tag", "main", "--extension-only"]),
    ("fallback-extension checks", ["--bank", "checks", "--tag", "checks", "--extension-only"]),
]


def total_busy():
    f = open("/proc/stat").readline().split()[1:]
    v = list(map(int, f))
    return sum(v) - v[3] - v[4]  # minus idle, iowait


def own_pids():
    pids = []
    for p in Path("/proc").iterdir():
        if not p.name.isdigit():
            continue
        try:
            cmd = (p / "cmdline").read_bytes().replace(b"\0", b" ").decode(errors="ignore")
        except OSError:
            continue
        if "ollama" in cmd or "run.runner" in cmd or "run.idle_supervisor" in cmd:
            pids.append(p.name)
    return pids


def proc_time(pids):
    t = 0
    for pid in pids:
        try:
            s = open(f"/proc/{pid}/stat").read().rsplit(")", 1)[1].split()
            t += int(s[11]) + int(s[12])
        except OSError:
            pass
    return t


def foreign_cores(window=10.0):
    pids = own_pids()
    b0, o0 = total_busy(), proc_time(pids)
    time.sleep(window)
    b1, o1 = total_busy(), proc_time(pids)
    return max(0.0, ((b1 - b0) - (o1 - o0)) / CLK / window)


def main():
    ap = argparse.ArgumentParser()
    ap.add_argument("--chunk", type=int, default=25)
    ap.add_argument("--max-foreign-cores", type=float, default=2.0)
    ap.add_argument("--fallback", action="store_true", help="also run the 5%%/45%% extension cells")
    args = ap.parse_args()
    jobs = JOBS[:1] + (EXT_JOBS[:1] if args.fallback else []) + JOBS[1:] + (EXT_JOBS[1:] if args.fallback else [])
    for name, jargs in jobs:
        while True:
            busy = foreign_cores()
            if busy > args.max_foreign_cores:
                print(f"{datetime.now():%m-%d %H:%M} busy ({busy:.1f} foreign cores) - waiting", flush=True)
                time.sleep(120)
                continue
            r = subprocess.run(["nice", "-n", "10", sys.executable, "-m", "run.runner", "--model", "llama31_8b",
                                *jargs, "--limit", str(args.chunk)], cwd=ROOT, capture_output=True, text=True)
            first = r.stdout.splitlines()[0] if r.stdout else r.stderr[-300:]
            print(f"{datetime.now():%m-%d %H:%M} [{name}] {first}", flush=True)
            if r.returncode != 0:
                print(r.stderr[-1000:], flush=True)
                time.sleep(60)
            if " 0 to run" in r.stdout:
                print(f"{datetime.now():%m-%d %H:%M} [{name}] complete", flush=True)
                break
    print("ALL LOCAL JOBS COMPLETE", flush=True)


if __name__ == "__main__":
    main()
