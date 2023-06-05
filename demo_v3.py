import os
import subprocess
import multiprocessing as mp
from concurrent import futures
import json
import shutil
import math
import argparse
from deformable_sprites.scripts import *

def run(gpus, out_root, motion_sculpture, pattern, times_to_interpolate):
    cur_proc = mp.current_process()
    print("PROCESS", cur_proc.name, cur_proc._identity)
    gpus_str = " ".join(gpus)
    
    frame_num = pow(2, times_to_interpolate)
    cmds0 = [
        (
            f"python -m frame_interpolation.eval.interpolator_cli --pattern {pattern} \
                    --model_path pretrained_models/film_net/Style/saved_model \
                    --times_to_interpolate {times_to_interpolate} --output_video"  
        ),
        (
            f"python get_config.py --pattern {pattern} --frame {frame_num}"
        )
    ]
    for cmd in cmds0:
        print(cmd)
        subprocess.call(cmd, shell=True)
        
    
    config = f'custom_dataset/{pattern}.json'
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
        # (
        #     f"python deformable_sprites/scripts/dataset_extract.py --specs {config}"
        # ),
        (
            f"python deformable_sprites/scripts/dataset_raft.py --gpus {gpus_str}"
        ),
        (
            f"python deformable_sprites/scripts/run_opt.py data=custom data.seq={pattern}"
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
            args.out_root,
            args.m,
            args.pattern,
            args.times_to_interpolate
        )


if __name__ == '__main__':
    parser = argparse.ArgumentParser()
    parser.add_argument('-p', '--pattern', default='baby')
    parser.add_argument('-t', '--times_to_interpolate', default=5)
    parser.add_argument('-o', '--out_root', default=None)
    parser.add_argument('-m', action="store_true", help="use motion sculpture")
    parser.add_argument('--gpus', nargs='*', default=['0'])
    args = parser.parse_args()
    
    main(args)