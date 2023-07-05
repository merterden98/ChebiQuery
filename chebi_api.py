import requests
from typing import List, Optional, Union
from dataclasses import dataclass
from bs4 import BeautifulSoup


@dataclass
class ChEBIEntity:
    name: str
    id: str
    type: Optional[
        str
    ]  # TODO: Enum for just "Has role" and "Is a", additionally in get_smiles_string this might be None
    smiles: Optional[str] = None


class ChEBI:
    ROOT = "https://www.ebi.ac.uk/webservices/chebi/2.0/test/"
    GET_ONTOLOGY_CHILDREN_ENDPOINT = "getOntologyChildren"
    GET_SMILES_ENDPOINT = "getCompleteEntity"

    @staticmethod
    def construct_url(endpoint: str, chebi_id: str) -> str:
        return f"{ChEBI.ROOT}{endpoint}?chebiId={chebi_id}"

    @classmethod
    # Note According CheBI this does grab all children, but I have not validated their claim
    def get_children(cls, chebi_id: str) -> List[ChEBIEntity]:
        url = cls.construct_url(cls.GET_ONTOLOGY_CHILDREN_ENDPOINT, chebi_id)
        response = requests.get(url)
        if response.status_code != 200:
            raise Exception(f"Error {response.status_code} when querying {url}")

        # Parse XML response with bs4
        bs = BeautifulSoup(response.text, "xml")
        # Get all tags <OntologyChildren>
        children = bs.find_all("ListElement")

        if children is [None] or len(children) == 0:
            return [cls.get_smiles_string(chebi_id)]
        # For each tag construct a CheBIEntity object
        children = [
            ChEBIEntity(
                c.find("chebiName").text,
                c.find("chebiId").text,
                c.find("type").text,
            )
            for c in children
        ]
        # Validate that all children are of type "has role" or "is a"
        children = [c for c in children if c.type in ["has role", "is a"]]
        return children

    @classmethod
    def get_smiles_string(
        cls, chebi_id: Union[str, ChEBIEntity]
    ) -> Optional[ChEBIEntity]:
        search = chebi_id
        if isinstance(chebi_id, ChEBIEntity):
            search = chebi_id.id
        url = cls.construct_url(cls.GET_SMILES_ENDPOINT, search)
        response = requests.get(url)
        if response.status_code != 200:
            raise Exception(f"Error {response.status_code} when querying {url}")

        # Parse XML response with bs4
        bs = BeautifulSoup(response.text, "xml")
        # Get tag <smiles>
        smiles = bs.find("smiles")
        if smiles is None:
            return None
        smiles = smiles.text
        if isinstance(chebi_id, ChEBIEntity):
            chebi_id.smiles = smiles
            return chebi_id
        return ChEBIEntity(bs.find("chebiAsciiName").txt, chebi_id, None, smiles)


if __name__ == "__main__":
    chebi_id = "CHEBI:33811"
    children = ChEBI.get_children(chebi_id)
    print(ChEBI.get_smiles_string(children[0]))
