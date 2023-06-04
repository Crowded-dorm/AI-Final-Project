import argparse
import os
import subprocess
import json
import sys
from pathlib import Path

from concurrent import futures


if __name__ == "__main__":
    parser = argparse.ArgumentParser()
    parser.add_argument("-o", "--out_root", default='./custom_dataset/videos')
    parser.add_argument("--vid_root", default="./custom_dataset/videos")
    parser.add_argument("--specs", default="./custom_dataset/panda.json")
    args = parser.parse_args()
        
    vid_root = args.vid_root
    with open(args.specs, "r") as f:
        time_specs = json.load(f)

    try:
        assert(len(time_specs.keys()) == 1)
    except:
        raise "You can only process one video in a single time."
    
    seq = list(time_specs.keys())[0]
    parent_root = Path(vid_root).parent.absolute()
    img_root = os.path.join(args.out_root, 'PNGImages')
    os.makedirs(img_root, exist_ok=True)

    with futures.ProcessPoolExecutor(max_workers=4) as ex:
        if seq not in time_specs:
            print(f"{seq} not specified")

        vid_path = "{}/{}.mp4".format(vid_root, seq)
        if not os.path.isfile(vid_path):
            print(vid_path, "does not exist!")

        spec = time_specs[seq]
        cmd = "python deformable_sprites/scripts/extract_frames.py {} {} --start {} --end {} --fps {}".format(
            vid_path, img_root, spec["start"], spec["end"], spec["fps"]
        )
        print(cmd)
        ex.submit(subprocess.call, cmd, shell=True)
