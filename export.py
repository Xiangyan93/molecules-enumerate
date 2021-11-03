#!/usr/bin/env python
# -*- coding: utf-8 -*-
import os
from typing import Dict, Iterator, List, Optional, Union, Literal, Tuple
from tqdm import tqdm
import pandas as pd
from enumerator.args import ExportArgs
from enumerator.database.models import *
from enumerator.creator.alkane import create_alkane


def export(args: ExportArgs):
    smiles = []
    for task in session.query(Task):
        if args.n_heavy[0] <= task.n_heavy <= args.n_heavy[1]:
            smiles += json.loads(task.smiles_list)
    pd.DataFrame({'smiles': smiles}).to_csv('smiles.csv', index=False)


if __name__ == '__main__':
    export(args=ExportArgs().parse_args())
