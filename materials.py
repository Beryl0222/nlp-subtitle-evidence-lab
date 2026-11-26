"""读取及检查合成资料；不进行业务推断。"""
import json
from pathlib import Path

ROOT = Path(__file__).resolve().parent

def load(directory=None):
    """返回文件名到记录列表的映射。"""
    base = Path(directory) if directory is not None else ROOT / "data"
    result = {}
    for path in sorted(base.glob("*.json")):
        rows = json.loads(path.read_text(encoding="utf-8"))
        if not isinstance(rows, list):
            raise ValueError(f"资料必须是记录列表：{path.name}")
        result[path.name] = rows
    if not result:
        raise ValueError("未找到资料")
    return result

def validate(groups):
    """检查记录身份及明确声明的跨文件引用。"""
    ids = set()
    for name, rows in groups.items():
        for row in rows:
            if not isinstance(row, dict) or not isinstance(row.get("id"), str):
                raise ValueError(f"记录缺少字符串 id：{name}")
            if row["id"] in ids:
                raise ValueError(f"记录身份重复：{row['id']}")
            ids.add(row["id"])
            for span in row.get("spans", []):
                start, end = span["start"], span["end"]
                if not 0 <= start < end <= len(row["text"]):
                    raise ValueError(f"跨度越界：{row['id']}")
                if row["text"][start:end] != span["text"]:
                    raise ValueError(f"跨度与原文不符：{row['id']}")
    for rows in groups.values():
        for row in rows:
            for target in row.get("refs", []):
                if target not in ids:
                    raise ValueError(f"引用不存在：{row['id']} -> {target}")
    return {name: len(rows) for name, rows in groups.items()}

if __name__ == "__main__":
    print(json.dumps(validate(load()), ensure_ascii=False, sort_keys=True))
