#!/usr/bin/env python
# -*- coding: utf-8 -*-
from .base import *


def create_3ring_1(n_heavy):
    growing_from_smiles(n_heavy, 'C1CC1', category='alkane-3ring')


def create_4ring_1(n_heavy):
    growing_from_smiles(n_heavy, 'C1CCC1', category='alkane-4ring')


def create_5ring_1(n_heavy):
    growing_from_smiles(n_heavy, 'C1CCCC1', category='alkane-5ring')


def create_6ring_1(n_heavy):
    growing_from_smiles(n_heavy, 'C1CCCCC1', category='alkane-6ring')


def create_7ring_1(n_heavy):
    growing_from_smiles(n_heavy, 'C1CCCCCC1', category='alkane-7ring')


def create_8ring_1(n_heavy):
    growing_from_smiles(n_heavy, 'C1CCCCCCC1', category='alkane-8ring')


def create_9ring_1(n_heavy):
    growing_from_smiles(n_heavy, 'C1CCCCCCCC1', category='alkane-9ring')


def create_10ring_1(n_heavy):
    growing_from_smiles(n_heavy, 'C1CCCCCCCCC1', category='alkane-10ring')


def create_11ring_1(n_heavy):
    growing_from_smiles(n_heavy, 'C1CCCCCCCCCC1', category='alkane-11ring')


def create_12ring_1(n_heavy):
    growing_from_smiles(n_heavy, 'C1CCCCCCCCCCC1', category='alkane-12ring')


def create_13ring_1(n_heavy):
    growing_from_smiles(n_heavy, 'C1CCCCCCCCCCCC1', category='alkane-13ring')


def create_14ring_1(n_heavy):
    growing_from_smiles(n_heavy, 'C1CCCCCCCCCCCCC1', category='alkane-14ring')


def create_15ring_1(n_heavy):
    growing_from_smiles(n_heavy, 'C1CCCCCCCCCCCCCC1', category='alkane-15ring')


def create_ring_ring(n_heavy):
    ring_list = ['C1CC1', 'C1CCC1', 'C1CCCC1', 'C1CCCCC1', 'C1CCCCCC1', 'C1CCCCCCC1']
    for i, r1 in enumerate(ring_list):
        for j in range(i, len(ring_list)):
            r2 = ring_list[j]
            smiles = r1 + r2
            smiles1 = r1 + 'C' + r2
            smiles2 = r1 + 'CC' + r2
            smiles3 = r1 + 'CCC' + r2
            growing_from_smiles(n_heavy, smiles, category='%iring-%iring' % (i + 3, j + 3))
            growing_from_smiles(n_heavy, smiles1, category='%iring-C-%iring' % (i + 3, j + 3))
            growing_from_smiles(n_heavy, smiles2, category='%iring-CC-%iring' % (i + 3, j + 3))
            growing_from_smiles(n_heavy, smiles3, category='%iring-CCC-%iring' % (i + 3, j + 3))
    for i, r1 in enumerate(ring_list):
        r2 = 'c1ccccc1'
        smiles = r1 + r2
        smiles1 = r1 + 'C' + r2
        smiles2 = r1 + 'CC' + r2
        smiles3 = r1 + 'CCC' + r2
        growing_from_smiles(n_heavy, smiles, category='benzene-%iring' % (i + 3))
        growing_from_smiles(n_heavy, smiles1, category='benzene-C-%iring' % (i + 3))
        growing_from_smiles(n_heavy, smiles2, category='benzene-CC-%iring' % (i + 3))
        growing_from_smiles(n_heavy, smiles3, category='benzene-CCC-%iring' % (i + 3))


def create_ring_ring_1(n_heavy):
    ring_list = ['C1CC1', 'C1CCC1', 'C1CCCC1', 'C1CCCCC1', 'C1CCCCCC1', 'C1CCCCCCC1']
    ring_list2 = ['2CC2', '2CCC2', '2CCCC2', '2CCCCC2', '2CCCCCC2', '2CCCCCCC2']
    for i, r1 in enumerate(ring_list):
        for j in range(i, len(ring_list)):
            r2 = ring_list2[j]
            smiles = r1 + r2
            growing_from_smiles(n_heavy, smiles, category='%iring.%iring' % (i + 3, j + 3))


