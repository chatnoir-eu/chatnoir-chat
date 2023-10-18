#!/bin/bash
#SBATCH --nodes=1
#SBATCH --cpus-per-task=20
#SBATCH --mem=200G
#SBATCH --job-name=alpaca
#SBATCH --partition=ai
#SBATCH --account=a_ielab
#SBATCH --gres=gpu:a100:3
#SBATCH --time=99:00:00
#SBATCH -o print2.txt
#SBATCH -e error2.txt


module load anaconda3/2022.05
module load cuda/11.7.0
# change below to your own environment name
source activate alpaca

# change below to your own path

torchrun --nproc_per_node=3 --master_port=12345 train.py \
    --model_name_or_path ./Llama/converted/llama-7b \
    --data_path alpaca_data.json \
    --bf16 True \
    --output_dir output/out_13b/ \
    --num_train_epochs 3 \
    --per_device_train_batch_size 4 \
    --per_device_eval_batch_size 2 \
    --gradient_accumulation_steps 8 \
    --evaluation_strategy "no" \
    --save_strategy "steps" \
    --save_steps 200 \
    --save_total_limit 1 \
    --learning_rate 2e-5 \
    --weight_decay 0. \
    --warmup_ratio 0.03 \
    --lr_scheduler_type "cosine" \
    --logging_steps 1 \
    --fsdp "full_shard auto_wrap" \
    --fsdp_transformer_layer_cls_to_wrap 'LlamaDecoderLayer' \
    --cache_dir ./alpaca_repro/cache \
    --tf32 True