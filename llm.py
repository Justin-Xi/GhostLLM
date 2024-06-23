"""大模型交互接口封装"""

import time

from openai import AzureOpenAI, OpenAI

MODEL_TYPE = "gpt4"
GPT_MODEL_TYPE = "gpt4turbo"


def inference(model, messages):
    """封装大模型"""
    if model == "gpt4":
        return inference_gpt4(messages, GPT_MODEL_TYPE if GPT_MODEL_TYPE else "gpt4turbo")
    else:
        return inference_self(messages)


def inference_gpt4(messages, model_name="gpt4turbo"):
    """GPT4的模型"""

    def safe_chat_create_with_retry(client, msgs, model=model_name, retry_times=1):
        print(f"🌟使用：{model}")
        for i in range(retry_times):
            try:
                # print(f"发起时间：{time.strftime('%Y年%m月%d日 %H:%M:%S')}")
                time1 = time.time()
                response = client.chat.completions.create(model=model, messages=msgs)
                # print(f"返回时间：{time.strftime('%Y年%m月%d日 %H:%M:%S')}")
                print(f"处理耗时：{time.time()-time1} 秒")
                msg = response.choices[0]
                # print(msg)
                if msg.finish_reason == "content_filter":
                    print("error!content_filter 1!")
                    continue
                return msg
            except Exception as e:
                print("error!content_filter 2!")
                print(e)
                continue
        return None

    def getstr_ai_rt_tool(msg):
        return msg.message.content
        if msg.finish_reason == "content_filter":
            print("error content filter!")
            return None
        if msg.finish_reason == "stop":
            return msg.message.content
        return None

    api_key = "a7d194b6355e4b5b83a47979fe20d245"
    azure_endpoint = "https://loox-eastus2.openai.azure.com/"
    client = AzureOpenAI(api_key=api_key, api_version="2024-02-15-preview", azure_endpoint=azure_endpoint)
    # model_name = "gpt4turbo"
    # model_name = "gpt4o"
    # model_name = "gpt4-32k"
    msg = safe_chat_create_with_retry(client, model=model_name, msgs=messages)
    if msg is None:
        print("GPT返回错误！")
        return ""
    content = getstr_ai_rt_tool(msg)
    if content is None:
        print("error content filter!")
        return ""
    return content


def inference_self(messages):
    """自己部署的模型"""

    client = OpenAI(api_key="123456", base_url="http://10.60.200.102:8000/v1/")
    try:
        response = client.chat.completions.create(
            # model="/mnt/harddisk/haichuan/src/70b/merge_lora",
            # model="/mnt/harddisk/haichuan/src/70b/awq",
            model="/mnt/harddisk/haichuan/models/hub/qwen/Qwen2-72B-Instruct",
            max_tokens=1024,
            messages=messages,
        )
        content = response.choices[0].message.content
    except Exception as e:
        print(e)
        return ""
    return content
