# 影视台词复用的文本证据与授权片段核对

用于影视台词复用的文本证据与授权片段核对的本地合成资料集。所有人名、机构、产品和业务记录均为虚构，不能据此推断真实个人或机构。

资料位于 `data/`，字段语义见 [资料格式](docs/资料格式.md)。`materials.py` 提供 JSON 资料读取和结构检查，可供后续业务程序调用；当前检查范围是编码、记录身份、引用和人工跨度，不包含文本推断结果。

运行环境为 Python 3.11，依赖固定在 `requirements.txt`。安装依赖后，可执行 `python3 materials.py` 检查资料，使用 `python3 -m unittest discover -s tests -v` 运行资料测试。运行期间不需要网络；文本为 UTF-8，持久化目录由业务调用者指定。

资料读取示例：

```python
from materials import load
records = load()
print({name: len(rows) for name, rows in records.items()})
```

人工跨度使用 Python Unicode 字符下标的半开区间，不是 UTF-8 字节下标。原文包含空格、标点和换行时仍按原文计数。文件可在独立副本中替换以检查其他资料。
