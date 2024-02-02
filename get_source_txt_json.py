'''
This file extracts source texts (Latin or Ancient Greek texts) stored in json files, obtained 
from Perseus, then writes one text file and json file per source document.

Each input json file (from Perseus) contains the following:
- rows: organized by source text; thus each row contains all data for one source text
- columns:
    id (str): CTS URN
    text (str): full text, with a single newline separating Perseus sections
    locs (list of dicts): metadata per Perseus section 
        dict keys: "loc"
                   "start" (starting character index)
                   "length"

The output files contain the following:
.txt file: full source text as a continuous string, with newline separator 
replaced with one whitespace
.json file: metadata per source text (from "locs" column)
'''

import os
import glob
import json
import argparse
import pandas as pd


def main():
    parser = argparse.ArgumentParser(description="Extract text and metadata from David's Perseus json files.")

    parser.add_argument("-i", type=str, required=True,
                        help="Path to directory with input json files")
    
    parser.add_argument("-o", type=str, required=True,
                        help="Path to save output .txt and .json files")
    
    args = parser.parse_args()
    
    # inside chironata repo, perseus_jsons_path is: data/perseus_jsons
    perseus_jsons_path = args.i
    # currently, these output files are saved in: data/source_sents
    out_path = args.o
    for filepath in glob.iglob(f"{perseus_jsons_path}/*.json"):
        print(f"Processing file: {filepath}")
        with open(filepath) as f:
            for line in f:
                row = json.loads(line)
                with open(os.path.join(out_path, f"{row['id'].rsplit('.',1)[0]}.txt"), "w") as d:
                    d.write(row['text'].replace('\n', ' '))
                with open(os.path.join(out_path, f"{row['id'].rsplit('.',1)[0]}.json"), "w") as m:
                    m.write(json.dumps(row['locs']))
        break

if __name__ == "__main__":
    main()