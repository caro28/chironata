'''
This file builds a dict mapping the CTS URNs of source texts (Latin or Ancient 
Greek) to their translations available in our dataset, then writes the 
dict to JSON.

The output .json has this structure:
    keys: CTS URN, e.g. "urn:cts:greekLit:tlg0001.tlg001"
    values: filenames (basename) of corresponding translations, e.g. [
        'apollonius_1889',
        'tlg0001.tlg001.opp-eng1.xml',
        'apolloniusRhodius_1_1791',
        'apolloniusRhodius_1892'
        ]
'''

import json
import argparse
import pandas as pd


def main():
    parser = argparse.ArgumentParser(
        description="Build look up table mapping CTS URN to corresponding translations")
    parser.add_argument("-transl_path", type=str, required=True,
                        help="Path to translations_repositories.csv")
    parser.add_argument("-o", type=str, required=True,
                        help="Path to save look up table.")
    
    args = parser.parse_args()

    transl_path = args.transl_path
    transl_df = load_transform_csv(transl_path)
    lookup_table = build_lookup_table(transl_df)
    dir_out = args.o
    path_out = f"{dir_out}/cts_lookup_table.json"
    with open(path_out, 'w') as t:
        json.dump(lookup_table, t)


def load_transform_csv(path):
    df = pd.read_csv(path)
    df = df.rename(columns={"CTS-URN/s":"cts-urns_grp", "Original File Name/Location":"Original_File_Name", 
                                        "Addiional File location/locations":"Additional_File_locations", "Translation Language":"translation_language",
                                        "New File Name/s":"New_File_Name"})
    df["cts-urns_uniques"] = df["cts-urns_grp"].str.split()
    df = df.explode("cts-urns_uniques", ignore_index=True)
    df["ctsurns"] = df["cts-urns_uniques"].str.rsplit(".",n=1).str[0]
    df["filename1"] = df["Original_File_Name"].str.split(".").str[0]
    df["filename2"] = df["Additional_File_locations"].str.split(".").str[0]
    # don't split filenames in this col
    df["filename3"] = df["New_File_Name"]
    df.fillna("", inplace=True)
    return df


def build_lookup_table(transl_df):
    lookup_table = {}
    keys = transl_df["ctsurns"].unique()
    for ctsurn in keys:
        vals_initial = set(transl_df.loc[transl_df["ctsurns"] == ctsurn, "filename1"])
        vals = set([name for name in vals_initial if name != ""])
        for other_files in list(transl_df.loc[transl_df["ctsurns"] == ctsurn, "filename2"]):
            # don't add empty string values
            if other_files != "":
                new_files = other_files.split()
                for file in new_files:
                    vals.add(file)
        for other_files in list(transl_df.loc[transl_df["ctsurns"] == ctsurn, "filename3"]):
            # don't add empty string values
            if other_files != "":
                new_files = other_files.split()
                for file in new_files:
                    vals.add(file)
        # turn back to list to write to json
        lookup_table[ctsurn] = list(vals)
    return lookup_table

if __name__ == "__main__":
    main()