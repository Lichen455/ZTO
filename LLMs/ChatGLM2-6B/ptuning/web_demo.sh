PRE_SEQ_LEN=128

CUDA_VISIBLE_DEVICES=0 python3 web_demo.py \
    --model_name_or_path data/models/chatglm2/ \
    --ptuning_checkpoint output2/checkpoint-100 \
    --pre_seq_len $PRE_SEQ_LEN

