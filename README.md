- 安装依赖
  - 假设你已经有一个conda环境，并且已经激活 `conda install --file requirements.txt`
  - 或者 `pip install -r requirements.txt`

- 用大模型为函数起名
  - `python name_it.py`

- 输出文件
  - `table_data_with_name.json`

这个json文件用于产品经理定义的函数与我们程序使用的函数映射，我们需要维护一套程序使用的函数列表，函数名、参数通过这个映射文件保持同步。

```json
{
  "独立 Agent": {
    "name": "IndependentAgent",
    "用户数据搜索 Agent": {
      "name": "UserDataSearchAgent",
      "搜索需求": {
        "name": "SearchRequirement",
        "字段描述": "用一段自然语言，描述需要的搜索需求",
        "数据格式": "纯文本",
        "是否必填": "是"
      }
    }
  }
}
```

第一级key是模块，第二级key是函数，第三级key是参数。

上述文件中，"独立 Agengt"是模块，"用户数据搜索 Agent"是函数，"搜索需求"是函数参数，再往后是针对参数的说明。
