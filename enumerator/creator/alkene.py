#!/usr/bin/env python
# -*- coding: utf-8 -*-
from .base import *


def create_alkene_1(n_heavy):
    print('\nCreate alkene with single double bond SMILES\n')
    category = 'alkene-1'
    n = n_heavy
    id = 2
    while id <= n:
        sys.stdout.write('\r present %i / %i' % (id, n))
        tasks_all = session.query(Task)
        tasks = tasks_all.filter(Task.category == category).filter(Task.n_heavy == id)
        if tasks.count() == 0:
            task = tasks_all.filter(Task.category == 'alkane').filter(Task.n_heavy == id).first()
            smiles_list = json.loads(task.smiles_list)
            add_double_bond(smiles_list, category=category)
        elif tasks.count() != 1:
            raise Exception('Bad infomation error\n')
        id += 1

def create_alkene_2(n_heavy):
    print('\nCreate alkene with two double bond SMILES\n')
    category = 'alkene-2'
    n = n_heavy
    id = 3
    while id <= n:
        sys.stdout.write('\r present %i / %i' % (id, n))
        tasks_all = session.query(Task)
        tasks = tasks_all.filter(Task.category == category).filter(Task.n_heavy == id)
        if tasks.count() == 0:
            task = tasks_all.filter(Task.category == 'alkene-1').filter(Task.n_heavy == id).first()
            smiles_list = json.loads(task.smiles_list)
            add_double_bond(smiles_list, category=category)
        elif tasks.count() > 2:
            raise Exception('Bad infomation error\n')
        id += 1

def create_alkene_3(n_heavy):
    print('\nCreate alkene with three double bond SMILES\n')
    category = 'alkene-3'
    n = n_heavy
    id = 4
    while id <= n:
        sys.stdout.write('\r present %i / %i' % (id, n))
        tasks_all = session.query(Task)
        tasks = tasks_all.filter(Task.category == category).filter(Task.n_heavy == id)
        if tasks.count() == 0:
            task_stable = tasks_all.filter(Task.category == 'alkene-2').filter(Task.n_heavy == id).filter(
                Task.remark == None).first()
            task_unstable = tasks_all.filter(Task.category == 'alkene-2').filter(Task.n_heavy == id).filter(
                Task.remark == 'unstable').first()
            smiles_list = json.loads(task_stable.smiles_list)
            smiles_list_unstable = json.loads(task_unstable.smiles_list)
            add_double_bond(smiles_list, category=category, smiles_list_unstable=smiles_list_unstable)
        elif tasks.count() > 2:
            raise Exception('Bad infomation error\n')
        id += 1

