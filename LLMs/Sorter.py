import Gendemo
from functools import partial
import api
import argparse

parser = argparse.ArgumentParser(description='web_demo参数解析')

# 添加参数
parser.add_argument('--question_type', type=str, help='生成题型调整')
parser.add_argument('--programming_language', type=str, help='调整编程语言')
parser.add_argument('--number_of_questions', type=int, help='生成题目数量')
parser.add_argument('--output_filename', type=str, help='保存为json格式的文件名')
parser.add_argument('--model_quantization', type=int, help='模型量化')
parser.add_argument('--content', type=str, help='题目内容')

# 解析参数
args = parser.parse_args()

PTuning_main = Gendemo.PTuning_main
api = api.use_Api


# 判断题
def Judgment(language_p: int = 1, num: int = 1, content1: str = ""):
    if language_p == 1:
        data = PTuning_main(num=num, ptuning_checkpoint="./ChatGLM2-6B/PTuning_models/tfc_500/", chatdata={
            "input": "请出一道C++判断题，格式固定",
            "chatbot": [], "max_length": 8192, "top_p": 0.8, "temperature": 0.95, "history": []})
        print(data)

        return

    elif language_p == 2:
        data = PTuning_main(num=num, ptuning_checkpoint="./ChatGLM2-6B/PTuning_models/tfp_500/", chatdata={
            "input": "请出一道python判断题，格式固定，内容为字典",
            "chatbot": [], "max_length": 8192, "top_p": 0.8, "temperature": 0.98, "history": []})
        print(data)
        return


# 选择题
def Choice(language_p: int = 1, num: int = 1, content1=""):
    if language_p == 1:
        data = api([
            {"role": "system", "content": "你是一名人工智能出题助手，负责以如下格式生成编程选择题目，编程语言为C++"},
            {"role": "user",
             "content": "请严格按照与上文相同的格式，生成”难度很高“的编程选择题目"},
            {"role": "assistant",
             "content": "[题目] 在C++中，关于类的静态变量成员，以下哪项描述是正确的？\nA. 静态变量成员在每个对象实例中都有自己的独立副本。\nB. 静态变量成员在类定义外部初始化时，不需要使用作用域解析运算符。\nC. 静态变量成员的存储是按照类类型分配的，而不是按照对象实例分配的。\nD. 静态变量成员只能在类的静态成员函数内部访问。\n[答案] C [解析] 静态变量成员的存储是按照类类型分配的，而不是按照对象实例分配的。这意味着所有对象共享同一个静态变量成员，而不是每个对象都有自己的副本。"},
            {"role": "user",
             "content": "请严格按照与上文相同的格式，生成”难度很高“的编程选择题目"},
            {"role": "assistant",
             "content": "[题目] 设A是一个有不带参数的构造函数的类，fun是一个如下定义的函数：Afun(A&a){returna;}则在执行程序段{Aa; fun(a); }时，对A类的：①构造函数，②析构函数，③拷贝构造函数的调用顺序是（ ）\nA. ①③③②②②\nB. ①③②②\nC. ①②③② \nD. ①②③③②②\n[做题依据] 在执行程序段{A a; fun(a); }时，首先调用A类的构造函数①创建对象a，然后调用fun函数，由于fun函数的参数是引用类型，所以不会调用拷贝构造函数，但是fun函数的返回值是对象类型，所以会调用拷贝构造函数③创建一个临时对象，然后将这个临时对象赋值给fun函数的调用者，由于这里没有接收fun函数的返回值，所以这个临时对象会被立即销毁，调用析构函数②，最后在程序段结束时，对象a也会被销毁，调用析构函数②。因此，对A类的构造函数，析构函数，拷贝构造函数的调用顺序是①③②②，选项B正确\n[答案] B"},
            {"role": "user",
             "content": "请严格按照与上文相同的格式，创新生成难度很高的一道编程选择题目，不能与上文重复或相似,考察内容为" + content1 + "，不能太简单，单选多选都可"}
        ])
        print(data)
    elif language_p == 2:
        data = api([
            {"role": "system", "content": "你是一名人工智能出题助手，负责以如下格式生成编程选择题目，编程语言为Python"},
            {"role": "user",
             "content": "请严格按照与上文相同的格式，生成”难度很高“的编程选择题目"},
            {"role": "assistant",
             "content": "[题目] 关于__name__的说法，下列描述错误的是( )。\nA.它是Python提供的一个方法\nB.每个模块内部都有一个__name__属性\nC.当它的值为’main‘时，表示模块自身在运行\nD.当它的值不为’main’时，表示模块被引用\n[答案] A \n[解析] 选项A描述错误。在Python中，__name__是一个特殊的属性，而不是一个方法。"},
            {"role": "user",
             "content": "请严格按照与上文相同的格式，创新生成难度很高的一道编程选择题目，不能与上文重复或相似,考察内容为" + content1 + "，不能太简单，单选多选都可"}
        ])
        print(data)


