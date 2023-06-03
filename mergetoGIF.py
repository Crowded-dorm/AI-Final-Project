import glob
import imageio
import cv2
import json
import os
import argparse

def isimage(path):
    ext = os.path.splitext(path)[-1].lower()
    return ext == ".png" or ext == ".jpg" or ext == ".jpeg"

def main(input_dir, config):
    img_paths = sorted(list(filter(isimage, glob.glob(f"{input_dir}/*"))))
    frames = [cv2.imread(im)[...,::-1] for im in img_paths]
    with open(config, 'r') as f:
        time_specs = json.load(f)
    seq = list(time_specs.keys())[0]
    spec = time_specs[seq]
    fps = spec["fps"]
    imageio.mimsave(f'{input_dir}/result.gif', frames, duration=1000/fps)

if __name__ == '__main__':
    parser = argparse.ArgumentParser()
    parser.add_argument('-i', '--input', default='custom_dataset/results/motion_sculpture', help='input directory')
    parser.add_argument('-c', '--config', default='custom_dataset/custom.json', help='config file')
    args = parser.parse_args()
    
    main(args.input, args.config)
