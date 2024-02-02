# Chironata
This repository presents an attempt to build Chironata, a large, multilingual dataset, aligned at the sentence level, using a neural pipeline. The latter is presented in this [paper](https://ceur-ws.org/Vol-3558/paper6193.pdf) and [repository](https://github.com/caro28/chiron) and consists of a sentence embedding model (LaBSE) and a sentence alignment model (Vecalign).

The homepage of this repository adapts this pipeline to run on directories of source texts and their translations.

# Pipeline steps
## Extract and transform texts
Data processing pipeline: runner.py

This file performs the following steps:
1. Extract _translations_ from XML files and post-process them (see note below on extracting texts from Perseus)
* book-stream.py
 * Input: xml file from Open Greek and Latin Project
 * Extracts from XML, suppressing paratext where possible
 * Writes output to .par
* clean_par.py
 * Input: .par file
 * Reconstitutes paragraphs split by paratext
 * Writes to output to .txt

2. Segments into sentences
* segment_sents.py
 * Input: .txt
 * Segments supported languages using Stanza, then splits further on periods, colons, semi-colons
 * Writes output to .sents

3. Builds "overlaps" files required by Vecalign
* overlap.py
 * Input: .sents
 * Builds concatenations of up to 10 consecutive sentences
 * Writes output to .overlaps

4. Embeds "overlaps" with LaBSE
* run_labse.py
 * Input: .overlaps
 * Embeds each line in .overlaps file
 * Writes output to binary file, .emb

### Extracting source texts (Latin or Ancient Greek) from Perseus
Texts and metadata downloaded using Perseus's API and saved in JSON files can be processed with get_source_txt_json.py

This file assumes that each JSON oject has the following structure:
- rows: organized by source text; thus each row contains all data for one source text
- columns:
    id (str): CTS URN
    text (str): full text, with a single newline separating Perseus sections
    locs (list of dicts): metadata per Perseus section 
        dict keys: "loc"
                   "start" (starting character index)
                   "length"

## Run Vecalign on embedded texts
* run_vecalign_on_dir.py

## Other files
* 
* build_lookup_table.py
* run_labse_on_dir.py

# Evaluation (with ground-truth sentence alignments)
* score_all.py

# Results
