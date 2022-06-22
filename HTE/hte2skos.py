'''
hte2skos.py

Clean up the HTE data and convert it to SKOS.

This script takes the HTE data as .xlsx file.
It tries to clean it up by adding some needed unique identifier
and deriving additional data columns. It then converts the
information into SKOS statements and writes these into an
intermediate file. This file is then checked and possibly
enhanced by the skosify tool.
'''

import argparse
import logging
from pathlib import Path

import numpy as np
import pandas as pd
from rdflib import Graph, Literal, Namespace, RDF, URIRef
from rdflib.namespace import SKOS, XSD
import skosify


URI_PREFIX = 'https://w3id.org/TRM/'
CONCEPT_PREFIX = f'{URI_PREFIX}concepts/'
CONCEPT_SCHEME = f'{URI_PREFIX}conceptSchemes/TRMBase'

PROJECT_PATH = Path(__file__).parent
HTE_PATH = PROJECT_PATH / 'Media_405073_smxx.xlsx'
CLEAN_PATH = PROJECT_PATH / 'prepared_hte_data.xlsx'
INTER_PATH = PROJECT_PATH / 'intermediate_hte_data.ttl'
RESULT_PATH = PROJECT_PATH / 'hte_data.ttl'

FIXTURES = {
    50: '238078',       # Asia, 01.01.06.02
    777: '238074',      # Textiles and clothing, 01.08
    1175: '238077',     # Condition of matter
    1986: '238071',     # Goodness and badness
    #2022: '999999',     # Emotion genuinely has no linked concept. Just use an arbitrary number for now
    #2023: '127644',     # Emotions, mood
}
    

def read(path=HTE_PATH):
    '''Read spreadsheet file and parse it into dataframe.'''
    df = pd.read_excel(path, dtype=str)
    return df


def prepare(df):
    '''Clean data up and create derived data columns.'''
    # Add missing (but known) catids.
    new_id_gen = _generate_new_trmid(df, starting=500000)
    def new_id(row):
        if row.name in FIXTURES:
            return FIXTURES[row.name]
        elif not row['catid'] or row['catid'] is np.NaN:
            return next(new_id_gen)
        return row['catid']

    df['trmid'] = df.apply(new_id, axis=1)

    # Regenerate the concat column by concatenating the HTE path columns.
    df['concat'] = df.apply(lambda row: build_sig(row, ['t1','t2','t3','t4','t5','t6','t7'], '.', 'pos'), axis=1)

    # Remove unneeded columns.
    df = df.drop(['t1', 't2', 't3', 't4', 't5', 't6', 't7', 'subcat', 'pos', 'HT heading'], axis=1)

    # Create HTE URL column.
    df['hte_url'] = df.apply(build_hte_url, axis=1)

    # Create signature column by concatenating the Thematic Categories path columns.
    df['signature'] = df.apply(build_sig, axis=1)

    # Create column with parent category (if any).
    # This is super slow, but unfortunately we have to check if all these
    # parent items actually exist.
    df['broader'] = df.apply(lambda row: determine_parent(df, row), axis=1)

    # Rename label column.
    df.rename(columns={'SAMUELS heading': 'prefLabel'}, inplace=True)

    # Remove excessive whitespace.
    df['prefLabel'] = df['prefLabel'].str.strip()

    # Remove now obsolete columns.
    df = df.drop(['AS1','S2','S3','S4','S5'], axis=1)

    return df


def build_sig(row, fields=['AS1', 'S2', 'S3', 'S4', 'S5'], sep='', end=None):
    '''Concatenate path elements from the given fields.'''
    r = row.loc[fields]
    sig = sep.join(r[r.notnull()])
    if end is not None:
        sig += f"{row.loc[end]}"
    return sig


def build_concept_uri(catid):
    '''Create a URI for a concept.'''
    return f'{CONCEPT_PREFIX}{catid}/'


def build_hte_url(row):
    catid = row.loc['catid']
    if catid and catid is not np.NaN:
        return f'https://ht.ac.uk/category/?id={row.loc["catid"]}'
    return None


