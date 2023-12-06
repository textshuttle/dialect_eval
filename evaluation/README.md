## NTREX-128 data

You can find the Swiss German translation of the NTREX-128 data in the `ntrex-128/references` directory. Other resources for the evaluation of existing metrics, e.g. the human ratings and the system translations are available inside the respective subdirectories of `ntrex-128`.

## Evaluation

In order to evaluate a metric with our resources, follow the `mtm-metrics-eval` installation instructions inside the repo (after updating it as a submodule). Next, run the following commands to be able to access our resources with `mtm-metrics-eval`

```
mkdir -p $HOME/.mt-metrics-eval/mt-metrics-eval-v2
cp -r ntrex-128 $HOME/.mt-metrics-eval/mt-metrics-eval-v2/
```

The evaluation of the metrics with `mtm-metrics-eval` on our resources can be reproduced by running 

```
python3 evaluate.py -f .
```

In order to reproduce the preprocessing necessary to bring the data into an adequate format for `mtm-metrics-eval`, run the following commands:

```
cd utils
bash prepare_data.sh
```

## Challenge Sets

To extract equivalent MT outputs pairs that each received a perfect human judgement score, run the following script where `DIALECT` is either `be` or `zh`:

```
python3 challenge_set/extract_good_segments.py -r ntrex-128/references/en-gsw_DIALECT.refA.txt -s ntrex-128/sources/en-gsw_DIALECT.txt -hs ntrex-128/human-scores/en-gsw_DIALECT.ntrex-128.seg.score -t ntrex-128/system-outputs/en-gsw_DIALECT/* -o challenge_set_DIALECT.tsv
```

To create our challenge set, we then manually altered the segment in the `sentA_to_modify` column as described in our paper. Our challenge sets can be found under `evaluation/challenge_set`. The `annotated` files can be used to score new metrics, the `scored` files additionally contain the scores of metrics evaluated in the paper. 

To evaluate metrics on our challenge set, run the following script where `DIALECT` is either `be` or `zh`:

```
python3 challenge_set/evaluate.py -i challenge_set/challenge_set_DIALECT.scored.tsv -p
```

If you want to have the numbers in TSV format, simply remove the `-p` parameter.



