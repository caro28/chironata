#!/usr/bin/env python

'''
This file is a data processing pipeline for source (Latin or Ancient Greek) 
texts obtained from Perseus and their translations collected in XML files by 
the Open Greek and Latin Project. It extracts the texts from their source 
files and transforms them into the required inputs for Vecalign. The pipeline's
steps are as follows:
    Extraction:
        - Source texts: from .txt files (written to .txt from JSON in 
        get_source_txt_json.py)
        - Translations: from .xml files (currently in data/)
    Transformation:
        - Post-processing: for translations only (reconstitute paragraphs after
        extraction from .xml)
        - Sentence segmentation
        - Build "overlaps" files: concatenations of up to 10 consecutive 
        sentences, required by Vecalign)
        - Embed "overlaps" files using LaBSE

If running on a directory of Ancient Greek or Latin texts, then lang = "src"

Spacy models used for Chironata: fr_core_news_sm, en_core_web_sm, it_core_news_sm, de_core_news_sm
'''

import os
import sys
import glob
import subprocess
from tqdm import tqdm


params = {
    'QUEUE':'short',
    'SWORKERS':2,
    'SMEM':10
}

# slurm_run = 'srun --time 1-0 -p {QUEUE} -N 1 -c {SWORKERS} --mem={SMEM}G bash -c "source /home/craig.car/miniconda3/bin/activate; conda activate use_lxml; {command};"'
lxml_cpu = 'srun --time 1-0 --partition=short --nodes=1 --pty --mem=4G --time=00:30:00 /bin/bash -c "source /home/craig.car/miniconda3/bin/activate; conda activate use_lxml; {command};"'
labse_vec_cpu = 'srun --partition=short --nodes=1 --pty --mem=4GB --time=01:00:00 /bin/bash -c "source /home/craig.car/miniconda3/bin/activate; conda activate labse_vec_pipeline; {command};"'
labse_vec_gpu = 'srun --partition=gpu --nodes=1 --pty --gres=gpu:v100-sxm2 --ntasks=1 --mem=4GB --time=01:00:00 /bin/bash -c "source /home/craig.car/miniconda3/bin/activate; conda activate labse_vec_pipeline; {command};"'

src_dir = sys.argv[1]
lang = sys.argv[2]
spacy_model_ = sys.argv[3]

if lang == "src":
    for path in tqdm(glob.iglob(src_dir+"*.txt")):
        prefix = os.path.splitext(path)[0]
        
        # # Step 1: Sentence Segmentation
        if os.path.isfile(prefix+".sents") == False:
            params['command'] = f'./segment_sents.py {path} {lang}'
            print(f'started a run on file {prefix}')
            subprocess.run(labse_vec_gpu.format(**params),shell=True,check=True)
        
        # # Step 2: Overlap builder
        if os.path.isfile(prefix+".overlaps") == False:
            params['command'] = f'./overlap.py {prefix+".sents"}'
            print("building overlaps")
            subprocess.run(labse_vec_cpu.format(**params), shell=True,check=True)
        
        # # Step 3: Embedder
        if os.path.isfile(prefix+".emb") == False:
            params['command'] = f'./run_labse.py {prefix+".overlaps"}'
            print('labse run')
            subprocess.run(labse_vec_gpu.format(**params), shell=True,check=True)

else:
    for path in tqdm(glob.iglob(src_dir+"*.xml")):
        prefix = os.path.splitext(path)[0]

        # Step 1: Extract from XML
        if os.path.isfile(prefix+".par") == False:
            params['command'] = f'./book-stream.py {path}'
            print(f"starting on new file {prefix}")
            subprocess.run(lxml_cpu.format(**params),shell=True,check=True)

        # Step 2: Clean XML output
        if os.path.isfile(prefix+".txt") == False:
            params['command'] = f'./clean_par.py {prefix+".par"} {spacy_model_} {lang}'
            print("cleaning pars")
            subprocess.run(lxml_cpu.format(**params),shell=True,check=True)

        # Step 3: Sentence Segmentation
        if os.path.isfile(prefix+".sents") == False:
            params['command'] = f'./segment_sents.py {prefix+".txt"} {lang}'
            print("splitting sents")
            subprocess.run(labse_vec_gpu.format(**params),shell=True,check=True)

        # Step 2: Overlap builder
        if os.path.isfile(prefix+".overlaps") == False:
            params['command'] = f'./overlap.py {prefix+".sents"}'
            print("building overlaps")
            subprocess.run(labse_vec_cpu.format(**params), shell=True,check=True)
        
        #Step 3: Embedder
        if os.path.isfile(prefix+".emb") == False:
            params['command'] = f'./run_labse.py {prefix+".overlaps"}'
            print('labse run')
            subprocess.run(labse_vec_gpu.format(**params), shell=True,check=True)`



