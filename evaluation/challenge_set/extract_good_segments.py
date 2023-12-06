#!/usr/bin/env python3
import csv
import random
import argparse

from collections import defaultdict
from typing import List, Dict
from itertools import combinations
from pathlib import Path

import pandas as pd


random.seed(2023)


def get_arg_parser() -> argparse.Namespace:
    '''
    Parse arguments via command-line.
    '''
    parser = argparse.ArgumentParser(description='Command for extracting challenge set.')

    parser.add_argument('-r', '--references',
                        type=argparse.FileType("r"),
                        required=True,
                        help='File with human reference translations.')

    parser.add_argument('-s', '--sources',
                        type=argparse.FileType("r"),
                        required=True,
                        help='File with English sources.')

    parser.add_argument('-hs', '--human_scores',
                        type=argparse.FileType("r"),
                        required=True,
                        help='Files with human scores.')

    parser.add_argument('-o', '--outfile',
                        type=argparse.FileType("w"),
                        required=True,
                        help='File to store challengeset in.')

    parser.add_argument('-t', '--system_outputs',
                        type=argparse.FileType("r"),
                        nargs='+',
                        required=True,
                        help='Files with automatic MT translations.')

    return parser


def extract_relevant_segments(system_outputs: List[Path],
                              human_scores: pd.DataFrame) -> Dict[int, Dict[int, str]]:
    '''
    Return all MT outputs with perfect scores.
    '''
    relevant_segments = defaultdict(dict)

    for system_output in system_outputs:

        # Find relevant human judgement scores
        doc_id = system_output.name.split('/')[-1].rstrip('.txt')
        system_scores = human_scores.loc[human_scores['docID'] == doc_id]
        system_scores.reset_index(inplace=True)

        # Extract all translations with perfect human judgement score
        for line, (i, score) in zip(system_output, system_scores.iterrows()):
            if score['score'] == 100:
                relevant_segments[i][doc_id] = line

    return relevant_segments


def construct_equivalent_pairs(sources: Path,
                               references: Path,
                               relevant_segments: Dict[int, Dict[int, str]],
                               modifications: List[str]) -> pd.DataFrame:
    '''
    Collect info about equivalent translation pairs.
    '''
    df = pd.DataFrame(columns=['source',
                               'reference',
                               'sentA',
                               'sentB',
                               'modification_type',
                               'sentA_to_modify'])

    for i, (src, ref) in enumerate(zip(sources, references)):
        new_pair = {'source': src.strip(),
                    'reference': ref.strip()}

        # Only consider cases where more than one translation was rated perfect
        translations = set([v for k, v in relevant_segments[i].items()])
        if len(translations) >= 2:
            for a, b in combinations(translations, 2):
                new_pair['sentA'] = a.strip()
                new_pair['sentB'] = b.strip()
                new_pair['modification_type'] = random.choice(modifications)
                new_pair['sentA_to_modify'] = a.strip()
                df = pd.concat([df, pd.DataFrame([new_pair])], ignore_index=True)


    return df


def main(args: argparse.Namespace) -> None:
    '''
    Create challengeset with equivalent translations.
    '''
    # Read the human judgement scores
    human_scores = pd.read_csv(args.human_scores,
                               sep='\t',
                               header=None,
                               names=['docID', 'score'])

    # Extract MT outputs that got perfect human judgement scores (100)
    relevant_segments = extract_relevant_segments(args.system_outputs,
                                                  human_scores)

    # Construct equivalent pairs of translations
    modifications = ['deletion', 'insertion', 'substitution']
    equivalent_pairs = construct_equivalent_pairs(args.sources,
                                                  args.references,
                                                  relevant_segments,
                                                  modifications)
    # Write to TSV format
    equivalent_pairs.to_csv(args.outfile,
                            index=None,
                            sep='\t',
                            quoting=csv.QUOTE_NONE)


if __name__ == "__main__":
    args = get_arg_parser().parse_args()
    main(args)
