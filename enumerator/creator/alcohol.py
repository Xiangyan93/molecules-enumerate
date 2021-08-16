#!/usr/bin/env python
# -*- coding: utf-8 -*-
from .base import *


def create_alcohol(n_heavy_cutoff, nOH):
    print('\nCreate SMILES: alcohol with %i hydroxyl group\n' % nOH)
    n = 1
    new_category = 'alcohol-%i' % nOH
    if nOH == 1:
        old_category = 'alkane'
    else:
        old_category = 'alcohol-%i' % (nOH - 1)
    while n < n_heavy_cutoff:
        sys.stdout.write('\r present %i / %i' % (n + 1, n_heavy_cutoff))
        generate_task(n_heavy=n, new_category=new_category, old_category=old_category, generate_type='add',
                      bond_order=1,
                      atom_number=8)
        n += 1
