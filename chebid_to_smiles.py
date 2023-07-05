import argparse
import pandas as pd
import re

from typing import List
from chebi_api import ChEBI, ChEBIEntity


def add_args(parser: argparse.ArgumentParser) -> argparse.ArgumentParser:
    parser.add_argument("--chebi_id", type=str, required=True, help="ChEBI Ontology ID")
    parser.add_argument(
        "--output",
        type=str,
        required=False,
        default="results.tsv",
        help="Output file. Will be saved as a tab separated file with columns: ['ChEBI ID', 'Type', 'Name', 'SMILES']",
    )
    return parser


def validate_chebi_id(chebi_id: str) -> str:
    if chebi_id.startswith("CHEBI:"):
        return chebi_id
    elif re.match(r"\d+", chebi_id):
        return f"CHEBI:{chebi_id}"
    else:
        raise Exception(f"Invalid ChEBI ID: {chebi_id}")


# ChEBI labels molecules with varying degrees of detail in the form
# of an ontology.
# retrieve_all_ontology_leaves returns all the leaf nodes of the ontology that correspond to a single molecule
def retrieve_all_ontology_leaves(chebi_id: str) -> List[ChEBIEntity]:
    children = ChEBI.get_children(chebi_id)
    return [ChEBI.get_smiles_string(c) for c in children]


def main(chebi_id: str, output: str):
    entries = retrieve_all_ontology_leaves(validate_chebi_id(chebi_id))

    df = pd.DataFrame(entries, columns=["id", "type", "name", "smiles"])
    df.columns = ["ChEBI ID", "Type", "Name", "SMILES"]
    df.to_csv(output, sep="\t", index=False)


if __name__ == "__main__":
    parser = argparse.ArgumentParser()
    parser = add_args(parser)
    args = parser.parse_args()
    main(args.chebi_id, args.output)
