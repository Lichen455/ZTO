import openai
import os, json, random
from zhipuai import ZhipuAI


client = ZhipuAI(api_key=os.environ.get('GLM_APIKEY'))
openai.api_key = "sk-GY7tkLBbSgTNcBuPDZ5JcBMFYY4VPoMGc4ZltTMbLvSpDILk"
openai.api_base = "https://api.chatanywhere.com.cn/v1"


def add(path, data1, data2):
    # 如果文件不存在，用 "x" 模式创建一个新文件
    try:
        with open(path, "x", encoding="utf-8") as f:
            # 什么都不做,作用是如果找不到文件就创建
            print()
    except FileExistsError:
        # 如果文件已经存在，不做任何操作
        pass

    # 用 "a+" 模式打开文件
    with open(path, "r+", encoding="utf-8") as f:
        # 如果文件为空，先写入一个空列表
        if os.stat(path).st_size == 0:
            json.dump([], f)
        # 将文件指针移动到开头
        f.seek(0)
        # 读取文件中的 JSON 数据
        datax = json.load(f)
        # 追加新的数据
        datax.append({"prompt": data1, "response": data2})
        # 将文件指针移动到开头
        f.seek(0)
        # 将修改后的数据写回文件中
        json.dump(datax, f, indent=4, ensure_ascii=False)


def ZhipuAI(messages):
    response = client.chat.completions.create(
        model="glm-4",  # 填写需要调用的模型名称
        messages=messages
    )
    return response.choices[0].message.content


def gpt_4_api_stream(messages: list):
    try:
        response = openai.ChatCompletion.create(
            model='gpt-4-1106-preview',
            messages=messages,
            stream=True,
        )
        completion = {'role': '', 'content': ''}
        for event in response:
            if event['choices'][0]['finish_reason'] == 'stop':
                break
            for delta_k, delta_v in event['choices'][0]['delta'].items():
                # print(f'流响应数据: {delta_k} = {delta_v}')
                completion[delta_k] += delta_v
        messages.append(completion)  # 直接在传入参数 messages 中追加消息
        return (True, ''), completion['content']
    except Exception as err:
        return (False, f'OpenAI API 异常: {err}')


def use_Api(messages:list = []):

    b = ZhipuAI(messages)
    return b

if __name__ == "__main__":
    print(use_Api([
        {"role": "system", "content": "你是一名人工智能出题助手，负责以如下格式生成编程题目，编程语言为Python，不需要解析"},
        {"role": "user",
         "content": "请严格按照与上文相同的格式，生成”难度很高“的编程判断题目"},
        {"role": "assistant",
         "content": "[题目] 在C++标准模板库中，可以使用 `<algorithm>` 头文件中的 `std::find_if` 函数对任意类型的容器进行查找，且该函数的搜索条件可以通过Lambda表达式或函数对象轻松自定义。 [答案] 正确"},
        {"role": "user",
         "content": "请严格按照与上文相同的格式，生成”难度很高“的编程判断题目"},
        {"role": "assistant",
         "content": "[题目] 在表达式 x+yz中， + 是作为成员函数重载的运算符， 是作为非成员函数重载的运算符。则 operator+ 有1个参数 [答案] 正确"},
        {"role": "user",
         "content": "请严格按照与上文相同的格式，生成”难度很高“的编程判断题目"},
        {"role": "assistant",
         "content": "[题目] 静态成员函数没有this指针 [答案] 正确"},
        {"role": "user",
         "content": "请严格按照与上文相同的格式，生成”难度很高“的编程判断题目"},
        {"role": "assistant",
         "content": "[题目] 构造函数、析构函数能被继承或取地址 [答案] 错误"},
        {"role": "user",
         "content": "请严格按照与上文相同的格式，创新生成难度很高的20道C++编程判断题目，题干尽量精简，不能与上文重复或相似，不能太简单，答案只能是正确或错误"}
    ]))