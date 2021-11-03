#!/usr/bin/env python
# -*- coding: utf-8 -*-
import os
CWD = os.path.dirname(os.path.abspath(__file__))
from typing import Dict, Iterator, List, Optional, Union, Literal, Tuple
from tap import Tap
import numpy as np
import pandas as pd


class GenerateArgs(Tap):
    types: List[str] = ['alkane', 'alcohol', 'ketone', 'ether', 'ammounia']
    """The types of molecules to be generated."""
    n_heavy: int = 15
    """The cutoff of the number of heavy atoms."""


class ExportArgs(Tap):
    n_heavy: List[int] = []
    """"""