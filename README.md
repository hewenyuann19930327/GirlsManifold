# GirlsManifold
An attempt to replicate [Towards the Automatic Anime Characters Creation with Generative Adversarial Networks](https://arxiv.org/abs/1708.05509) using PyTorch


## Install

With Conda:

```bash
conda update environment.yml   # set up environment
conda activate girls_manifold  # activate environment
```

## Run

1. Put `erogamescape_sql_output.zip` into `data/`. (The file could be found [here]( https://github.com/makegirlsmoe/makegirlsmoe_web/issues/11#issuecomment-330504682).)
2. Put `lbpcascade_animeface.xml` into `data/`.
3. Run the following:

```bash
# parse sql files to get image URLs
./scripts/preprocess_sql.sh
# crawl faces via Scrapy
./scripts/crawl_faces.sh
# detect and crop faces
./scripts/process_faces.sh
# get labels of faces via illustration2vec
./scripts/get_face_labels.sh
```
