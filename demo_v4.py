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
    
    seq_root = [f'custom_dataset/videos/PNGImages/{pattern}*', 
                f'custom_dataset/videos/flow_imgs_gap-1/{pattern}*', 
                f'custom_dataset/videos/flow_imgs_gap1/{pattern}*', 
                f'custom_dataset/videos/raw_flows_gap-1/{pattern}*', 
                f'custom_dataset/videos/raw_flows_gap1/{pattern}*',
                f'outputs/{pattern}*']
    for seq in seq_root:
        shutil.rmtree(seq, ignore_errors=True)
    
    config = f'custom_dataset/{pattern}.json'
    os.makedirs(f'custom_dataset/videos/PNGImages/{pattern}_NO_FILM_0.0-1.0_fps10', exist_ok=True)
    cmds0 = [
        (
            f"cp -r custom_dataset/frames/{pattern}/*.png custom_dataset/videos/PNGImages/{pattern}_NO_FILM_0.0-1.0_fps10"
        ),
        (
            f"python -m frame_interpolation.eval.interpolator_cli --pattern {pattern} \
                    --model_path pretrained_models/film_net/Style/saved_model \
                    --times_to_interpolate {times_to_interpolate} --output_video"  
        ),
        (
            f"python get_configv2.py --pattern {pattern} -t {times_to_interpolate}"
        )
    ]
    for cmd in cmds0:
        print(cmd)
        subprocess.call(cmd, shell=True)
        
    
    config = f'custom_dataset/{pattern}_both.json'
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
            f"python deformable_sprites/scripts/dataset_raft.py --gpus {gpus_str} --seqs {pattern}_NO_FILM {pattern}_FILM"
        ),
        (
            f"python deformable_sprites/scripts/run_opt.py data=custom data.seq={pattern}_NO_FILM model.use_tex=False"
        ),
        (
            f"python deformable_sprites/scripts/run_opt.py data=custom data.seq={pattern}_FILM model.use_tex=False"
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
    parser.add_argument('-t', '--times_to_interpolate', type=int, default=3)
    parser.add_argument('-o', '--out_root', default=None)
    parser.add_argument('-m', action="store_true", help="use motion sculpture")
    parser.add_argument('--gpus', nargs='*', default=['0'])
    args = parser.parse_args()
    
    main(args)