"""为json字段起名"""

import argparse
import json
import re

from llm import inference

REG_EXP = r"\(|\)|（|）【|】|\[|\]"


def translate(json_file, model, prompt, output_file):
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
            obj = json.load(input_json)
            for mo in obj:
                if (len(mo.trim())==0):
                    print(f"没有意义的key'{mo}',跳过")
                    continue

                if isinstance(obj[mo], dict):
                    if len(obj[mo]) == 0:
                        print(f"{mo} 字典项没有函数，跳过")
                        continue
                else:
                    print(f"{mo} 非字典项，跳过")

                if re.search(REG_EXP, mo.strip()):
                    print(f"{mo} 跳过")
                    continue

                # if mo.strip() in out:
                #     print(f"{mo} 已经翻译过，跳过")
                #     continue

                to_translate = json.dumps(
                    {mo.strip(): {key: obj[mo][key] for key in obj[mo] if not re.search(REG_EXP, key)}},
                    ensure_ascii=False,
                )
                # print(f"to_translate {to_translate}")
                print(f"处理：{mo}")
                messages = [
                    {"role": "system", "content": prompt_content},
                    {"role": "user", "content": to_translate},
                ]
                reply = inference(model, messages).replace("```json", "").replace("```", "")
                out[mo.strip()] = json.loads(reply).get(mo.strip(), {})
                print(out[mo.strip()])

                with open(output_file, "w", encoding="utf-8") as output:
                    output.write(json.dumps(out, indent=2, ensure_ascii=False))

    except FileNotFoundError:
        print(f"{json_file} or {prompt} is not found")
    except Exception as e:
        print(f"遇到错误 error: {e}")
        print(f"遇到错误 reply: {reply}")


def main():
    """入口"""
    parser = argparse.ArgumentParser(description="用大模型起英文名")
    parser.add_argument("json_file", type=str, help="要命名的json文件")
    parser.add_argument("-m", "--model", type=str, help="模型名称(gpt4)", default="gpt4")
    parser.add_argument("-p", "--prompt", type=str, help="prompt 文件", default="./prompt.txt")
    parser.add_argument("-o", "--output", type=str, help="输出文件名", default="table_data_with_name.json")
    args = parser.parse_args()

    translate(args.json_file, args.model, args.prompt, args.output)


if __name__ == "__main__":
    # main()
    translate("./table_data.json", "gpt4", "./prompt.txt", "table_data_with_name.json")
