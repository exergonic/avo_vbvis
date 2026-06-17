from typing import Any, Dict, List

STANDARD_VALENCE = {
    1: 1,
    6: 4,
    7: 5,
    8: 6,
    9: 7,
    14: 4,
    15: 5,
    16: 6,
    17: 7,
}


def estimate_lone_pairs(atomic_number: int, bonded_count: int) -> int:
    valence = STANDARD_VALENCE.get(atomic_number, 0)
    lone_pairs = max(valence - bonded_count, 0)
    return lone_pairs


def steric_number(atomic_number: int, bonded_count: int) -> int:
    return bonded_count + estimate_lone_pairs(atomic_number, bonded_count)


def hybridization(sn: int) -> str:
    if sn == 2:
        return "sp"
    if sn == 3:
        return "sp2"
    if sn >= 4:
        return "sp3"
    return "unknown"


def build_orbital_cube(molecule: Dict[str, Any]) -> Dict[str, Any]:
    positions = molecule["positions"]
    elements = molecule["elements"]
    adjacency = molecule["adjacency"]

    origin = [0.0, 0.0, 0.0]
    spacing = [0.25, 0.25, 0.25]
    dimensions = [2, 2, 2]
    scalars: List[float] = [0.0 for _ in range(8)]

    for atom_index, element in enumerate(elements):
        bonded = adjacency[atom_index]
        sn = steric_number(element, len(bonded))
        _ = hybridization(sn)

    return {
        "origin": origin,
        "spacing": spacing,
        "dimensions": dimensions,
        "scalars": scalars,
    }
