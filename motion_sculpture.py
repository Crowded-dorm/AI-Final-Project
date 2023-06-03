import os
import glob
import imageio

import numpy as np
import torch
import torch.nn.functional as F
import torchvision.transforms.functional as TF

import sys
import json

sys.path.append(os.path.abspath("__file__/../.."))
from PIL import Image
import cv2

def propagate_edits(dataset_dir, config, out_dir):
    mask_dir = find_mask_dir(dataset_dir)
    img_dir = find_img_dir(dataset_dir, config)
    masks, imgs = load_components(mask_dir, img_dir)

    if out_dir == None:
        out_dir = os.path.join(dataset_dir, 'results/motion_sculpture')
    os.makedirs(out_dir, exist_ok=True)

    #N, M, h, w, _ = coords.shape
    M = 2
    N, _, H, W = imgs.shape
    pre = Image.new('RGBA', (W,H), (0,0,0,0))
    for i in range(N):
        mask = TF.resize(masks[i], (H, W), antialias=True)  # (M, 1, H, W)
        apprs = imgs[i, None].repeat(M, 1, 1, 1)  # (M, 3, H, W)
        
        test = (255*apprs[0]).permute(1, 2, 0).numpy().astype(np.uint8)
        test = cv2.cvtColor(test, cv2.COLOR_BGR2BGRA)
        cpmask = (255*mask[0].permute(1, 2, 0).numpy()).astype(np.uint8)
        test[:,:,3] = cpmask[:,:,0]
        test = Image.fromarray(test)
        
        pre.paste(test, mask=test)
        background = Image.open(f'{img_dir}/{i+1:05d}.png')
        background.paste(pre, mask=pre)
        background.save(f"{out_dir}/{i:05d}.png")
        
def find_mask_dir(dataset_dir):
    log_dir = os.path.join(dataset_dir, 'results')
    mask_dir = sorted(glob.glob(f"{log_dir}/*_masks"))
    return mask_dir[-1]

def find_img_dir(dataset_dir, config):
    base_dir = os.path.join(dataset_dir, 'PNGImages')
    with open(config, 'r') as f:
        time_specs = json.load(f)
    seq = list(time_specs.keys())[0]
    spec = time_specs[seq]
    subdir = "{}_{}-{}_fps{}".format(seq, float(spec["start"]), float(spec["end"]), spec["fps"])
    img_dir = f"{base_dir}/{subdir}"
    print(img_dir)
    return img_dir

def load_components(mask_dir, img_dir):
    imgs = load_imgs(img_dir, -1)  # (1, 3, H, W)
    M = 2
    masks = torch.stack(
        [load_imgs(f"{mask_dir}/masks_{m}", -1) for m in range(M)], dim=1
    )  # (N, M, 1, h, w)
    return masks, imgs


def isimage(path):
    ext = os.path.splitext(path)[-1].lower()
    return ext == ".png" or ext == ".jpg" or ext == ".jpeg"


def load_imgs(img_dir, n_expected=-1):
    img_paths = sorted(list(filter(isimage, glob.glob(f"{img_dir}/*"))))
    if n_expected > 0 and len(img_paths) != n_expected:
        print("found {} matching imgs, need {}".format(len(img_paths), n_expected))
        raise ValueError
    imgs = torch.from_numpy(np.stack([imageio.imread(p) for p in img_paths], axis=0))
    imgs = imgs.reshape(*imgs.shape[:3], -1).float()  # (N, H, W, -1)
    imgs = imgs.permute(0, 3, 1, 2)[:, :3] / 255  # (N, 3, H, W)
    return imgs


if __name__ == "__main__":
    import argparse

    parser = argparse.ArgumentParser()
    parser.add_argument("-d", "--dataset_dir", default='custom_dataset', help="dataset directory")
    parser.add_argument("-c", "--config", default="custom_dataset/custom.json")
    parser.add_argument("-o", "--out_dir", default=None)
    args = parser.parse_args()

    propagate_edits(args.dataset_dir, args.config, args.out_dir)
