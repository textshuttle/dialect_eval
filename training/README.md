## Training

### Language Model Fine-Tuning

We fine-tuned [XLMR](https://huggingface.co/xlm-roberta-base) with the Huggingface Transformers library with `fine-tune_xlmr.sh`. We used [this specific version](https://github.com/huggingface/transformers/blob/149cb0cce2df3f932de58c6d05cec548600553e2/examples/pytorch/language-modeling/run_mlm.py) of the HuggingFace training script (`run_mlm.py`) for our experiments.

### COMET Training

We trained COMET models according to the [Unbabel/COMET repo](https://github.com/Unbabel/COMET) "Train your own Metric":
``` 
comet-train --cfg configs/models/{model_config}.yml
```
`model_config.yml` is either `regression_model.yml` or `referenceless_model.yml` for QE metrics.

We used [this specific version](https://github.com/Unbabel/COMET/blob/8503fe799658b753055ced0b1f0950e4404b5065/comet/cli/train.py) of the COMET training script (`train.py`) for our experiments.

## Data

The data we used for the continued LM pre-training can be downloaded from [here](https://icosys.ch/swisscrawl).

The data we used for the task fine-tuning can be downloaded from [here](https://files.ifi.uzh.ch/cl/dialect-eval). It contains the direct assessment (DA) data from the official [COMET repo](https://github.com/Unbabel/COMET/blob/master/data/README.md) and the noised version of this data set, which we used for the fine-tuning with character-level noise.
