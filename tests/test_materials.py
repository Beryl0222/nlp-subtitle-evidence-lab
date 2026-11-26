"""合成资料结构及诊断测试。"""
import unittest
from materials import load, validate

class MaterialsTest(unittest.TestCase):
    def test_pack_is_connected_and_readable(self):
        groups = load()
        counts = validate(groups)
        self.assertGreater(len(counts), 1)
        self.assertTrue(all(n > 0 for n in counts.values()))

    def test_missing_reference_is_rejected(self):
        with self.assertRaisesRegex(ValueError, "引用不存在"):
            validate({"x": [{"id": "x1", "refs": ["missing"]}]})

    def test_unicode_offsets_use_characters(self):
        row = {"id": "x1", "text": "阿青说：我没去。", "spans": [{"start": 4, "end": 7, "text": "我没去"}]}
        validate({"x": [row]})
        row["spans"][0]["end"] = 8
        with self.assertRaisesRegex(ValueError, "跨度与原文不符"):
            validate({"x": [row]})
