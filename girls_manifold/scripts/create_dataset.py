import argparse
import json
import logging
import math
import os
import sys

import bitarray
import yaml
from tqdm import tqdm

logger = logging.getLogger(__name__)


def mutex_decide(spec, labels):
    maxi_tag, maxi_score = None, 0.0
    for tag, score in labels:
        if tag in spec:
            if score > maxi_score:
                maxi_score = score
                maxi_tag = tag
    if maxi_tag:
        return {maxi_tag: 1.0}
    else:
        return {}


def threshold_decide(spec, labels):
    result_tags = {}
    for tag, score in labels:
        if tag in spec and score > spec[tag]:
            result_tags[tag] = 1.0
    return result_tags


def start_create(tags_file, input_dir, label_dir, output_dir):
    # load tags specification
    with open(tags_file) as infile:
        tags_spec = yaml.load(infile)

    allowed_tags = set(tags_spec['tags'])
    num_tag_bytes = math.ceil(len(allowed_tags) / 8)
    mutex_specs = [
        set(mutex_tags) for mutex_tags in tags_spec['mutex'].values()
    ]
    threshold_spec = tags_spec['threshold']

    # create output_dir
    os.makedirs(output_dir, exist_ok=True)

    data_config = {
        'fields': [
            {
                'name': 'image',
                'type': 'image'
            },
            {
                'name': 'tags',
                'type': 'bitarray',
                'size': len(tags_spec['tags']),
                'fields': tags_spec['tags']
            },
        ],
        'items': []
    }
    total = 0

    with open(os.path.join(output_dir, 'data.bin'), 'wb') as outfile:
        for fname in tqdm(os.listdir(input_dir)):
            label_path = os.path.join(label_dir, fname + '.json')
            image_path = os.path.join(input_dir, fname)

            # extract tags
            tags = {}
            with open(label_path) as infile:
                labels = [(name, score) for name, score in json.load(infile)
                          if name in allowed_tags]
                for mutex_spec in mutex_specs:
                    tags.update(mutex_decide(mutex_spec, labels))
                tags.update(threshold_decide(threshold_spec, labels))

            bits = ''.join(
                ['1' if tag in tags else '0' for tag in tags_spec['tags']])
            bits_arr = bitarray.bitarray(bits)

            # save image
            with open(image_path, 'rb') as infile:
                image_bytes = infile.read()
                num_image_bytes = len(image_bytes)
                outfile.write(image_bytes)
            bits_arr.tofile(outfile)

            data_config['items'].append([num_image_bytes, num_tag_bytes])
            total += 1

    # save config
    data_config['total'] = total
    with open(os.path.join(output_dir, 'config.yaml'), 'w') as outfile:
        yaml.dump(data_config, outfile)


def main():
    args = parse_args()
    start_create(**vars(args))


def parse_args():
    parser = argparse.ArgumentParser()
    parser.add_argument('--tags-file', required=True)
    parser.add_argument('--input-dir', required=True)
    parser.add_argument('--label-dir', required=True)
    parser.add_argument('--output-dir', required=True)
    args = parser.parse_args()
    return args


if __name__ == '__main__':
    main()
