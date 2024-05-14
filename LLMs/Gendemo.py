import os, sys
import time
import gradio as gr
import mdtex2html
from typing import Dict
import torch
import transformers
from transformers import (
    AutoConfig,
    AutoModel,
    AutoTokenizer,
    AutoTokenizer,
    DataCollatorForSeq2Seq,
    HfArgumentParser,
    Seq2SeqTrainingArguments,
    set_seed,
)
import sys
# sys.path.append('./ptuning')

import os
import subprocess

# 设置环境变量
os.environ['CUDA_VISIBLE_DEVICES'] = '0'
os.environ['PRE_SEQ_LEN'] = '128'

# # web_demo.py 的参数
# model_name_or_path = '/data/models/chatglm2/'
# ptuning_checkpoint = './PTuning_models/cf_500/'
# pre_seq_len = 128
# quantization_bit = None


model = None
tokenizer = None


def postprocess(self, y):
    if y is None:
        return []
    for i, (message, response) in enumerate(y):
        y[i] = (
            None if message is None else mdtex2html.convert((message)),
            None if response is None else mdtex2html.convert(response),
        )
    return y


gr.Chatbot.postprocess = postprocess


def parse_text(text):
    return text


def parse_text_b(text):
    """copy from https://github.com/GaiZhenbiao/ChuanhuChatGPT/"""
    lines = text.split("\n")
    lines = [line for line in lines if line != ""]
    count = 0
    for i, line in enumerate(lines):
        if "```" in line:
            count += 1
            items = line.split('`')
            if count % 2 == 1:
                lines[i] = f'<pre><code class="language-{items[-1]}">'
            else:
                lines[i] = f'<br></code></pre>'
        else:
            if i > 0:
                if count % 2 == 1:
                    line = line.replace("`", "\`")
                    line = line.replace("<", "&lt;")
                    line = line.replace(">", "&gt;")
                    line = line.replace(" ", "&nbsp;")
                    line = line.replace("*", "&ast;")
                    line = line.replace("_", "&lowbar;")
                    line = line.replace("-", "&#45;")
                    line = line.replace(".", "&#46;")
                    line = line.replace("!", "&#33;")
                    line = line.replace("(", "&#40;")
                    line = line.replace(")", "&#41;")
                    line = line.replace("$", "&#36;")
                lines[i] = "<br>" + line
    text = "".join(lines)
    return text


global prev_string, count, judgment_End
judgment_End = 0
prev_string = None


def predict2(input, chatbot, max_length, top_p, temperature, history, past_key_values):
    strs = ""
    # print(input, chatbot, max_length, top_p, temperature, history, past_key_values)
    chatbot2, max_length2, top_p2, temperature2, history2, past_key_values2 = chatbot, max_length, top_p, temperature, history, past_key_values
    # print(past_key_values2)
    global judgment_End
    # if not isinstance(chatbot, list):
    #     chatbot = [chatbot]

    print("User Input:", parse_text(input))

    chatbot.append((parse_text(input), ""))
    # input = "请出一道编程算法题目，只出题干，不包括解题过程,格式一致"
    for response, history, past_key_values in model.stream_chat(tokenizer, input, history,
                                                                past_key_values=past_key_values,
                                                                return_past_key_values=True,
                                                                max_length=max_length, top_p=top_p,
                                                                temperature=temperature):
        # print(parse_text(response))
        chatbot[-1] = (parse_text(input), parse_text(response))

        yield parse_text(response)


def reset_user_input():
    return gr.update(value='')


def reset_state():
    return [], [], None


def PTuning_main(num: int = 5, model_name_or_path: str = os.environ.get('GLM_6B_PATH'),
                 ptuning_checkpoint: str = None, pre_seq_len: int = 128,
                 chatdata: Dict[str, int] = {"input": "", "chatbot": [], "max_length": 8192, "top_p": 0.8,
                                             "temperature": 0.95, "history": []}) -> list:
    global model, tokenizer
    quantization_bit = None
    # 加载模型
    tokenizer = AutoTokenizer.from_pretrained(
        model_name_or_path, trust_remote_code=True)
    config = AutoConfig.from_pretrained(
        model_name_or_path, trust_remote_code=True)

    config.pre_seq_len = pre_seq_len
    config.prefix_projection = False

    if ptuning_checkpoint is not None:
        print(f"Loading prefix_encoder weight from {ptuning_checkpoint}")
        model = AutoModel.from_pretrained(model_name_or_path, config=config, trust_remote_code=True)
        prefix_state_dict = torch.load(os.path.join(ptuning_checkpoint, "pytorch_model.bin"))
        new_prefix_state_dict = {}
        for k, v in prefix_state_dict.items():
            if k.startswith("transformer.prefix_encoder."):
                new_prefix_state_dict[k[len("transformer.prefix_encoder."):]] = v
        model.transformer.prefix_encoder.load_state_dict(new_prefix_state_dict)
    else:
        model = AutoModel.from_pretrained(model_name_or_path, config=config, trust_remote_code=True)

    if quantization_bit is not None:
        print(f"Quantized to {quantization_bit} bit")
        model = model.quantize(quantization_bit)
    model = model.cuda()
    if pre_seq_len is not None:
        # P-tuning v2
        model.transformer.prefix_encoder.float()

    model = model.eval()

    re1 = []

    for i in range(0, num):
        re1.append(Generator(chatdata))

    return re1


def Generator(chatdata):
    #  生成生成器对象
    prediction_generator = predict2(chatdata["input"], chatdata["chatbot"], chatdata["max_length"], chatdata["top_p"],
                                    chatdata["temperature"], chatdata["history"], None)
    result = ""
    try:
        while True:
            # 迭代
            result = next(prediction_generator)

    except StopIteration:
        # 当生成器迭代完毕时，会引发 StopIteration 异常
        print("生成器迭代完毕")
        print(result)

    print("主函数main运行")

    # demo.queue().launch(share=False, inbrowser=True)

    return result


if __name__ == "__main__":
    print(PTuning_main(model_name_or_path=os.environ.get('GLM_6B_PATH'), chatdata={
        "input": "请严格按照与上文相同的格式，必须有以下字段：[题目]，创新生成难度很高的编程填空题目，不能与上文重复或相似,必须有____，不能太简单，答案只能一行",
        "chatbot": [], "max_length": 8192, "top_p": 0.8, "temperature": 0.95, "history": []}))
