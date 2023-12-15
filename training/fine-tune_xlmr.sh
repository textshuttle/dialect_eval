#!/bin/bash

# Fine-tuning XLMR with the Huggingface Transformers library
# huggingface/transformers/examples/pytorch/language-modeling/run_mlm.py
# specific version used:
# https://github.com/huggingface/transformers/blob/149cb0cce2df3f932de58c6d05cec548600553e2/examples/pytorch/language-modeling/run_mlm.py


OUT_PATH='model_output_path'
TRAIN_FILE=='path_to_train_file'

WDIR='working_directory'

python $WDIR/transformers/examples/pytorch/language-modeling/run_mlm.py \
    --model_name_or_path xlm-roberta-base \
    --train_file $TRAIN_FILE \
    --per_device_train_batch_size 8 \
    --per_device_eval_batch_size 8 \
    --do_train \
    --do_eval \
    --output_dir $OUT_PATH \
    --line_by_line \
    --overwrite_output_dir


# Parameters (default)

# Training/evaluation parameters TrainingArguments(
# _n_gpu=1,
# adafactor=False,
# adam_beta1=0.9,
# adam_beta2=0.999,
# adam_epsilon=1e-08,
# auto_find_batch_size=False,
# bf16=False,
# bf16_full_eval=False,
# data_seed=None,
# dataloader_drop_last=False,
# dataloader_num_workers=0,
# dataloader_pin_memory=True,
# ddp_backend=None,
# ddp_broadcast_buffers=None,
# ddp_bucket_cap_mb=None,
# ddp_find_unused_parameters=None,
# ddp_timeout=1800,
# debug=[],
# deepspeed=None,
# disable_tqdm=False,
# dispatch_batches=None,
# do_eval=True,
# do_predict=False,
# do_train=True,
# eval_accumulation_steps=None,
# eval_delay=0,
# eval_steps=None,
# evaluation_strategy=no,
# fp16=False,
# fp16_backend=auto,
# fp16_full_eval=False,
# fp16_opt_level=O1,
# fsdp=[],
# fsdp_config={'min_num_params': 0, 'xla': False, 'xla_fsdp_grad_ckpt': False},
# fsdp_min_num_params=0,
# fsdp_transformer_layer_cls_to_wrap=None,
# full_determinism=False,
# gradient_accumulation_steps=1,
# gradient_checkpointing=False,
# greater_is_better=None,
# group_by_length=False,
# half_precision_backend=auto,
# hub_always_push=False,
# hub_model_id=None,
# hub_private_repo=False,
# hub_strategy=every_save,
# hub_token=<HUB_TOKEN>,
# ignore_data_skip=False,
# include_inputs_for_metrics=False,
# include_tokens_per_second=False,
# jit_mode_eval=False,
# label_names=None,
# label_smoothing_factor=0.0,
# learning_rate=5e-05,
# length_column_name=length,
# load_best_model_at_end=False,
# local_rank=0,
# log_level=passive,
# log_level_replica=warning,
# log_on_each_node=True,
# logging_dir=/srv/scratch3/naepli/dialect-eval/ft_xlmr//test/runs/Oct13_15-21-07_glados,
# logging_first_step=False,
# logging_nan_inf_filter=True,
# logging_steps=500,
# logging_strategy=steps,
# lr_scheduler_type=linear,
# max_grad_norm=1.0,
# max_steps=-1,
# metric_for_best_model=None,
# mp_parameters=,
# no_cuda=False,
# num_train_epochs=3.0,
# optim=adamw_torch,
# optim_args=None,
# output_dir=/srv/scratch3/naepli/dialect-eval/ft_xlmr//test,
# overwrite_output_dir=True,
# past_index=-1,
# per_device_eval_batch_size=8,
# per_device_train_batch_size=8,
# prediction_loss_only=False,
# push_to_hub=False,
# push_to_hub_model_id=None,
# push_to_hub_organization=None,
# push_to_hub_token=<PUSH_TO_HUB_TOKEN>,
# ray_scope=last,
# remove_unused_columns=True,
# report_to=['tensorboard', 'wandb'],
# resume_from_checkpoint=None,
# run_name=/srv/scratch3/naepli/dialect-eval/ft_xlmr//test,
# save_on_each_node=False,
# save_safetensors=False,
# save_steps=500,
# save_strategy=steps,
# save_total_limit=None,
# seed=42,
# sharded_ddp=[],
# skip_memory_metrics=True,
# tf32=None,
# torch_compile=False,
# torch_compile_backend=None,
# torch_compile_mode=None,
# torchdynamo=None,
# tpu_metrics_debug=False,
# tpu_num_cores=None,
# use_cpu=False,
# use_ipex=False,
# use_legacy_prediction_loop=False,
# use_mps_device=False,
# warmup_ratio=0.0,
# warmup_steps=0,
# weight_decay=0.0,
# )