def convert(df):
    '''Take dataframe and express its information as SKOS.
    
    It expects the following columns to be present:
    * hte_url (the UID of the concept)
    * signature (the path of the concept)
    * broader (UID of the broader concept)
    * prefLabel (preferred label of the concept)
    * concat (the corresponding path in the full HTE hierarchy)
    '''
    graph = Graph()
    ns = Namespace(URI_PREFIX)

    # Create the skos:ConceptScheme
    scheme = URIRef(CONCEPT_SCHEME)
    graph.add((scheme, RDF.type, SKOS.ConceptScheme))
    graph.add((scheme, SKOS.prefLabel, Literal('Thesaurus of Religious Metaphors', lang='en')))
    graph.add((scheme, SKOS.altLabel, Literal('TRM', lang='en')))

    # Yes, I know that `df.iterrows()` is slow but these are only 4000 rows, give me a break..
    for _idx, row in df.iterrows():
        concept = URIRef(build_concept_uri(row['trmid']))
        graph.add((concept, RDF.type, SKOS.Concept))
        graph.add((concept, SKOS.prefLabel, Literal(row['prefLabel'], lang='en')))
        graph.add((concept, SKOS.notation, Literal(row['signature'], datatype=ns.TCPath)))
        
        if row['concat'] and row['concat'] != 'nan':
            graph.add((concept, SKOS.notation, Literal(row['concat'], datatype=ns.HTEPath)))

        if row['broader'] and row['broader'] is not np.NaN:
            graph.add((concept, SKOS.broader, URIRef(row['broader'])))
    
    return graph


def determine_parent(df, row):
    '''Check if there is a parent category, and if so, what its URL would be.
    
    This is pretty slow, but unfortunately we cannot simply assume that
    concepts which are deeper in the hierarchy have a parent concept which
    actually exists inside the TC.
    See https://git.noc.ruhr-uni-bochum.de/sfb1475-inf/TRM/-/issues/5 for
    further info.
    '''
    path = row.loc[['AS1', 'S2', 'S3', 'S4', 'S5']]
    path = path[path.notnull()]

    found = None
    while len(path) > 1:
        path, leaf = path[:-1], path[-1]
        sig = ''.join(path)
        trmid = df.loc[df['signature'] == sig]['trmid']

        if trmid.empty:
            msg = f"Concept path '{sig}{leaf}' suggests that '{sig}' should exist, but it doesn't."
            logging.warning(msg)
        else:
            found = build_concept_uri(trmid.iloc[0])
            break
    return found


def _generate_new_trmid(df, starting=None):
    '''In cases where no catid is present, just use the next highest integer.'''
    if starting is not None:
        maxid = starting
    else:
        maxid = df[df['catid'].notnull()]['catid'].astype(int).max()
    while True:
        maxid += 1
        yield str(maxid)


def write_prepared(df, filename=CLEAN_PATH):
    '''Write prepared HTE data to another spreadsheet file.'''
    df.to_excel(filename)


def write_intermediate(graph, filename=INTER_PATH):
    '''Write intermediate SKOS graph to turtle file.'''
    graph.serialize(filename, encoding='utf8')


def main(config):
    df = read(config.infile)
    df = prepare(df)
    write_prepared(df, config.prepared)
    graph = convert(df)
    write_intermediate(graph, config.intermediate)


if __name__ == '__main__':
    p = argparse.ArgumentParser(description='Convert HTE data from .xlsx file to SKOS and enhance it with skosify.')
    p.add_argument('infile', type=Path, default=HTE_PATH, nargs='?',
        help='path to the .xlsx file which contains the HTE data'
    )
    p.add_argument('-p', '--prepared', type=Path, default=CLEAN_PATH,
        help='path where the cleaned up .xlsx file should be written'
    )
    p.add_argument('-i', '--intermediate', type=Path, default=INTER_PATH,
        help='path where the intermediate SKOS ttl file should be written'
    )
    p.add_argument('-o', '--output', type=Path, default=RESULT_PATH,
        help='path where the final "skosified" SKOS ttl file should be written'
    )

    args = p.parse_args()
    main(args)