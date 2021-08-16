#!/usr/bin/env python
# -*- coding: utf-8 -*-
from typing import Dict, Iterator, List, Optional, Union, Literal, Tuple
from ..database.models import *


def is_mol_stable(smiles: str) -> bool:
    """

    Parameters
    ----------
    smiles

    Returns
    -------

    """
    rdk_mol = Chem.MolFromSmiles(smiles)
    # double bond check
    atom_idx_list = []
    for bond in rdk_mol.GetBonds():
        if bond.GetBondTypeAsDouble() == 2:
            atom_idx_list.append(bond.GetBeginAtomIdx())
            atom_idx_list.append(bond.GetEndAtomIdx())
    if len(set(atom_idx_list)) != len(atom_idx_list):
        return False
    # two hydroxyl group cannot connect to same carbon

    return True


def add_task(smiles_list: List[str], category: str, remark: str = None):
    if session.query(Task).filter(Task.smiles_list == json.dumps(smiles_list)).first() is not None:
        return
    new_task = Task()
    new_task.smiles_list = json.dumps(smiles_list)
    new_task.n_heavy = get_heavy_atoms_number(smiles_list[0])
    new_task.category = category
    new_task.molecule_number = len(smiles_list)
    new_task.charge = get_charge(smiles_list[0])
    if remark is not None:
        new_task.remark = remark
    session.add(new_task)
    session.commit()


def add_atom(smiles_list: List[str], bond_order: int, category: str, atom_num, growing_atom=6, remark=None, stable_check=False):
    """Add a new atom and bond to previous molecule from previous smiles

    Parameters
    ----------
    smiles_list: a list of smiles.
    bond_order: 1,2,3 means add a single, double, triple bond, respectively.
    category: string.
    atom_num:
    growing_atom: atomic number
    remark
    stable_check

    Returns
    -------

    """
    new_smiles_list = []
    for smiles in smiles_list:
        rdk_mol = Chem.MolFromSmiles(smiles)
        for atom in rdk_mol.GetAtoms():
            if atom.GetImplicitValence() < bond_order:
                continue
            if atom.GetAtomicNum() != growing_atom:
                continue
            for _atom in atom.GetNeighbors():
                if _atom.GetAtomicNum() != 6:
                    break
            else:
                new_mol = Chem.RWMol(rdk_mol)
                new_id = new_mol.AddAtom(Chem.Atom(atom_num))
                if bond_order == 1:
                    new_mol.AddBond(atom.GetIdx(), new_id, Chem.BondType.SINGLE)
                elif bond_order == 2:
                    new_mol.AddBond(atom.GetIdx(), new_id, Chem.BondType.DOUBLE)
                elif bond_order == 3:
                    new_mol.AddBond(atom.GetIdx(), new_id, Chem.BondType.TRIPLE)
                else:
                    continue
                new_smiles = get_rdkit_smiles(Chem.MolToSmiles(new_mol))
                if stable_check and not is_mol_stable(new_smiles):
                    continue
                if new_smiles not in new_smiles_list:
                    new_smiles_list.append(new_smiles)

    if new_smiles_list:
        add_task(new_smiles_list, category, remark=remark)


def replace_atom(smiles_list, old_atom_number, new_atom_number, connect_number, category, remark=None,
                 stable_check=False):
    new_smiles_list = []
    for smiles in smiles_list:
        rdk_mol = Chem.MolFromSmiles(smiles)
        for atom in rdk_mol.GetAtoms():
            if atom.GetAtomicNum() != old_atom_number:
                continue
            if len(atom.GetNeighbors()) not in connect_number:
                continue
            accept = True
            for _atom in atom.GetNeighbors():
                if _atom.GetAtomicNum() != 6:
                    accept = False
                    break
                for __atom in _atom.GetNeighbors():
                    if __atom.GetAtomicNum() != 6:
                        accept = False
                        break
                if not accept:
                    break
            if accept:
                new_mol = Chem.RWMol(rdk_mol)
                idx = atom.GetIdx()
                new_mol.GetAtoms()[idx].SetAtomicNum(new_atom_number)
                new_smiles = get_rdkit_smiles(Chem.MolToSmiles(new_mol))
                if stable_check and not is_mol_stable(new_smiles):
                    continue
                if new_smiles not in new_smiles_list:
                    new_smiles_list.append(new_smiles)

    if new_smiles_list:
        add_task(new_smiles_list, category, remark=remark)


