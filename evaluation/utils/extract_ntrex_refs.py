from argparse import ArgumentParser
from pathlib import Path

from utils import load_segments, write_segments

def parse_args():
    parser = ArgumentParser()
    parser.add_argument('--dialect', required=True)

    return parser.parse_args()

def main(args):
    
    assert args.dialect in ["be", "zh"], "dialect needs to be either be or zh"

    dir_path = Path(f'../ntrex-128/raw/references_be_zh/ntrex_gsw_{args.dialect}')
    total_segments = []
    file_paths = list(dir_path.glob('*.txt'))
    for file_path in sorted(file_paths):
        #print(file_path)
        segments = load_segments(file_path)
        total_segments.extend(segments)

    total_segments = [segm for segm in total_segments if segm != '']

    write_segments(f"../ntrex-128/references/en-gsw_{args.dialect}.refA.txt", total_segments)

if __name__ == '__main__':
    args = parse_args()
    main(args)
