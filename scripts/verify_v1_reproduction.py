#!/usr/bin/env python3
"""Verify V1 final-curation reproducibility.

Usage:
  python verify_v1_reproduction.py dataset_omnetpp_P.csv dataset_omnetpp_cleaned_2.csv
"""
from pathlib import Path
import importlib.util
import tempfile
import pandas as pd
import sys

source=Path(sys.argv[1])
published=Path(sys.argv[2])
cleaner=Path(__file__).with_name("clean_dataset_final.py")

spec=importlib.util.spec_from_file_location("cleaner",cleaner)
mod=importlib.util.module_from_spec(spec)
spec.loader.exec_module(mod)

with tempfile.TemporaryDirectory() as td:
    out=Path(td)/"reconstructed.csv"
    reconstructed=mod.clean(str(source),str(out))
    target=pd.read_csv(published)
    print("ROWS_RECONSTRUCTED",len(reconstructed))
    print("ROWS_PUBLISHED",len(target))
    print("VALUE_LEVEL_EQUAL",reconstructed.equals(target))
    if not reconstructed.equals(target):
        raise SystemExit(1)
