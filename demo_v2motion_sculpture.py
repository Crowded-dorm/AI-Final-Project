import os
import subprocess
import multiprocessing as mp
from concurrent import futures
import json
import shutil

import argparse
from deformable_sprites.scripts import *

def run(gpus, config, out_root, motion_sculpture):
    cur_proc = mp.current_process()
    print("PROCESS", cur_proc.name, cur_proc._identity)
    gpus_str = " ".join(gpus)
    with open(config, "r") as f:
        time_specs = json.load(f)
    seq = list(time_specs.keys())[0]
    seq_root = os.path.join('outputs', seq)
    shutil.rmtree(seq_root, ignore_errors=True)
    os.makedirs(seq_root)
    if motion_sculpture and out_root == None:
        seq_root = os.path.join('outputs', seq)
        out_root = os.path.join(seq_root, 'motion_sculpture')
        os.makedirs(out_root)
    cmds = [
        (
            f"python deformable_sprites/scripts/dataset_extract.py --specs {config}"
        ),
        (
            f"python deformable_sprites/scripts/dataset_raft.py --gpus {gpus_str}"
        ),
        (
            f"python deformable_sprites/scripts/run_opt.py data=custom data.seq={seq} model.use_tex=False"
        )
    ]
    cmds2 = [
        (
            f"python motion_sculpture.py -c {config} -o {out_root}"
        ),
        (
            f"python mergetoGIF.py -m {out_root} -c {config}"
        )
    ]
    if motion_sculpture:
        cmds.extend(cmds2)
    for cmd in cmds:
        print(cmd)
        subprocess.call(cmd, shell=True)


def main(args):
    with futures.ProcessPoolExecutor(max_workers=len(args.gpus)) as exe:
        exe.submit(
            run,
            args.gpus,
            args.config,
            args.out_root,
            args.m
        )


if __name__ == '__main__':
    parser = argparse.ArgumentParser()
    parser.add_argument('-c', '--config', default='custom_dataset/panda.json')
    parser.add_argument('-o', '--out_root', default=None)
    parser.add_argument('-m', action="store_true", help="use motion sculpture")
    parser.add_argument('--gpus', nargs='*', default=['0'])
    args = parser.parse_args()
    
    main(args)