def create_ring_ring_2(n_heavy):
    ring_list = ['', 'C', 'CC', 'CCC', 'CCCC', 'CCCCC']
    for i, r1 in enumerate(ring_list):
        for j in range(i, len(ring_list)):
            r2 = ring_list[j]
            smiles = 'C1' + r1 + '2C(C1)C' + r2 + '2'
            growing_from_smiles(n_heavy, smiles, category='%iring..%iring' % (i + 3, j + 3))
    ring_list = ['C1', 'C1C', 'C1CC', 'C1CCC', 'C1CCCC', 'C1CCCCC']
    for i, r1 in enumerate(ring_list):
        r2 = 'c2c1cccc2'
        smiles = r1 + r2
        growing_from_smiles(n_heavy, smiles, category='benzene..%iring' % (i + 3))


def create_ring_alkene_1(n_heavy):
    backbones = []
    for i in range(3, 14):
        backbones += ['alkane-%iring' % (i)]

    for i in range(3, 9):
        for j in range(3, 9):
            backbones += ['%iring-%iring' % (i, j)]
            backbones += ['%iring-C-%iring' % (i, j)]
            backbones += ['%iring-CC-%iring' % (i, j)]
            backbones += ['%iring-CCC-%iring' % (i, j)]
            backbones += ['%iring.%iring' % (i, j)]
            backbones += ['%iring..%iring' % (i, j)]

    for i in range(3, 9):
        backbones += ['benzene-%iring' % (i)]
        backbones += ['benzene-C-%iring' % (i)]
        backbones += ['benzene-CC-%iring' % (i)]
        backbones += ['benzene-CCC-%iring' % (i)]

    print('\nCreate cyclic alkene with single double bond SMILES\n')
    category = 'ring-alkene-1'
    n = n_heavy
    id = 5
    while id <= n:
        sys.stdout.write('\r present %i / %i' % (id, n))
        tasks_all = session.query(Task)
        tasks = tasks_all.filter(Task.category == category).filter(Task.n_heavy == id)
        if tasks.count() == 0:
            tasks = tasks_all.filter(Task.category.in_(backbones)).filter(Task.n_heavy == id)
            smiles_list = []
            for task in tasks:
                smiles_list += json.loads(task.smiles_list)
            add_double_bond(smiles_list, category=category)
        id += 1


def create_ring_alkene_2(n_heavy):
    print('\nCreate cyclic alkene with two double bond SMILES\n')
    category = 'ring-alkene-2'
    n = n_heavy
    id = 5
    while id <= n:
        sys.stdout.write('\r present %i / %i' % (id, n))
        tasks_all = session.query(Task)
        tasks = tasks_all.filter(Task.category == category).filter(Task.n_heavy == id)
        if tasks.count() == 0:
            tasks = tasks_all.filter(Task.category == 'ring-alkene-1').filter(Task.n_heavy == id)
            smiles_list = []
            for task in tasks:
                smiles_list += json.loads(task.smiles_list)
            add_double_bond(smiles_list, category=category)
        id += 1


def create_ring_alkene_3(n_heavy):
    print('\nCreate cyclic alkene with three double bond SMILES\n')
    category = 'ring-alkene-3'
    n = n_heavy
    id = 6
    while id <= n:
        sys.stdout.write('\r present %i / %i' % (id, n))
        tasks_all = session.query(Task)
        tasks = tasks_all.filter(Task.category == category).filter(Task.n_heavy == id)
        if tasks.count() == 0:
            tasks = tasks_all.filter(Task.category == 'ring-alkene-2').filter(Task.n_heavy == id)
            smiles_list = []
            for task in tasks:
                smiles_list += json.loads(task.smiles_list)
            add_double_bond(smiles_list, category=category)
        id += 1
