# Chironata
This repository presents an attempt to build Chironata, a large, multilingual dataset, aligned at the sentence level, using a neural pipeline. The latter is presented in this [paper](https://ceur-ws.org/Vol-3558/paper6193.pdf) and [repository](https://github.com/caro28/chiron) and consists of a sentence embedding model (LaBSE) and a sentence alignment model (Vecalign).

The homepage of this repository adapts this pipeline to run on directories of source texts and their translations.

# Pipeline files
## Data processing files
* runner.py
  * book-stream.py
  * clean_par.py
  * segment_sents.py
  * overlap.py
  * run_labse.py

## Run Vecalign's algorithm
* run_vecalign_on_dir.py

## Other files
* get_source_txt_json.py
* build_lookup_table.py
* run_labse_on_dir.py

# Evaluation (with ground-truth sentence alignments)
* score_all.py

# Results
