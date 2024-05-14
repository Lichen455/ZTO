usage() {
    echo "Usage: $0 --question_type <type> --programming_language <language> --number_of_questions <num> --output_filename <file> --model_quantization <4|8> --content <str>"
    exit 1
}
export GLM_APIKEY="a12935687eac698a342e739c4820ac4c.wor32LL9tJN0voEY" \
export GLM_6B_PATH="/data/models/chatglm2/"
python3 Sorter.py \
    --question_type "Judgment" \
    --programming_language "Python" \
    --number_of_questions 2 \
    --output_filename "ss.json" \
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