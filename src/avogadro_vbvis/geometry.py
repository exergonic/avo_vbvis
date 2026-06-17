from typing import Any, Dict, List


def parse_molecule(avo_input: Dict[str, Any]) -> Dict[str, Any]:
    molecule = avo_input.get("molecule", {})
    atoms = molecule.get("atoms", {})
    coords = atoms.get("coords", {}).get("3d", [])
    positions = [coords[i : i + 3] for i in range(0, len(coords), 3)]
    elements = atoms.get("elements", [])

    bonds = molecule.get("bonds", {})
    connections = bonds.get("connections", [])

    adjacency: List[List[int]] = [[] for _ in positions]
    for connection in connections:
        if len(connection) >= 2:
            i, j = connection[:2]
            adjacency[i].append(j)
            adjacency[j].append(i)

    return {
        "positions": positions,
        "elements": elements,
        "adjacency": adjacency,
        "raw_bonds": bonds,
    }
