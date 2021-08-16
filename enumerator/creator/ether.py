#!/usr/bin/env python
# -*- coding: utf-8 -*-
from .base import *


def create_ether(n_heavy_cutoff, nO):
    print('\nCreate ether with %i C-O-C group SMILES\n' % nO)
    n = 1
    new_category = 'ether-%i' % nO
    if nO == 1:
        old_category = 'alkane'
    else:
        old_category = 'ether-%i' % (nO - 1)
    while n <= n_heavy_cutoff:
        sys.stdout.write('\r present %i / %i' % (n, n_heavy_cutoff))
        generate_task(n_heavy=n, new_category=new_category, old_category=old_category, generate_type='replace',
                      old_atom_number=6, new_atom_number=8, connect_number=[2])
        n += 1
