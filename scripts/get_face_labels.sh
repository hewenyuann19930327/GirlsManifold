#!/bin/bash
./illustration2vec/get_models.sh
cp scripts/parse_labels.py ./illustration2vec
cd ./illustration2vec
python -m parse_labels \
  --input-dir ../data/detected_faces \
  --output-dir ../data/detected_faces_labels
