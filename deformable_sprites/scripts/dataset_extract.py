import argparse
import os
import subprocess
import json
import sys
from pathlib import Path

from concurrent import futures


if __name__ == "__main__":
    parser = argparse.ArgumentParser()
    parser.add_argument("--seqs", default=None, nargs="*")
    parser.add_argument("--vid_root", default="./custom_dataset/videos")
    parser.add_argument("--specs", default="./custom_dataset/custom.json")
    args = parser.parse_args()

    vid_root = args.vid_root
    parent_root = Path(vid_root).parent.absolute()
    out_root = os.path.join(parent_root, "PNGImages")
    os.makedirs(out_root, exist_ok=True)
    with open(args.specs, "r") as f:
        time_specs = json.load(f)

    if args.seqs is None:
        args.seqs = time_specs.keys()

    with futures.ProcessPoolExecutor(max_workers=4) as ex:
        for seq in args.seqs:
            if seq not in time_specs:
                print(f"{seq} not specified")
                continue

            vid_path = "{}/{}.mp4".format(vid_root, seq)
            if not os.path.isfile(vid_path):
                print(vid_path, "does not exist!")
                continue

            spec = time_specs[seq]
            cmd = "python deformable_sprites/scripts/extract_frames.py {} {} --start {} --end {} --fps {}".format(
                vid_path, out_root, spec["start"], spec["end"], spec["fps"]
            )
            print(cmd)
            ex.submit(subprocess.call, cmd, shell=True)
