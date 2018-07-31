#!/bin/bash
python -m girls_manifold.scripts.create_dataset \
  --input-dir data/detected_faces \
  --label-dir data/detected_faces_labels \
  --tags-file configs/tags.yaml \
  --output-dir parsed_data/girls
