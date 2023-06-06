import glob
import imageio
import cv2
import json
import os
import argparse

def isimage(path):
    ext = os.path.splitext(path)[-1].lower()
    return ext == ".png" or ext == ".jpg" or ext == ".jpeg"

def main(motion_sculpture_root, config, fps):
    with open(config, 'r') as f:
        time_specs = json.load(f)
    seqs = list(time_specs.keys())
    for seq in seqs:
        spec = time_specs[seq]
        seq_root = os.path.join('outputs', seq)
        motion_sculpture_root = os.path.join(seq_root, 'motion_sculpture')
        print("Store motion-sculpture-effect video to:", motion_sculpture_root)
        if fps == None:
            fps = spec["fps"]
        img_paths = sorted(list(filter(isimage, glob.glob(f"{motion_sculpture_root}/*"))))
        frames = [cv2.imread(im)[...,::-1] for im in img_paths]
        imageio.mimsave(f'{motion_sculpture_root}/result.gif', frames, duration=len(frames)/fps)

if __name__ == '__main__':
    parser = argparse.ArgumentParser()
    parser.add_argument('-m', '--motion_sculpture_root', default=None, help='motion sculpture directory')
    parser.add_argument('-c', '--config', default='custom_dataset/panda.json', help='config file')
    parser.add_argument('-f', '--fps', default=None, help='set fps')
    args = parser.parse_args()
    
    main(args.motion_sculpture_root, args.config, args.fps)
