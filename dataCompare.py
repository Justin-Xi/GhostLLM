"""为json字段起名"""

import argparse
import json
import re

from llm import inference

REG_EXP = r"\(|\)|（|）【|】|\[|\]"


def merge(json_file, json_file1, model, prompt, output_file):
    """模块名、函数名、参数翻译"""
    with open(prompt, "r", encoding="utf-8") as prompt:
        prompt_content = prompt.read()

    try:
        with open(output_file, "r", encoding="utf-8") as output:
            try:
                out = json.load(output)
            except Exception as e:
                print(e)
                out = {}
    except FileNotFoundError:
        out = {}

    try:
        with open(json_file, "r", encoding="utf-8") as input_json:
            obj1 = json.load(input_json)
        with open(json_file1, "r", encoding="utf-8") as input_json1:
            obj2 = json.load(input_json1)
        ob = {**obj1, **obj2}
        message = json.dumps(ob, indent=4, ensure_ascii=False)
        messages = [
            {"role": "system", "content": prompt_content},
            {"role": "user", "content": ob},
        ]
        reply = inference(model, messages).replace("```json", "").replace("```", "")
        with open(output_file, "w", encoding="utf-8") as output:
            output.write(reply)

    except FileNotFoundError:
        print(f"{json_file} or {prompt} is not found")
    except Exception as e:
        print(f"遇到错误 error: {e}")

def main():
    """入口"""
    parser = argparse.ArgumentParser(description="用大模型起英文名")
    parser.add_argument("json_file", type=str, help="table_data_with_name.json")
    parser.add_argument("json_file1", type=str, help="test_spec.json")
    parser.add_argument("-m", "--model", type=str, help="模型名称(gpt4)", default="gpt4")
    parser.add_argument("-p", "--prompt", type=str, help="prompt 文件", default="./prompt.txt")
    parser.add_argument("-o", "--output", type=str, help="输出文件名", default="table_data_with_name.json")
    args = parser.parse_args()

    merge(args.json_file, args.json_file1, args.model, args.prompt, args.output)


if __name__ == "__main__":
    # main()
    merge("./table_data_with_name.json","./test_spec.json", "gpt4", "./prompt2.txt", "new.json")
