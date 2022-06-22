# hte2skos

## Prerequisites

This script uses `pandas`, `rdflib`, `skosify` and `openpyxl`. You can install it with eg.

```sh
pip install pandas rdflib skosify openpyxl
# Or use:
pip install -r requirements.txt
```

## Basic usage

To run the script with default options, just use 

```sh
python hte2skos.py
```

from the directory, where your HTE data file is located. To view the usage notes and the available
command line options, use

```sh
python hte2skos.py --help
```

## Configuration

Apart from the command line options, you can customize the URI used to reference the `skos:ConceptScheme` and
individual `skos:Concept`s, by changing some constants at the very top of the script. These are:

* `URI_PREFIX`: The base URI to use for everything. Defaults to (the currently non-existing) `'https://w3id.org/TRM/'`.
* `CONCEPT_PREFIX`: The URI to use for `skos:Concept`s. Defauls to `URI_PREFIX`+`'concepts/'`.
* `CONCEPT_SCHEME`: The URI of the `skos:ConceptScheme`. Defaults to `URI_PREFIX`+`'conceptSchemes/TRMBase'`.