# 填空题
def FillBlank(language_p: int = 1, num: int = 1, content1: str = ""):
    if language_p == 1:
        data = api([
            {"role": "system", "content": "你是一名人工智能出题助手，负责以如下格式生成程序填空题目，编程语言为C++"},
            {"role": "user",
             "content": "请严格按照与上文相同的格式，生成”难度很高“的程序解释题目"},
            {"role": "assistant",
             "content": "[题目] C++的标识符由字母、____________和数字组成，而且第一个字符不能为数字。\n\n[答案] 下划线"},
            {"role": "user",
             "content": "请严格按照与上文相同的格式，生成”难度很高“的程序解释题目"},
            {"role": "assistant",
             "content": "[题目] 为了避免在嵌套的条件语句if-else中产生二义性，C++规定：else子句总是与______配对。\n\n[答案]其前面最近的if。"},
            {"role": "user",
             "content": "请严格按照与上文相同的格式，创新生成难度很高的一道程序解释题目，不能与上文重复或相似,考察内容为" + content1}
        ])
        print(data)
        return

    elif language_p == 2:
        data = PTuning_main(num=num, ptuning_checkpoint="./ChatGLM2-6B/PTuning_models/gp5_600/", chatdata={
            "input": "请严格按照与上文相同的格式，必须有以下字段：[题目]，创新生成难度很高的编程填空题目，不能与上文重复或相似,必须有____，不能太简单，答案只能一行",
            "chatbot": [], "max_length": 8192, "top_p": 0.8, "temperature": 0.95, "history": []})
        print(data)
    return


def ExplainCode(language_p: int = 1, num: int = 1, content1: str = ""):
    if language_p == 1:
        data = api([
            {"role": "system", "content": "你是一名人工智能出题助手，负责以如下格式生成程序填空题目，编程语言为C++"},
            {"role": "user",
             "content": "请严格按照与上文相同的格式，生成”难度很高“的程序解释题目"},
            {"role": "assistant",
             "content": "[题目] 有以下C++程序段：\n#include \n\nclass Temperature {\npublic:\n static double celsiusTo Fahrenheit(double celsius) {\n return celsius * 9.0 / 5.0 + 32.0;\n }\n};\n\nint main() {\n double celsius = 25.0;\n double fahrenheit = Temperature::celsiusToFahrenheit(celsius);\n std::cout << celsius << \" degrees Celsius is \" << fahrenheit << \" degrees Fahrenheit.\" << std::endl;\n return 0;\n}\n这个程序的主要功能是什么？\n\n[答案] 这个程序的主要功能是将摄氏温度转换为华氏温度。程序定义了一个名为 Temperature 的类，其中包含一个静态成员函数 celsiusToFahrenheit，该函数接受一个摄氏温度值作为参数，并返回对应的华氏温度值。转换公式是 Fahrenheit = Celsius * 9.0 / 5.0 + 32.0"},
            {"role": "user",
             "content": "请严格按照与上文相同的格式，创新生成难度很高的一道程序解释题目，不能与上文重复或相似,考察内容为" + content1}
        ])
        print(data)
        return

    elif language_p == 2:
        data = api([
            {"role": "system", "content": "你是一名人工智能出题助手，负责以如下格式生成程序填空题目，编程语言为C++"},
            {"role": "user",
             "content": "请严格按照与上文相同的格式，生成”难度很高“的程序填空题目"},
            {"role": "assistant",
             "content": "[题目] 有以下Python程序段：\nclass Player:\n    def __init__(self, name, level):\n        self.name = name\n        self.level = level\n\n    def get_stats(self):\n        return {\"name\": self.name, \"level\": self.level}\n\nplayer1 = Player(\"Alice\", 10)\nplayer_stats = player1.get_stats()\nprint(f\"Player {player_stats['name']} is at level {player_stats['level']}.\")\n这个程序的主要功能是什么？\n\n[答案] 这个程序的主要功能是创建一个玩家对象，并获取其统计信息。程序定义了一个名为 Player 的类，该类有两个属性：name 和 level，分别代表玩家的名字和等级。类中还有一个方法 get_stats，该方法返回一个包含玩家名字和等级的字典。"},
            {"role": "user",
             "content": "请严格按照与上文相同的格式，创新生成难度很高的一道程序解释题目，不能与上文重复或相似,考察内容为" + content1}
        ])
        print(data)
        return
    return


