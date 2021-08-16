#!/usr/bin/env python
# -*- coding: utf-8 -*-
from .base import *


def create_ketone(n_heavy_cutoff, nO):
    print('\nCreate ketone with %i C=O group SMILES\n' % nO)
    n = 1
    new_category = 'ketone-%i' % nO
    if nO == 1:
        old_category = 'alkane'
    else:
        old_category = 'ketone-%i' % (nO - 1)
    while n < n_heavy_cutoff:
        sys.stdout.write('\r present %i / %i' % (n + 1, n_heavy_cutoff))
        generate_task(n_heavy=n, new_category=new_category, old_category=old_category, generate_type='add', bond_order=2
                      , atom_number=8)
        n += 1
