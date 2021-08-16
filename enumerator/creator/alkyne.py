#!/usr/bin/env python
# -*- coding: utf-8 -*-
from .base import *


def create_alkyne_1(n_heavy):
    print('\nCreate alkyne with single triple bond SMILES\n')
    category = 'alkyne-1'
    n = n_heavy
    id = 2
    while id <= n:
        sys.stdout.write('\r present %i / %i' % (id, n))
        tasks_all = session.query(Task)
        tasks = tasks_all.filter(Task.category == category).filter(Task.n_heavy == id)
        if tasks.count() == 0:
            task = tasks_all.filter(Task.category == 'alkane').filter(Task.n_heavy == id).first()
            smiles_list = json.loads(task.smiles_list)
            add_triple_bond(smiles_list, category=category)
        elif tasks.count() != 1:
            raise Exception('Bad infomation error\n')
        id += 1

def create_alkyne_2(n_heavy):
    print('\nCreate alkyne with two triple bond SMILES\n')
    category = 'alkyne-2'
    n = n_heavy
    id = 4
    while id <= n:
        sys.stdout.write('\r present %i / %i' % (id, n))
        tasks_all = session.query(Task)
        tasks = tasks_all.filter(Task.category == category).filter(Task.n_heavy == id)
        if tasks.count() == 0:
            task = tasks_all.filter(Task.category == 'alkyne-1').filter(Task.n_heavy == id).first()
            smiles_list = json.loads(task.smiles_list)
            add_triple_bond(smiles_list, category=category)
        elif tasks.count() != 1:
            raise Exception('Bad infomation error\n')
        id += 1

def create_alkyne_3(n_heavy):
    print('\nCreate alkyne with three triple bond SMILES\n')
    category = 'alkyne-3'
    n = n_heavy
    id = 6
    while id <= n:
        sys.stdout.write('\r present %i / %i' % (id, n))
        tasks_all = session.query(Task)
        tasks = tasks_all.filter(Task.category == category).filter(Task.n_heavy == id)
        if tasks.count() == 0:
            task = tasks_all.filter(Task.category == 'alkyne-2').filter(Task.n_heavy == id).first()
            smiles_list = json.loads(task.smiles_list)
            add_triple_bond(smiles_list, category=category)
        elif tasks.count() != 1:
            raise Exception('Bad infomation error\n')
        id += 1


def create_alkene_1_alkyne_1(n_heavy):
    print('\nCreate hydrocarbon with 1 double bond and 1 triple bond SMILES\n')
    category = 'alkene-1-alkyne-1'
    n = n_heavy
    id = 4
    while id <= n:
        sys.stdout.write('\r present %i / %i' % (id, n))
        tasks_all = session.query(Task)
        tasks = tasks_all.filter(Task.category == category).filter(Task.n_heavy == id)
        if tasks.count() == 0:
            task = tasks_all.filter(Task.category == 'alkene-1').filter(Task.n_heavy == id).first()
            smiles_list = json.loads(task.smiles_list)
            add_triple_bond(smiles_list, category=category)
        elif tasks.count() != 1:
            raise Exception('Bad infomation error\n')
        id += 1

def create_alkene_1_alkyne_2(n_heavy):
    print('\nCreate hydrocarbon with 1 double bond and 2 triple bond SMILES\n')
    category = 'alkene-1-alkyne-2'
    n = n_heavy
    id = 6
    while id <= n:
        sys.stdout.write('\r present %i / %i' % (id, n))
        tasks_all = session.query(Task)
        tasks = tasks_all.filter(Task.category == category).filter(Task.n_heavy == id)
        if tasks.count() == 0:
            task = tasks_all.filter(Task.category == 'alkene-1-alkyne-1').filter(Task.n_heavy == id).first()
            smiles_list = json.loads(task.smiles_list)
            add_triple_bond(smiles_list, category=category)
        elif tasks.count() != 1:
            raise Exception('Bad infomation error\n')
        id += 1

def create_alkene_2_alkyne_1(n_heavy):
    print('\nCreate hydrocarbon with 2 double bond and 1 triple bond SMILES\n')
    category = 'alkene-2-alkyne-1'
    n = n_heavy
    id = 5
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
            add_triple_bond(smiles_list, category=category)
            add_triple_bond(smiles_list_unstable, category=category, remark='unstable')
        elif tasks.count() > 2:
            raise Exception('Bad infomation error\n')
        id += 1