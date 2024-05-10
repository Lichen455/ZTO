from LLMs import Gendemo
from functools import partial



PTuning_main = Gendemo.PTuning_main

# 判断题
def Judgment(language_p:int = 1,num:int=1):

    if   language_p == 1:
        data = PTuning_main(num=num, ptuning_checkpoint="./PTuning_models/tfc_500/", chatdata={
            "input": "请出一道C++判断题，格式固定",
            "chatbot": [], "max_length": 8192, "top_p": 0.8, "temperature": 0.95, "history": []})
        print(data)


        return

    elif language_p == 2:
        data = PTuning_main(num=num, ptuning_checkpoint="./PTuning_models/tfp_500/", chatdata={
            "input": "请出一道python判断题，格式固定，内容为字典",
            "chatbot": [], "max_length": 8192, "top_p": 0.8, "temperature": 0.98, "history": []})
        print(data)
        return


    return
#选择题
def Choice(language_p:int = 1,num:int=1):
    return
#填空题
def FillBlank(language_p:int = 1,num:int=1):
    if   language_p == 1:
        return

    elif language_p == 2:
        data = PTuning_main(num=num, ptuning_checkpoint="./PTuning_models/gp5_600/", chatdata={
            "input": "请严格按照与上文相同的格式，必须有以下字段：[题目]，创新生成难度很高的编程填空题目，不能与上文重复或相似,必须有____，不能太简单，答案只能一行",
            "chatbot": [], "max_length": 8192, "top_p": 0.8, "temperature": 0.95, "history": []})
        print(data)
    return
def ExplainCode (language_p:int = 1,num:int=1):
    return
def CodeCompletion (language_p:int = 1,num:int=1):
    return
def BigProgram (language_p:int = 1,num:int=1):
    return
def Algorithm (language_p:int = 1,num:int=1):
    return

def Sort_and_Gen(language_p:int = 1,question_type:str = "Judgment",nums:int = 10):

    function_d = {
        'Judgment': partial(Judgment),
        'Choice': partial(Choice),
        'FillBlank': partial(FillBlank),
        'ExplainCode': partial(ExplainCode),
        'CodeCompletion': partial(CodeCompletion),
        'BigProgram': partial(BigProgram),
        'Algorithm': partial(Algorithm),

        '10': partial(Judgment),
        '20': partial(Choice),
        '30': partial(FillBlank),
        '40': partial(ExplainCode),
        '50': partial(CodeCompletion),
        '60': partial(BigProgram),
        '70': partial(Algorithm),
    }
    # 调用函数
    function_d[question_type](language_p = language_p,num = nums)


if __name__ == "__main__":

    Sort_and_Gen(2,"Judgment",5)