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
    NO_FILM = f"{pattern}_NO_FILM"
    FILM = f"{pattern}_FILM"
    
    d = dict()
    d[NO_FILM] = dict()
    d[NO_FILM]['start'] = 0
    #d[NO_FILM]['end'] = frame_num//30 + 1
    d[NO_FILM]['end'] = 1
    d[NO_FILM]['fps'] = 10
    d[NO_FILM]['times_to_interpolate'] = 0
    d[NO_FILM]['img_num'] = img_num
    d[FILM] = dict()
    d[FILM]['start'] = 0
    #d[FILM]['end'] = frame_num//30 + 1
    d[FILM]['end'] = 1
    d[FILM]['fps'] = 10
    d[FILM]['times_to_interpolate'] = times_to_interpolate
    d[FILM]['img_num'] = img_num
    with open(f'custom_dataset/{pattern}_both.json', 'w') as f:
        json.dump(d, f)
    
    # with open(f'custom_dataset/{pattern}_orig.json', 'w') as f:
    #     json.dump(d2, f)


if __name__ == "__main__":
    
    parser = argparse.ArgumentParser()
    parser.add_argument("-p", "--pattern", default="baby")
    parser.add_argument("-t", "--times_to_interpolate", type=int, default=3)
    args = parser.parse_args()
    
    get_config(args.pattern, args.times_to_interpolate)
    