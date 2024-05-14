

# 智舟题海

ProjectName and Description

<!-- PROJECT SHIELDS -->


<!-- PROJECT LOGO -->
<br />

<p align="center">
  <a href="https://github.com/Lichen455/ZTO/blob/main/img/zrx.png">
    <img src="img/zrx.png" alt="Logo" width="245" height="80">
  </a>

  <h3 align="center">智舟题海 - AI</h3>
  <p align="center">
    基于LLM的试题生成器
    <br />
    <a href="https://github.com/shaojintian/Best_README_template"><strong>探索本项目的文档 »</strong></a>
    <br />
    <br />
    <a href="https://github.com/shaojintian/Best_README_template">查看Demo</a>
    ·
    <a href="https://github.com/shaojintian/Best_README_template/issues">报告Bug</a>
    ·
    <a href="https://github.com/shaojintian/Best_README_template/issues">提出新特性</a>
  </p>



 本篇README.md面向开发者
 
## 目录

- [上手指南](#上手指南)
  - [开发前的配置要求](#开发前的配置要求)
  - [安装步骤](#安装步骤)
- [文件目录说明](#文件目录说明)
- [开发的架构](#开发的架构)
- [部署](#部署)
- [使用到的框架](#使用到的框架)
- [贡献者](#贡献者)
  - [如何参与开源项目](#如何参与开源项目)
- [版本控制](#版本控制)
- [作者](#作者)
- [鸣谢](#鸣谢)

### 上手指南

###### 开发前的配置要求

显存 > 23G

若不满足条件，请考虑量化（量化所需内存参考ChatGLM2-6B），或者进行纯API调用

###### **安装步骤**

```sh
git clone git@github.com:Lichen455/ZTO.git

pip install -r requirements.txt
```
cudnn torch 等建议单独安装

需要下载 ChatGLM2-6B 模型文件，考虑所需微调模型多，分开进行储存

###### 如何使用

您可以通过LLMs文件夹下的 start.sh 与 start_test.sh脚本进行调用

```
cd LLMs
bash start.sh
```

```sh
usage() {
    echo "Usage: $0 --question_type <type> --programming_language <language> --number_of_questions <num> --output_filename <file> --model_quantization <4|8> --content <str>"
    exit 1
}
export GLM_APIKEY="a12935687eac698a342e739c4820ac4c.wor32LL9tJN0voEY"

python3 Sorter.py \
    --question_type "Judgment" \
    --programming_language "C++" \
    --number_of_questions 31 \
    --output_filename "n" \
    --model_quantization 8 \
    --content "类" \

 : '
question_type 题型
  填入英文和数字都可以
  10 / Judgment->通用判断题
  20 / Choice->通用选择题
  30 / FillBlank->通用填空题
  40 / ExplainCode->解释程序题
  50 / CodeCompletion->程序填空题（补全程序）
  
  70 / Algorithm->算法题

programming_language 语言
可填 C++ or Python

number_of_questions 题目数量 int

output_filename 若输出为一个json文件，该文件的名称

model_quantization 若加载模型，模型量化 4 or 8

content 出题相关内容

GLM_APIKEY 需要的智谱AI GLM的APIkey
'
```


### 文件目录说明

```
├── img
└── LLMs
    ├── ChatGLM2-6B
        ├── evaluation
        ├── ptuning
        │   ├── dataset
        │   └── __pycache__
        ├── PTuning_models

```





### 开发的架构 

### 部署

pip install -r requirements.txt

cudnn torch 等建议单独安装

### 使用到的框架


### 贡献者

伟大转圈鸽子

#### 如何参与开源项目

贡献使开源社区成为一个学习、激励和创造的绝佳场所。你所作的任何贡献都是**非常感谢**的。


1. 什么还有人参加这个项目？



### 版本控制

该项目使用Git进行版本管理。您可以在repository参看当前可用版本。

### 作者

黎晨

Q 2425113174   

 *您也可以在贡献者名单中参看所有参与该项目的开发者。*

### 开源协议

Apache License 2.0

### 鸣谢






