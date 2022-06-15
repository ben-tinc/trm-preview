'''
hte2skos.py

Clean up the HTE data and convert it to SKOS.
'''

from pathlib import Path
import logging

import pandas as pd


HTE_PATH = Path(__file__).parent / 'Media_405073_smxx.xlsx'
RES_PATH = Path(__file__).parent / 'prepared_hte_data.xlsx'
FIXTURES = {
    50: '238078',       # Asia, 01.01.06.02
    777: '238074',      # Textiles and clothing, 01.08
    1175: '238077',     # Condition of matter
    1986: '238071',     # Goodness and badness
    2022: '127464',     # Emotion
    2023: '127644',     # Emotions, mood
}
    

def read(path=HTE_PATH):
    '''Read spreadsheet file and parse it into dataframe.'''
    df = pd.read_excel(path, dtype=str)
    return df


def prepare(df):
    '''Clean data up and create derived data columns.'''
    # Add missing (but known) catids.
    for rownum, catid in FIXTURES.items():
        df.iloc[rownum]['catid'] = catid
    
    # Regenerate the concat column.
    df['concat'] = df.apply(lambda row: build_sig(row, ['t1','t2','t3','t4','t5','t6','t7'], '.', 'pos'), axis=1)

    # Remove unneeded columns.
    df = df.drop(['t1', 't2', 't3', 't4', 't5', 't6', 't7', 'subcat', 'pos', 'HT heading'], axis=1)

    # Create HTE URL column.
    df['hte_url'] = df.apply(lambda row: build_hte_url(row.loc["catid"]), axis=1)

    # Create signature column by concatenating the Thematic Categories path columns.
    df['signature'] = df.apply(build_sig, axis=1)

    # Create column with parent category (if any)
    df['broader'] = df.apply(lambda row: determine_parent(df, row), axis=1)

    # Rename label column.
    df.rename(columns={'SAMUELS heading': 'prefLabel'}, inplace=True)

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


def build_hte_url(catid):
    return f'https://ht.ac.uk/category/?id={catid}'


def determine_parent(df, row):
    '''Check if there is a parent category, and if so, what its URL is.'''
    path = row.loc[['AS1', 'S2', 'S3', 'S4', 'S5']]
    path = path[path.notnull()]
    
    if len(path) > 1:
        parent = path[:-1]
        sig = ''.join(parent)
        try:
            catid = df[df['signature']==sig].iloc[0]['catid']
            return build_hte_url(catid)
        except IndexError:
            # This can actually happen, if the parent concept simply does not exist in
            # the dataset. See https://git.noc.ruhr-uni-bochum.de/sfb1475-inf/TRM/-/issues/5
            # for further info.
            msg = f"Concept path '{''.join(path)}' suggests that '{sig}' should exist, but it doesn't."
            logging.error(msg)
            return None
    return None


def write(df, filename=RES_PATH):
    df.to_excel(filename)


def main():
    df = read(HTE_PATH)
    df = prepare(df)
    write(df, RES_PATH)


if __name__ == '__main__':
    main()