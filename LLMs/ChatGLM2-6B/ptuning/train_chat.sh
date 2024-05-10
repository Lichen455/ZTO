PRE_SEQ_LEN=128
LR=1e-2
NUM_GPUS=1

torchrun --standalone --nnodes=1 --nproc-per-node=$NUM_GPUS main.py \
    --do_train \
    --train_file ./dataset/cf200.json \
    --validation_file ./dataset/cf200v.json \
    --preprocessing_num_workers 50 \
    --prompt_column prompt \
    --response_column response \
    --overwrite_cache \
    --model_name_or_path /data/models/chatglm2 \
    --output_dir ./output \
    --overwrite_output_dir \
    --max_source_length 256 \
    --max_target_length 256 \
    --per_device_train_batch_size 2 \
    --per_device_eval_batch_size 2 \
    --gradient_accumulation_steps 16 \
    --predict_with_generate \
    --max_steps 1000 \
    --logging_steps 10 \
    --save_steps 100 \
    --learning_rate $LR \
    --pre_seq_len $PRE_SEQ_LEN \
    --quantization_bit 8

