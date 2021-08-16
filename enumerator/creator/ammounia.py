#!/usr/bin/env python
# -*- coding: utf-8 -*-
from .base import *


def create_ammounia(n_heavy_cutoff, nN):
    print('\nCreate SMILES: ammounia with %i N\n' % nN)
    n = 1
    new_category = 'ammounia-%i' % nN
    if nN == 1:
        old_category = 'alkane'
    else:
        old_category = 'ammounia-%i' % (nN - 1)
    while n <= n_heavy_cutoff:
        sys.stdout.write('\r present %i / %i' % (n, n_heavy_cutoff))
        generate_task(n_heavy=n, new_category=new_category, old_category=old_category, generate_type='replace',
                      old_atom_number=6, new_atom_number=7, connect_number=[1, 2, 3])
        n += 1
