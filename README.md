# Chironata
This repository presents an attempt to build Chironata, a large, multilingual dataset, aligned at the sentence level, using a neural pipeline. The latter is presented in this [paper](https://ceur-ws.org/Vol-3558/paper6193.pdf) and [repository](https://github.com/caro28/chiron) and consists of a sentence embedding model (LaBSE) and a sentence alignment model (Vecalign).

The homepage of this repository adapts this pipeline to run on directories of source texts and their translations.

# Pipeline steps
## Extract and transform texts
Data processing pipeline: runner.py

This file performs the following steps by calling other python files in this repository, listed below.

1. Extract _translations_ from XML files, suppressing paratext, then post-process the output
* book-stream.py: Extract from XML, write to .par
* clean_par.py: Reconstitute paragraphs split by paratext, write to .txt

2. Segment into sentences
* segment_sents.py: Segment using Stanza (if lang supported), then split further on periods, colons, semi-colons, and write to .sents

3. Build "overlaps" files required by Vecalign
* overlap.py: Build concatenations of up to 10 consecutive sentences, write to .overlaps

4. Embed "overlaps" with LaBSE
* run_labse.py: Embed each line in .overlaps file, write to .emb (binary file)

### Note: Extracting source texts (Latin or Ancient Greek)
Texts and metadata downloaded using Perseus's API and saved in JSONL files can be processed with get_source_txt_json.py

get_source_txt_json.py assumes that each JSON oject has the following keys:
* id (str): CTS URN
* text (str): full text, with a single newline separating Perseus sections
* locs (list of dicts): metadata per Perseus section
    * locs keys: "loc", "start" (starting character index), "length"

## Run Vecalign on embedded texts
* run_vecalign_on_dir.py

## Other files
* 
* build_lookup_table.py
* run_labse_on_dir.py

# Evaluation (with ground-truth sentence alignments)
* score_all.py

# Results
