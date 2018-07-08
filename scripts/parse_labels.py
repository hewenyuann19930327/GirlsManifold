import argparse
import os
import json

import tqdm
from PIL import Image

import i2v

illust2vec = i2v.make_i2v_with_chainer('illust2vec_tag_ver200.caffemodel',
                                       'tag_list.json')


def start_parse_labels(input_dir, output_dir):
    os.makedirs(output_dir, exist_ok=True)
    for name in tqdm.tqdm(os.listdir(input_dir)):
        image_path = os.path.join(input_dir, name)
        output_path = os.path.join(output_dir, name + '.json')

        img = Image.open(image_path)
        img_info = illust2vec.estimate_plausible_tags(
            [img], threshold=0.0)[0]['general']
        with open(output_path, 'w') as outfile:
            json.dump(img_info, outfile)


def main():
    start_parse_labels(**vars(parse_args()))


def parse_args():
    parser = argparse.ArgumentParser()
    parser.add_argument('--input-dir', required=True)
    parser.add_argument('--output-dir', required=True)
    return parser.parse_args()


if __name__ == '__main__':
    main()
