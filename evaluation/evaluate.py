#!/usr/bin/env python
# coding: utf-8


import argparse

from mt_metrics_eval_utils import (load_dataset, print_stats,
                                   run_seg_level_acc_analysis,
                                   run_seg_level_kendall_tau_analysis,
                                   run_sys_level_pearson_corr_analysis,
                                   run_sys_pairwise_acc_analysis)

DIALECTS = ["be", "zh"]


def get_arg_parser() -> argparse.Namespace:
    """
    Parse arguments via command-line.
    """
    parser = argparse.ArgumentParser(description="Command for evaluating different metrics.")

    parser.add_argument(
        "-f",
        "--eval_folder",
        type=str,
        required=True,
        help="Path to evaluation folder.",
    )

    return parser


def main(args: argparse.Namespace) -> None:
    """Run evaluations from the "A Benchmark for Evaluating Machine Translation Metrics on Dialects Without Standard Orthography" paper."""

    # Load dataset and print test set stats.
    eval_sets = load_dataset(args.eval_folder)
    print_stats(eval_sets)

    print(
        "\nThe output shows the rank of each metric's significance cluster, followed by its accuracy, \nand whether it is statistically tied with (=) or better than (>) each lower-ranking metric."
    )

    # Evaluate metrics using global accuracy.
    print("\nPairwise accuracy")
    run_sys_pairwise_acc_analysis(eval_sets, args.eval_folder)

    # Evaluate metrics using system-level Pearson correlation.
    print("\nSystem-level Pearson correlation")

    for dialect in DIALECTS:
        print(f"Gsw {dialect}")
        run_sys_level_pearson_corr_analysis(eval_sets[f"ntrex-128/en-gsw_{dialect}"])

    # Evaluate metrics using segment-level Kendall correlation.
    print("\nSegment-level Kendall correlation")

    for dialect in DIALECTS:
        print(f"Gsw {dialect}")
        run_seg_level_kendall_tau_analysis(eval_sets[f"ntrex-128/en-gsw_{dialect}"])

    # Evaluate metrics using seg-level accuracy with optimized tie threshold.
    print("\nSegment-level accuracy with optimized tie threshold")

    for dialect in DIALECTS:
        print(f"Gsw {dialect}")
        run_seg_level_acc_analysis(eval_sets[f"ntrex-128/en-gsw_{dialect}"])


if __name__ == "__main__":
    args = get_arg_parser().parse_args()
    main(args)
