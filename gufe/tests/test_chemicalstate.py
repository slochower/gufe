# This code is part of OpenFE and is licensed under the MIT license.
# For details, see https://github.com/OpenFreeEnergy/openfe

import pytest
from openff.toolkit.topology import Molecule
import numpy as np

import gufe


@pytest.fixture
def prot_comp(PDB_181L_path):
    yield gufe.ProteinComponent.from_pdbfile(PDB_181L_path)


@pytest.fixture
def solv_comp():
    yield gufe.SolventComponent(ions=('K', 'Cl'))


@pytest.fixture
def toluene_ligand_comp(benzene_modifications):
    yield gufe.SmallMoleculeComponent.from_rdkit(
        benzene_modifications['toluene'])


@pytest.fixture
def phenol_ligand_comp(benzene_modifications):
    yield gufe.SmallMoleculeComponent.from_rdkit(
        benzene_modifications['phenol'])


@pytest.fixture
def solvated_complex(prot_comp, solv_comp, toluene_ligand_comp):
    return gufe.ChemicalState(
        {'protein': prot_comp,
         'solvent': solv_comp,
         'ligand': toluene_ligand_comp},
    )


@pytest.fixture
def solvated_ligand(solv_comp, toluene_ligand_comp):
    return gufe.ChemicalState(
        {'ligand': toluene_ligand_comp, 'solvent': solv_comp},
    )


def test_construction(prot_comp, solv_comp, toluene_ligand_comp):
    # sanity checks on construction

    state = gufe.ChemicalState(
        {'protein': prot_comp,
         'solvent': solv_comp,
         'ligand': toluene_ligand_comp},
    )

    assert len(state.components) == 3

    assert state.components['protein'] == prot_comp
    assert state.components['solvent'] == solv_comp
    assert state.components['ligand'] == toluene_ligand_comp


def test_hash_and_eq(prot_comp, solv_comp, toluene_ligand_comp):
    c1 = gufe.ChemicalState({'protein': prot_comp,
                             'solvent': solv_comp,
                             'ligand': toluene_ligand_comp})

    c2 = gufe.ChemicalState({'solvent': solv_comp,
                             'ligand': toluene_ligand_comp,
                             'protein': prot_comp})

    assert c1 == c2
    assert hash(c1) == hash(c2)


def test_chemical_state_neq_1(solvated_complex, prot_comp):
    # wrong class
    assert solvated_complex != prot_comp
    assert hash(solvated_complex) != hash(prot_comp)


def test_chemical_state_neq_2(solvated_complex, prot_comp, solv_comp,
                              toluene_ligand_comp):
    # identifiers are different
    complex2 = gufe.ChemicalState(
        {'protein': prot_comp,
         'solvent': solv_comp,
         'ligand': toluene_ligand_comp},
        identifier='Not quite the same'
    )

    assert solvated_complex != complex2
    assert hash(solvated_complex) != hash(complex2)


def test_chemical_state_neq_3(solvated_complex, prot_comp, solv_comp,
                              toluene_ligand_comp):
    # different unit cell size
    complex2 = gufe.ChemicalState(
        {'protein': prot_comp,
         'solvent': solv_comp,
         'ligand': toluene_ligand_comp},
        box_vectors=np.array([10, 0, 0] + [np.nan] * 6),
    )
    assert solvated_complex != complex2
    assert hash(solvated_complex) != hash(complex2)


def test_chemical_state_neq_4(solvated_complex, solvated_ligand):
    # different component keys
    assert solvated_complex != solvated_ligand
    assert hash(solvated_complex) != hash(solvated_ligand)


def test_chemical_state_neq_5(solvated_complex, prot_comp, solv_comp,
                              phenol_ligand_comp):
    # same component keys, but different components
    complex2 = gufe.ChemicalState(
        {'protein': prot_comp,
         'solvent': solv_comp,
         'ligand': phenol_ligand_comp},
    )
    assert solvated_complex != complex2
    assert hash(solvated_complex) != hash(complex2)
