#!/usr/bin/env python
# -*- coding: utf-8 -*-
import os
from typing import Dict, Iterator, List, Optional, Union, Literal, Tuple
from tqdm import tqdm
from enumerator.args import GenerateArgs
from enumerator.database.models import create_table
from enumerator.creator.alkane import create_alkane


def generate(args: GenerateArgs):
    if not os.path.exists(os.path.join('data')):
        os.mkdir('data')
    create_table()
    if 'alkane' in args.types:
        create_alkane(args.n_heavy)


if __name__ == '__main__':
    generate(args=GenerateArgs().parse_args())