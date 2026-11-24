#!/usr/bin/env python3
"""news-image-20261124 entry (acct1, Masrukhan25).

The image is drawn by build.py and shipped as entry.png beside this file;
this program copies it to /output/entry.png, exactly like the kit starter.
Standard library only. Deterministic: the same bytes every run.

Outside the grader's container, MAKEFUN_OUTPUT_DIR stands in for /output:
    mkdir -p out && MAKEFUN_OUTPUT_DIR=out python3 main.py
"""
import os
import shutil

HERE = os.path.dirname(os.path.abspath(__file__))
OUT_DIR = os.environ.get("MAKEFUN_OUTPUT_DIR", "/output")

os.makedirs(OUT_DIR, exist_ok=True)
shutil.copyfile(os.path.join(HERE, "entry.png"),
                os.path.join(OUT_DIR, "entry.png"))