# substitute a single bond to double bond
def sub_double_bond(smiles_list, category=None, smiles_list_unstable=None):
    if category is None:
        raise Exception('you must asign category for function add_double_bond()')

    new_smiles_list = []
    new_smiles_list_unstable = []
    for smiles in smiles_list:
        rdk_mol = Chem.MolFromSmiles(smiles)
        for bond in rdk_mol.GetBonds():
            if bond.GetBondTypeAsDouble() == 1 and bond.GetBeginAtom().GetImplicitValence() != 0 and \
                    bond.GetEndAtom().GetImplicitValence() != 0:
                bond.SetBondType(Chem.BondType.DOUBLE)
                new_smiles = get_rdkit_smiles(Chem.MolToSmiles(rdk_mol))
                if is_mol_stable(new_smiles) and new_smiles not in new_smiles_list:
                    new_smiles_list.append(new_smiles)
                elif not is_mol_stable(new_smiles) and new_smiles not in new_smiles_list_unstable:
                    new_smiles_list_unstable.append(new_smiles)
                bond.SetBondType(Chem.BondType.SINGLE)
    if smiles_list_unstable != None:
        for smiles in smiles_list_unstable:
            rdk_mol = Chem.MolFromSmiles(smiles)
            for bond in rdk_mol.GetBonds():
                if bond.GetBondTypeAsDouble() == 1 and bond.GetBeginAtom().GetImplicitValence() != 0 and bond.GetEndAtom().GetImplicitValence() != 0:
                    bond.SetBondType(Chem.BondType.DOUBLE)
                    new_smiles = get_rdkit_smiles(Chem.MolToSmiles(rdk_mol))
                    if new_smiles not in new_smiles_list_unstable:
                        new_smiles_list_unstable.append(new_smiles)
                    bond.SetBondType(Chem.BondType.SINGLE)
    if new_smiles_list != []:
        new_info = Task()
        new_info.smiles_list = json.dumps(new_smiles_list)
        new_info.n_heavy = get_heavy_atoms_number(new_smiles_list[0])
        new_info.category = category
        new_info.molecule_number = len(new_smiles_list)
        new_info.charge = get_charge(new_smiles_list[0])
        session.add(new_info)
    if new_smiles_list_unstable != []:
        new_info = Task()
        new_info.smiles_list = json.dumps(new_smiles_list_unstable)
        new_info.n_heavy = get_heavy_atoms_number(new_smiles_list_unstable[0])
        new_info.category = category
        new_info.molecule_number = len(new_smiles_list_unstable)
        new_info.charge = get_charge(new_smiles_list_unstable[0])
        new_info.remark = 'unstable'
        session.add(new_info)
    session.commit()


def add_triple_bond(smiles_list, category=None, remark=None):
    if category == None:
        raise Exception('you must asign category for function add_triple_bond()')

    new_smiles_list = []
    for smiles in smiles_list:
        rdk_mol = Chem.MolFromSmiles(smiles)
        for bond in rdk_mol.GetBonds():
            if bond.GetBondTypeAsDouble() == 1 and bond.GetBeginAtom().GetImplicitValence() > 1 and bond.GetEndAtom().GetImplicitValence() > 1:
                bond.SetBondType(Chem.BondType.TRIPLE)
                new_smiles = get_rdkit_smiles(Chem.MolToSmiles(rdk_mol))
                if new_smiles not in new_smiles_list:
                    new_smiles_list.append(new_smiles)
                bond.SetBondType(Chem.BondType.SINGLE)
    if new_smiles_list != []:
        new_info = Task()
        new_info.smiles_list = json.dumps(new_smiles_list)
        new_info.n_heavy = get_heavy_atoms_number(new_smiles_list[0])
        new_info.category = category
        new_info.molecule_number = len(new_smiles_list)
        new_info.charge = get_charge(new_smiles_list[0])
        if remark != None:
            new_info.remark = remark
        session.add(new_info)
        session.commit()


# n_heavy is for old_category
def generate_task(n_heavy, new_category, old_category, generate_type,
                  bond_order=None, atom_number=None, # generate_type = 'add'
                  old_atom_number=None, new_atom_number=None, connect_number=[] # generate_type = replace
                  ):
    tasks_all = session.query(Task)
    tasks = tasks_all.filter(Task.category == old_category).filter(Task.n_heavy == n_heavy)
    if tasks.count() == 1:
        task = tasks.first()
        smiles_list = json.loads(task.smiles_list)
        if generate_type == 'add':
            if bond_order is None or atom_number is None:
                return
            if tasks_all.filter(Task.category == new_category).filter(Task.n_heavy == n_heavy + 1).count() != 0:
                return
            add_atom(smiles_list, bond_order, category=new_category, atom_num=atom_number)
        elif generate_type == 'replace':
            if old_atom_number is None or new_atom_number is None or not connect_number:
                return
            if tasks_all.filter(Task.category == new_category).filter(Task.n_heavy == n_heavy).count() != 0:
                return
            replace_atom(smiles_list, category=new_category, old_atom_number=old_atom_number,
                         new_atom_number=new_atom_number, connect_number=connect_number)


def growing_from_smiles(n_heavy_cutoff, smiles, category):
    print('\nCreate SMILES by growing from %s\n' % smiles)
    add_task([smiles], category, )
    n = get_heavy_atoms_number(smiles)
    while n < n_heavy_cutoff:
        sys.stdout.write('\r present %i / %i' % (n + 1, n_heavy_cutoff))
        generate_task(n_heavy=n, new_category=category, old_category=category, generate_type='add', bond_order=1, atom_number=6)
        n += 1
