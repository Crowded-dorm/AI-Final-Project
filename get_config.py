import argparse
import json
import os
import glob

def isimage(path):
    ext = os.path.splitext(path)[-1].lower()
    return ext == ".png" or ext == ".jpg" or ext == ".jpeg"

def get_config(pattern, times_to_interpolate):
    seg_root = os.path.join('custom_dataset/frames', pattern)
    img_num = len(list(filter(isimage, glob.glob(f"{seg_root}/*"))))
    
    frame_num = 2**times_to_interpolate * (img_num-1) + 1
    
    d = dict()
    d[pattern] = dict()
    d[pattern]['start'] = 0
    d[pattern]['end'] = frame_num//30 + 1
    d[pattern]['fps'] = 10
    d[pattern]['times_to_interpolate'] = times_to_interpolate
    d[pattern]['img_num'] = img_num
    with open(f'custom_dataset/{pattern}.json', 'w') as f:
        json.dump(d, f)
    
    # with open(f'custom_dataset/{pattern}_orig.json', 'w') as f:
    #     json.dump(d2, f)


if __name__ == "__main__":
    
    parser = argparse.ArgumentParser()
    parser.add_argument("-p", "--pattern", default="baby")
    parser.add_argument("-t", "--times_to_interpolate", type=int, default=3)
    args = parser.parse_args()
    
    get_config(args.pattern, args.times_to_interpolate)
    