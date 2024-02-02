# Chironata
This repository presents an attempt to build Chironata, a large, multilingual dataset, aligned at the sentence level, using a neural pipeline. The latter is presented in this [paper](https://ceur-ws.org/Vol-3558/paper6193.pdf) and [repository](https://github.com/caro28/chiron) and consists of a sentence embedding model (LaBSE) and a sentence alignment model (Vecalign).

The homepage of this repository adapts this pipeline to run on directories of source texts and their translations.

## Pipeline files
* runner.py
** book-stream.py
* clean_par.py
* segment_sents.py
* overlap.py
* run_vecalign_on_dir.py

## Evaluation files
* score_all.py

## 
