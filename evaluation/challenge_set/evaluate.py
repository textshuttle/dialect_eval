#!/usr/bin/env python3
import re
import csv
import argparse

from typing import List

import pandas as pd
import numpy as np


def get_arg_parser() -> argparse.Namespace:
    '''
    Parse arguments via command-line.
    '''
    parser = argparse.ArgumentParser(description='Command for evaluating different metrics.')

    parser.add_argument('-i', '--input',
                        type=argparse.FileType("r"),
                        required=True,
                        help='Input TSV file with sources, translation hypotheses, references and metric scores.')

    parser.add_argument('-p', '--pretty_print',
                        action='store_true',
                        help='If set will print readable format, otherwise will print format that can be copied to spreadsheet.')

    return parser


def comp_acc(scoresA: List[float],
             scoresB: List[float],
             scoresA_sem_changed: List[float]) -> float:
    '''
    Compute success rate (accuracy), inspired by Sun etal. (2023).
    '''
    # Compute score differences between hypotheses
    a_b_diffs = np.absolute(scoresA - scoresB)
    a_sem_changed = np.minimum(scoresA, scoresB) - scoresA_sem_changed

    # Compare score differences
    b_larger_diff = np.count_nonzero(a_b_diffs < a_sem_changed)
    a_sem_changed_larger_diff = np.count_nonzero(a_b_diffs >= a_sem_changed)
    acc = b_larger_diff / (b_larger_diff + a_sem_changed_larger_diff)

    return acc


def main(args: argparse.Namespace) -> None:
    '''
    Evaluate all models in all TSV files and print success rate.
    '''
    tsv_f = pd.read_csv(args.input, sep='\t', quoting=csv.QUOTE_NONE)
    metrics = [re.sub('_sentA', '', m) for m in tsv_f.columns
               if m.endswith('_sentA')]

    # Print info / header
    if args.pretty_print:
        print(f'\n\nEvaluating {args.input.name}\n')
    if not args.pretty_print:
        print('\t'.join(metrics))

    # Compute success rate for each metric
    results = []
    metric_results = []
    for m in metrics:
        acc = round(comp_acc(tsv_f[f'{m}_sentA'],
                             tsv_f[f'{m}_sentB'],
                             tsv_f[f'{m}_sentA_sem_changed']), 3)
        results.append(str(acc))
        metric_results.append((str(acc), m))

    # Print results
    if args.pretty_print:
        for a, m in sorted(metric_results, reverse=True):
            print(f'\t{m}\t{a}')
    if not args.pretty_print:
        print('\t'.join(results))


if __name__ == '__main__':
    args = get_arg_parser().parse_args()
    main(args)
