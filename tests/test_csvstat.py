import io
import json
import os
import sys
import tempfile
import unittest
from contextlib import redirect_stdout

sys.path.insert(0, os.path.dirname(os.path.dirname(os.path.abspath(__file__))))
import csvstat


def run(text, *args):
    with tempfile.NamedTemporaryFile("w", suffix=".csv", delete=False) as f:
        f.write(text)
    try:
        buf = io.StringIO()
        with redirect_stdout(buf):
            csvstat.main([f.name, *args])
        return buf.getvalue()
    finally:
        os.unlink(f.name)


class T(unittest.TestCase):
    def test_types_and_numbers(self):
        h, r = csvstat.read_csv(io.StringIO("a,b,c\n1,1.5,x\n3,,y\n,2.5,x\n"))
        s = csvstat.summarize(r, h)
        self.assertEqual([x["type"] for x in s], ["int", "float", "text"])
        self.assertEqual(s[0]["empty"], 1)
        self.assertEqual(s[0]["mean"], 2)
        self.assertEqual((s[1]["min"], s[1]["max"]), (1.5, 2.5))
        self.assertEqual(s[2]["top"][0], {"value": "x", "count": 2})
        self.assertEqual(s[2]["unique"], 2)

    def test_delimiter_json(self):
        out = json.loads(run("a;b\n1;z\n2;z\n", "-d", ";", "--json"))
        self.assertEqual(out[0]["max"], 2)
        self.assertEqual(out[1]["top"], [{"value": "z", "count": 2}])

    def test_text_output_and_empty_file(self):
        self.assertIn("a (int)", run("a\n1\n"))
        self.assertEqual(run("").strip(), "")

    def test_short_rows(self):
        h, r = csvstat.read_csv(io.StringIO("a,b\n1\n"))
        self.assertEqual(csvstat.summarize(r, h)[1]["empty"], 1)


if __name__ == "__main__":
    unittest.main()