def CodeCompletion(language_p: int = 1, num: int = 1, content1: str = ""):
    if language_p == 1:
        data = api([
            {"role": "system", "content": "你是一名人工智能出题助手，负责以如下格式生成编程题目，编程语言为python"},
            {"role": "user",
             "content": "请严格按照与上文相同的格式，但内容不可一样，生成”难度很高“的编程填空题目，要求考生根据[功能]补全[题目]中缺失的一行代码，需要你在出题时扣去并用___代替，题目答案的考察内容为重载运算符"},
            {"role": "assistant",
             "content": "[题目]#include <iostream>\nusing namespace std;\n\nclass Complex {\nprivate:\n    int real, imag;\npublic:\n    Complex(int r = 0, int i = 0) : real(r), imag(i) {}\n\n    Complex operator+(const Complex &obj) {\n        Complex res;\n        ______________  //需要考生填空\n        res.imag = imag + obj.imag;\n        return res;\n    }\n\n    friend ostream & operator<<(ostream &output, const Complex &obj) {\n        output << obj.real << \"+\" << obj.imag << \"i\";\n        return output;\n    }\n};\n\nint main() {\n    Complex c1(3, 4), c2(5, 6);\n    Complex c3 = c1 + c2;\n    cout << c3;\n    return 0;\n}\n\n\n[功能]\n在上述程序中，通过重载运算符，使得两个Complex对象可以相加。请补全上述程序中的一行，使得程序能够正确编译运行，并输出正确的结果。\n\n[答案] :\nres.real = real + obj.real;"},
            {"role": "user",
             "content": "请严格按照与上文相同的格式，但内容不可一样，现在语言改为python，生成”难度很高“的编程填空题目，要求考生根据[功能]补全[题目]中缺失的一行代码，需要你在出题时扣去并用___代替，考点必须为" + content1 + ""}
        ])
        print(data)
        return

    elif language_p == 2:
        data = api([
            {"role": "system", "content": "你是一名人工智能出题助手，负责以如下格式生成程序填空题目，编程语言为C++"},
            {"role": "user",
             "content": "请严格按照与上文相同的格式，生成”难度很高“的程序填空题目"},
            {"role": "assistant",
             "content": "[题目] 有以下Python程序段：\nclass Player:\n    def __init__(self, name, level):\n        self.name = name\n        self.level = level\n\n    def get_stats(self):\n        return {\"name\": self.name, \"level\": self.level}\n\nplayer1 = Player(\"Alice\", 10)\nplayer_stats = player1.get_stats()\nprint(f\"Player {player_stats['name']} is at level {player_stats['level']}.\")\n这个程序的主要功能是什么？\n\n[答案] 这个程序的主要功能是创建一个玩家对象，并获取其统计信息。程序定义了一个名为 Player 的类，该类有两个属性：name 和 level，分别代表玩家的名字和等级。类中还有一个方法 get_stats，该方法返回一个包含玩家名字和等级的字典。"},
            {"role": "user",
             "content": "请严格按照与上文相同的格式，创新生成难度很高的一道程序解释题目，不能与上文重复或相似,考察内容为" + content1}
        ])
        print(data)
        return
    return


def BigProgram(language_p: int = 1, num: int = 1):
    return


def Algorithm(language_p: int = 1, num: int = 1):
    data = PTuning_main(num=num, ptuning_checkpoint="./ChatGLM2-6B/PTuning_models/cf_500/", chatdata={
        "input": "请出一道编程算法题目，只出题干，不包括解题过程,格式一致",
        "chatbot": [], "max_length": 8192, "top_p": 0.8, "temperature": 0.98, "history": []})
    print(data)
    return


def test(language_p: int = 1, num: int = 1):
    data = PTuning_main(num=num, ptuning_checkpoint="./ChatGLM2-6B3/ptuning/output5/checkpoint-50/", chatdata={
        "input": "请出一道复杂的算法题",
        "chatbot": [], "max_length": 8192, "top_p": 0.8, "temperature": 0.98, "history": []})
    print(data)
    return


def Sort_and_Gen(language_p: int = 1, question_type: str = "Judgment", nums: int = 1, content1: str = ""):
    function_d = {
        'Judgment': partial(Judgment),
        'Choice': partial(Choice),
        'FillBlank': partial(FillBlank),
        'ExplainCode': partial(ExplainCode),
        'CodeCompletion': partial(CodeCompletion),
        'BigProgram': partial(BigProgram),
        'Algorithm': partial(Algorithm),
        'test': partial(test),

        '10': partial(Judgment),
        '20': partial(Choice),
        '30': partial(FillBlank),
        '40': partial(ExplainCode),
        '50': partial(CodeCompletion),
        '60': partial(BigProgram),
        '70': partial(Algorithm),

    }
    # 调用函数
    function_d[question_type](language_p=language_p, num=nums)


if __name__ == "__main__":
    # Sort_and_Gen(1, "Judgment", 1,"列表推导式")

    if args.programming_language == "C++":
        language_p = 1
    elif args.programming_language == "Python":
        language_p = 2

    print(args.question_type)
    Sort_and_Gen(language_p, args.question_type, args.number_of_questions, args.content)
