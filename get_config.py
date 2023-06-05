import argparse
import json

def get_config(pattern, frame_num):
    d = dict()
    d[pattern] = dict()
    d[pattern]['start'] = 0
    d[pattern]['end'] = int(frame_num)//30+1
    d[pattern]['fps'] = 10
    with open(f'custom_dataset/{pattern}.json', 'w') as f:
        json.dump(d, f)
    


if __name__ == "__main__":
    
    parser = argparse.ArgumentParser()
    parser.add_argument("-p", "--pattern", default="baby")
    parser.add_argument("-f", "--frame_num", default=32)
    args = parser.parse_args()
    
    get_config(args.pattern, args.frame_num)
    