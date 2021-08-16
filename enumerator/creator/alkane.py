#!/usr/bin/env python
# -*- coding: utf-8 -*-
from .base import *


def create_alkane(n_heavy):
    growing_from_smiles(n_heavy, 'C', category='alkane')
