#!/usr/bin/env python3
"""csvstat: summarize a CSV file column by column (stdlib only)."""
import argparse
import csv
import json
import sys
from collections import Counter


def _is_int(s):
    try:
        int(s)
        return True
    except ValueError:
        return False


def _is_float(s):
    try:
        float(s)
        return True
    except ValueError:
        return False


def infer_type(values):
    if values and all(_is_int(v) for v in values):
        return "int"
    if values and all(_is_float(v) for v in values):
        return "float"
    return "text"


def summarize(rows, header):
    stats = []
    for i, name in enumerate(header):
        col = [(r[i].strip() if i < len(r) else "") for r in rows]
        vals = [v for v in col if v != ""]
        t = infer_type(vals)
        s = {"column": name, "type": t, "count": len(vals),
             "empty": len(col) - len(vals), "unique": len(set(vals))}
        if t in ("int", "float"):
            nums = [int(v) if t == "int" else float(v) for v in vals]
            s["min"], s["max"] = min(nums), max(nums)
            s["mean"] = sum(nums) / len(nums)
        else:
            s["top"] = [{"value": v, "count": c}
                        for v, c in sorted(Counter(vals).items(),
                                           key=lambda kv: (-kv[1], kv[0]))[:3]]
        stats.append(s)
    return stats


def read_csv(f, delimiter=","):
    reader = csv.reader(f, delimiter=delimiter)
    try:
        header = next(reader)
    except StopIteration:
        return [], []
    return header, list(reader)


def format_text(stats):
    out = []
    for s in stats:
        out.append(f"{s['column']} ({s['type']})")
        out.append(f"  non-empty: {s['count']}  empty: {s['empty']}  unique: {s['unique']}")
        if "mean" in s:
            out.append(f"  min: {s['min']}  max: {s['max']}  mean: {s['mean']:.4g}")
        elif s["top"]:
            out.append("  top: " + ", ".join(f"{t['value']} ({t['count']})" for t in s["top"]))
    return "\n".join(out)


def main(argv=None):
    p = argparse.ArgumentParser(description="Summarize a CSV file.")
    p.add_argument("file", help="CSV file path, or - for stdin")
    p.add_argument("-d", "--delimiter", default=",", help="field delimiter (default ,)")
    p.add_argument("--json", action="store_true", help="output JSON")
    a = p.parse_args(argv)
    if a.delimiter == "\\t":
        a.delimiter = "\t"
    if len(a.delimiter) != 1:
        p.error("delimiter must be a single character")
    if a.file == "-":
        header, rows = read_csv(sys.stdin, a.delimiter)
    else:
        with open(a.file, newline="", encoding="utf-8-sig") as f:
            header, rows = read_csv(f, a.delimiter)
    stats = summarize(rows, header)
    print(json.dumps(stats, indent=2) if a.json else format_text(stats))
    return 0


if __name__ == "__main__":
    sys.exit(main())
