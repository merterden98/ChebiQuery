## [ChEBI Id](https://www.ebi.ac.uk/chebi) to Molecule Query
Given a ChEBI id will attempt to query for all molecules matching that id. Ids appear in an ontology format and therefore many molecules will share common characteristics. This script will help you pull relevant molecules based on an a general description id.

## Installation Requirements

Make sure you have
1. Pandas 
2. Beautiful Soup
3. Requests
4. Lxml

installed. Otherwise you will inevitably encounter an error. 

Here are the associated pip installs

```bash
pip install pandas
pip install bs4
pip install requests
pip install lxml
```

## Usage

```bash
python chebid_to_smiles.py --chebi_id [ID] --output [OUTFILE]
```

output flag is optional and will default to results.tsv. To see output format look at the provided `results.tsv` file.



### Example Usage

```bash
python chebid_to_smiles.py --chebi_id CHEBI:15377
```

will yield the file found in `results.tsv`