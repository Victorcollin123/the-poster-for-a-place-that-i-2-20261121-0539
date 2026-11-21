#!/usr/bin/env python3
"""VELMARA travel poster entry: copy the poster's image to /output/entry.png.
Deterministic, no network."""
import os
import shutil

HERE = os.path.dirname(os.path.abspath(__file__))


def main():
    os.makedirs("/output", exist_ok=True)
    shutil.copyfile(os.path.join(HERE, "entry.png"), "/output/entry.png")


if __name__ == "__main__":
    main()
