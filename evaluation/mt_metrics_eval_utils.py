#!/usr/bin/env python
# coding: utf-8

# This is an adapted version of the official Jupyter notebook:
# in google-research/mt-metrics-eval/mt_metrics_eval/mt_metrics_eval.ipynb.

# Imports

import itertools
from typing import Dict, List, Tuple

import numpy as np
import pandas as pd
import scipy.stats
from mt_metrics_eval import data, meta_info, stats

INCLUDE_HUMAN = False
INCLUDE_OUTLIERS = False
TEST_SET_NAME = "ntrex-128"
PRIMARY_METRICS = False
DOMAIN = None
k = 2000
PSD = stats.PermutationSigDiffParams(block_size=100)
PVAL = 0.05
CRITICAL_P_VAL = (
    0.05  # For system filtering - vary between 1 and 0; 1 corresponds to no filtering
)


def load_dataset(path: str) -> Dict[str, data.EvalSet]:
    eval_sets = {}
    for testset in meta_info.DATA:
        # Our evaluation only concerns the ntrex-128 test set
        if testset != TEST_SET_NAME:
            continue
        for lp in meta_info.DATA[testset]:
            eval_sets[f"{testset}/{lp}"] = data.EvalSet(testset, lp, True, path=path)
    return eval_sets


def load_scores(dialect: str, path: str) -> pd.DataFrame:
    scores = pd.read_csv(
        f"{path}/{TEST_SET_NAME}/human-scores/en-gsw_{dialect}.{TEST_SET_NAME}.seg.score",
        sep="\t",
        header=None,
        names=["sys_name", "score"],
    )
    return scores


def get_differences(scores: pd.DataFrame, system_1: str, system_2: str) -> pd.DataFrame:
    system_1_scores = scores[scores["sys_name"] == system_1]["score"].reset_index(
        drop=True
    )
    system_2_scores = scores[scores["sys_name"] == system_2]["score"].reset_index(
        drop=True
    )
    return system_1_scores.subtract(system_2_scores)


def filter_according_to_p_val(
    eval_set: data.EvalSet, dialect: str, path: str, critical_p_val: float
) -> List[Tuple[str, str]]:
    all_sys_pairs = itertools.combinations(eval_set.sys_names, 2)

    sys_pairs = []
    human_scores = load_scores(dialect=dialect, path=path)
    for sys_1, sys_2 in all_sys_pairs:
        diff = get_differences(human_scores, sys_1, sys_2)
        # Run Wilcoxon signed-rank test
        p_val = scipy.stats.wilcoxon(diff, alternative="two-sided").pvalue
        if p_val < critical_p_val:
            sys_pairs.append((sys_1, sys_2))
            sys_pairs.append((sys_2, sys_1))

    return sys_pairs


def print_stats(eval_sets: Dict[str, data.EvalSet]) -> None:
    print("Summaries for all loaded evalsets")

    print(f'{"name":<20}  segs sys metrics gold  refs std')
    for name, evs in eval_sets.items():
        nsegs = len(evs.src)
        nsys = len(evs.sys_names)
        nmetrics = len(evs.metric_basenames)
        gold = evs.StdHumanScoreName("sys")
        nrefs = len(evs.ref_names)
        std_ref = evs.std_ref

        print(
            f"{name:<20} {nsegs:5d} {nsys:3d} {nmetrics:7d} "
            f"{gold:5} {nrefs:4d} {std_ref}"
        )


def run_sys_pairwise_acc_analysis(
    eval_sets: Dict[str, data.EvalSet], path: str
) -> None:
    name_to_sys_pairs = {}
    for name, eval_set in eval_sets.items():
        name_to_sys_pairs[name] = filter_according_to_p_val(
            eval_set=eval_set,
            dialect=name[-2:],
            path=path,
            critical_p_val=CRITICAL_P_VAL,
        )

    evs_list = eval_sets.values()
    main_refs = [{evs.std_ref} for evs in evs_list]
    close_refs = [{"refB"} if k == "wmt21.news/en-de" else set() for k in eval_sets]

    ranks, matrix = data.CompareMetricsWithGlobalAccuracy(
        eval_sets,
        main_refs,
        close_refs,
        INCLUDE_HUMAN,
        INCLUDE_OUTLIERS,  # evs_list
        TEST_SET_NAME,
        PRIMARY_METRICS,
        DOMAIN,
        k,
        PSD,
        PVAL,
        relevant_sys_pairs=name_to_sys_pairs,
    )

    data.PrintMetricComparison(ranks, matrix, PVAL)


def run_sys_level_pearson_corr_analysis(eval_set: data.EvalSet) -> None:
    corrs = data.GetCorrelations(
        eval_set,
        "sys",
        {eval_set.std_ref},
        {"refB"},
        INCLUDE_HUMAN,
        INCLUDE_OUTLIERS,
        TEST_SET_NAME,
        PRIMARY_METRICS,
        DOMAIN,
    )
    ranks, matrix = data.CompareMetrics(
        corrs, scipy.stats.pearsonr, "none", k, PSD, PVAL
    )
    data.PrintMetricComparison(ranks, matrix, PVAL, eval_set)


def run_seg_level_kendall_tau_analysis(eval_set: data.EvalSet) -> None:
    corrs = data.GetCorrelations(
        eval_set,
        "seg",
        {eval_set.std_ref},
        {"refB"},
        INCLUDE_HUMAN,
        INCLUDE_OUTLIERS,
        TEST_SET_NAME,
        PRIMARY_METRICS,
        DOMAIN,
    )
    ranks, matrix = data.CompareMetrics(
        corrs, scipy.stats.kendalltau, "none", k, PSD, PVAL
    )
    data.PrintMetricComparison(ranks, matrix, PVAL, eval_set)


def run_seg_level_acc_analysis(eval_set: data.EvalSet) -> None:
    corrs = data.GetCorrelations(
        eval_set,
        "seg",
        {eval_set.std_ref},
        {"refB"},
        INCLUDE_HUMAN,
        INCLUDE_OUTLIERS,
        TEST_SET_NAME,
        PRIMARY_METRICS,
        DOMAIN,
    )
    ranks, matrix = data.CompareMetrics(
        corrs,
        stats.KendallWithTiesOpt,
        "item",
        0,
        PSD,
        PVAL,
        variant="acc23",
        sample_rate=0.1,
    )
    data.PrintMetricComparison(ranks, matrix, PVAL, eval_set)
