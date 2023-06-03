import os
import subprocess
import multiprocessing as mp
from concurrent import futures

import argparse
from deformable_sprites.scripts import *

def run(gpus, config, out_dir, motion_sculpture):
    cur_proc = mp.current_process()
    print("PROCESS", cur_proc.name, cur_proc._identity)
    gpus_str = " ".join(gpus)
    cmds = [
        (
            f"python deformable_sprites/scripts/dataset_extract.py"
        ),
        (
            f"python deformable_sprites/scripts/dataset_raft.py --gpus {gpus_str}"
        ),
        (
            f"python deformable_sprites/scripts/run_opt.py"
        )
    ]
    cmds2 = [
        (
            f"python motion_sculpture.py -d custom_dataset -c {config} -o {out_dir}/motion_sculpture"
        ),
        (
            f"python mergetoGIF.py -i {out_dir}"
        )
    ]
    if motion_sculpture:
        cmds.extend(cmds2)
    for cmd in cmds:
        print(cmd)
        subprocess.call(cmd, shell=True)


def main(args):
    os.makedirs(args.output, exist_ok=True)
    with futures.ProcessPoolExecutor(max_workers=len(args.gpus)) as exe:
        exe.submit(
            run,
            args.gpus,
            args.config,
            args.output,
            args.m
        )


if __name__ == '__main__':
    parser = argparse.ArgumentParser()
    parser.add_argument('-c', '--config', default='custom_dataset/custom.json')
    parser.add_argument('-o', '--output', default='custom_dataset/results')
    parser.add_argument('-m', action="store_true", help="use motion sculpture")
    parser.add_argument('--gpus', nargs='*', default=['0'])
    args = parser.parse_args()
    
    main(args)