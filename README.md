# Chironata
This repository presents an attempt to build Chironata, a large, multilingual dataset, aligned at the sentence level, using a neural pipeline. The latter is presented in this [paper](https://ceur-ws.org/Vol-3558/paper6193.pdf) and [repository](https://github.com/caro28/chiron) and consists of a sentence embedding model (LaBSE) and a sentence alignment model (Vecalign).

The homepage of this repository adapts this pipeline to run on directories of source texts and their translations.

# Pipeline steps
## Extract and transform texts
Data processing pipeline: runner.py

This file performs the following steps by calling other python files in this repository, listed below.

Note: source (Latin or Ancient Greek) texts skip the first step below. They enter the data processing pipeline at "2. Segment into sentences."

1. Extract _translations_ from XML files, suppressing paratext, then post-process the output
* book-stream.py: Extract from XML, write to .par
* clean_par.py: Filter out additional paratext by checking language (with Spacy), reconstitute paragraphs split by paratext, and write to .txt

2. Segment into sentences
* segment_sents.py: Segment using Stanza (if lang supported), then split further on periods, colons, semi-colons, and write to .sents

3. Build "overlaps" files required by Vecalign
* overlap.py: Build concatenations of up to 10 consecutive sentences, write to .overlaps

4. Embed "overlaps" with LaBSE
* run_labse.py: Embed each line in .overlaps file, write to .emb (binary file)

### Note: Extracting source texts (Latin or Ancient Greek): get_source_txt_json.py
Texts and metadata downloaded using Perseus's API and saved in JSONL files must be processed separately, using get_source_txt_json.py.

This file assumes that each JSON oject has the following keys:
* id (str): CTS URN
* text (str): full text, with a single newline separating Perseus sections
* locs (list of dicts): metadata per Perseus section
    * locs keys: "loc", "start" (starting character index), "length"

Output: 
* .txt file: full text as continuous string
* .json file: metadata (all locs per text)

## Run Vecalign on embedded texts
run_vecalign_on_dir.py
* Calls Vecalign's algorithm, using vecalign.py, on an input directory.
* Filters for files ending in .emb and assumes these are embeddings of overlaps files (the final output of runner.py)

Required files:
* cts_lookup_table.json: map of CTS URN to available translations
   * To build this table, run: build_lookup_table.py
   * Required input: translations_repositories.csv (currently in data/)

## Other convenience files
* run_labse_on_dir.py: to run LaBSE on a directory of .sents files (and embed by sentence rather than overlap)

# Evaluation (with ground-truth sentence alignments)
score_all.py
* Vecalign's original strict scoring function
* Chiron's new strict scoring function
* Chiron's new lax scoring function

# Results
* Vecalign's raw output: results/alignment_rslts/
* Sentence-aligned texts: results/sentence_aligned_texts

# Pipeline models
1. LaBSE, Feng et al. (2020)
* For embedding sentences, using [Hugging Face implementation](https://huggingface.co/sentence-transformers/LaBSE)
* LaBSE [paper](https://arxiv.org/abs/2007.01852): Feng, F., Yang, Y., Cer, D.M., Arivazhagan, N., & Wang, W. (2020). Language-agnostic BERT Sentence Embedding. *Annual Meeting of the Association for Computational Linguistics.*

2. Vecalign, Thompson (2019)
* For aligning two texts embedded at the sentence level
* Vecalign GitHub: https://github.com/thompsonb/vecalign
* Vecalign [paper](https://aclanthology.org/D19-1136/): Thompson, B. (2019). Vecalign: Improved Sentence Alignment in Linear Time and Space. *Conference on Empirical Methods in Natural Language Processing.*


# Installation
1. To use LaBSE, see instructions on [Hugging Face](https://huggingface.co/sentence-transformers/LaBSE#usage-sentence-transformers)
2. To use Vecalign, see list of dependencies on [Vecalign's GitHub](https://github.com/thompsonb/vecalign#build-vecalign)
3. For sentence segmentation with Stanza, see their [documentation]((https://stanfordnlp.github.io/stanza/tokenize.html))
4. For language detection with Spacy, see this implementation [using FastText and Spacy](https://spacy.io/universe/project/spacy_fastlang)
