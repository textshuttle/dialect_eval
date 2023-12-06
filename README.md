# Official resources for ["A Benchmark for Evaluating Machine Translation Metrics on Dialects Without Standard Orthography"](https://aclanthology.org/2023.wmt-1.99/)

This repository contains the code and additional resources for the paper "A Benchmark for Evaluating Machine Translation Metrics on Dialects Without Standard Orthography" presented at WMT 2023.

In the `evaluation` directory, you can find:
- the Swiss German translations of [NTREX-128](https://github.com/MicrosoftTranslator/NTREX)
- the systems translations and the human ratings
- the challenge set
- the code to evaluate metrics on our test sets.

In the `training` directory, you can find the code for training the neural metrics evaluated in the paper. 

## Installation 

We provide a fork of the `mtm-metrics-eval` repository. Run the following commands to clone it before you follow instructions in the `evaluation` directory. 
```
git submodule init
git submodule update
```

## Citation

If you use our code, data or models, please cite our [paper](https://aclanthology.org/2023.wmt-1.99/):

    @inproceedings{aepli-etal-2023-benchmark,
        title = "A Benchmark for Evaluating Machine Translation Metrics on Dialects without Standard Orthography",
        author = {Aepli, No{\"e}mi  and
        Amrhein, Chantal  and
        Schottmann, Florian  and
        Sennrich, Rico},
        editor = "Koehn, Philipp  and
        Haddon, Barry  and
        Kocmi, Tom  and
        Monz, Christof",
        booktitle = "Proceedings of the Eighth Conference on Machine Translation",
        month = dec,
        year = "2023",
        address = "Singapore",
        publisher = "Association for Computational Linguistics",
        url = "https://aclanthology.org/2023.wmt-1.99",
        pages = "1045--1065"
    }
