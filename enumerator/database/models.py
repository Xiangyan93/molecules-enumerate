#!/usr/bin/env python
# -*- coding: utf-8 -*-
import os
CWD = os.path.dirname(os.path.abspath(__file__))
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import (
    sessionmaker,
    relationship
)
from sqlalchemy import (
    create_engine,
    exists,
    and_,
    ForeignKey
)
from sqlalchemy import (
    Column, Integer, Float, Text, Boolean, String, ForeignKey, UniqueConstraint,
)
import sys, math, json
from mstools.smiles.rdkit import *


Base = declarative_base()
metadata = Base.metadata

db_file = 'sqlite:///%s' % os.path.join(CWD, '..', '..', 'data', 'enumerator.db')

engine = create_engine(db_file, echo=False)
Session = sessionmaker(engine)
session = Session()


class Task(Base):
    __tablename__ = 'task'
    id = Column(Integer, primary_key=True)
    smiles_list = Column(Text, unique=True)
    n_heavy = Column(Integer)
    category = Column(Text)
    molecule_number = Column(Integer)
    remark = Column(Text)
    charge = Column(Integer)
    molecules = relationship('Molecule', back_populates='task')

    def __repr__(self):
        return '<Task: %i %s %i>' % (self.id, self.category, self.n_heavy)

    def generate_Molecule_table(self, smiles_unique_check: bool = False):
        print('generate_Molecule_table task_id = %i' % self.id)
        smiles_list = json.loads(self.smiles_list)
        if self.molecules.count() == len(smiles_list):
            return
        for smiles in smiles_list:
            if smiles_unique_check:
                mols = session.query(Molecule).filter(Molecule.smiles == smiles)
                if mols.count() == 1:
                    print('%i, %s' % (mols.first().id, mols.first().smiles))
                    continue
            mol = Molecule(task=self)
            mol.smiles = smiles
            if self.remark == 'unstable':
                mol.stability = False
            else:
                mol.stability = True
            smiles_stereo_isomer = get_stereo_isomer(smiles)
            if len(smiles_stereo_isomer) == 1:
                mol.has_StereoIsomer = False
            else:
                mol.has_StereoIsomer = True
            session.add(mol)
            mol.generate_Stereoisomer_table()
            session.commit()

    def delete(self):
        print('delete task_id = %i' % self.id)
        self.delete_molecule()
        session.delete(self)
        session.commit()

    def delete_molecule(self):
        print('delete molecules of task_id = %i' % self.id)
        for mol in self.molecules:
            session.delete(mol)
        session.commit()

    def get_mol_number_list(self):
        stereos_all = session.query(StereoIsomer)
        n = 10000
        N = math.ceil(stereos_all.count() / n)
        count = [0, 0]
        for j in range(N):
            stereos = stereos_all.filter(StereoIsomer.id >= j * n).filter(StereoIsomer.id < (j + 1) * n)
            if stereos[0].molecule.task != self and stereos[-1].molecule.task != self and j != 0:
                sys.stdout.write('\r %i / %i' % (j * n, N * n))
                if count != [0, 0]:
                    return count
                continue
            for i, stereo in enumerate(stereos):
                if i % 100 == 0:
                    sys.stdout.write('\r %i / %i' % (i + j * n, N * n))
                if stereo.molecule.task == self:
                    if stereo.training:
                        count[0] += 1
                    count[1] += 1
        return count


class Molecule(Base):
    __tablename__ = 'molecule'
    id = Column(Integer, primary_key=True)
    smiles = Column(Text, unique=True)
    stability = Column(Boolean)
    has_StereoIsomer = Column(Boolean)
    remark = Column(Text)

    task = relationship('Task', foreign_keys='Molecule.task_id')
    task_id = Column(Integer, ForeignKey(Task.id))
    stereoisomers = relationship('StereoIsomer', back_populates='molecule')

    def generate_Stereoisomer_table(self):
        smiles_stereo_isomers = get_stereo_isomer(self.smiles)
        for smiles in smiles_stereo_isomers:
            isomer = StereoIsomer(molecule=self)
            isomer.smiles = smiles
            session.add(isomer)
        session.commit()

    def delete(self):
        for isomer in self.stereoisomers:
            session.delete(isomer)
        session.delete(self)
        session.commit()


class StereoIsomer(Base):
    __tablename__ = 'stereoisomer'
    id = Column(Integer, primary_key=True)
    smiles = Column(Text, unique=True)
    molecule_id = Column(Integer, ForeignKey(Molecule.id))
    molecule = relationship('Molecule', foreign_keys='StereoIsomer.molecule_id')


def create_table():
    if not os.path.exists(os.path.join('..', 'database')):
        os.mkdir(os.path.join('..', 'database'))
    metadata.create_all(engine)
