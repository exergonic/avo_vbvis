import argparse
import json
import sys
from pathlib import Path
from datetime import datetime

from .geometry import parse_molecule
from .orbitals import build_orbital_cube
from .io import write_json_output

sys.stdout.reconfigure(encoding="utf-8")
FEATURE_IDENTIFIER = "display-valence-orbitals"
LOG_FILE = Path(r"C:\Users\mccan\AppData\Local\OpenChemistry\Avogadro\plugins\avo_vbvis\log.txt")

def log_invocation(feature, args, input_keys):
    LOG_FILE.parent.mkdir(parents=True, exist_ok=True)
    with LOG_FILE.open("a", encoding="utf-8") as f:
        f.write(
            f"{datetime.now().isoformat()} "
            f"feature={feature} "
            f"args={args} "
            f"input_keys={input_keys}\n"
        )

def run(avo_input, feature, **args):
    if feature == FEATURE_IDENTIFIER:
        molecule = parse_molecule(avo_input)
        cube = build_orbital_cube(molecule)
        return {"molecule": {"cube": cube}}
    return {"error": f"Unknown feature: {feature}"}


def main():
    parser = argparse.ArgumentParser()
    common = argparse.ArgumentParser(add_help=False)
    common.add_argument("--lang", nargs="?", default="en")
    common.add_argument("--debug", action="store_true")
    common.add_argument("--print-options", action="store_true")

    subparsers = parser.add_subparsers(dest="feature")
    subparsers.add_parser(FEATURE_IDENTIFIER, parents=[common])

    args = parser.parse_args()
    avo_input = json.loads(sys.stdin.read() or "{}")

    log_invocation(args.feature, vars(args), list(avo_input.keys()))

    if args.print_options:
        write_json_output(
            {
                "options": [
                    {
                        "name": "grid-resolution",
                        "type": "integer",
                        "label": "Grid resolution",
                        "default": 24,
                    },
                    {
                        "name": "isovalue",
                        "type": "number",
                        "label": "Orbital isovalue",
                        "default": 0.05,
                    },
                ]
            }
        )
        return

    output = run(avo_input, args.feature, user_options=False)
    write_json_output(output)
