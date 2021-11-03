#!/usr/bin/env python
# -*- coding: utf-8 -*-
from .base import *


def create_alkane(n_heavy):
    growing_from_smiles(n_heavy, 'C', category='alkane')


def create_cyclic_alkane(n_heavy):
    growing_from_smiles(n_heavy, 'C1CCCC1', category='5-member ring alkane')
    growing_from_smiles(n_heavy, 'C1CCCCC1', category='6-member ring alkane')