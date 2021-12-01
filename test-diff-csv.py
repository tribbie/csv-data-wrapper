#!/usr/bin/python3 -tt

### FYI - example input file 'data/input/Website2021.csv'
### FYI - header line of this example file:
###       "Code";"Type";"Wijn";"Land";"Regio";" Prijs/fles ";"Beschrijving";"Description";"Website";"Pakketactie"
##
## Run like so: python3 dimarco-csv-oo-prepare-products.py --inputfile data/input/Website2021.csv --limit 5

import csv
import time
import argparse
import logging
import pprint
from data_table import DataTable

def chapter(title):
    number_of_title_dashes = (132 - len(title)) // 2
    title_dashes = "-" * number_of_title_dashes
    # logging.info("-" * 132)
    logging.info(title_dashes + title + title_dashes)
    # logging.info("-" * 132)
    return

def configure():
    parser = argparse.ArgumentParser(description='diff two csv files')
    parser.add_argument('--files', required=True, help='2 input files (comma separated)')
    parser.add_argument('--delimiter', default=';', help='field delimiter')
    parser.add_argument('--key', default='id', help='key field for diff')
    parser.add_argument('--fields', default='', help='field list to diff (comma separated)')
    parser.add_argument('--limit', default=0, help='number of records to process (0 processes them all)')

    args = parser.parse_args()
    configuration = {}
    configuration['limit']          = int(args.limit)
    configuration['files']          = args.files.split(',')
    configuration['fielddelimiter'] = args.delimiter
    configuration['keyfield']       = args.key
    if len(args.fields) == 0:
        configuration['fieldlist'] = []
    else:
        configuration['fieldlist'] = args.fields.split(',')
    configuration['stamp']          = time.strftime("%Y%m%d-%H%M%S")
    return configuration


def diff_data(f1, f2, keyfield, fieldlist):
    if keyfield not in f1.fields:
        logging.error(f"ERROR - ERROR - field [{keyfield}] not in fieldlist of 1st file - NOT DIFFING!!")
        return
    if keyfield not in f2.fields:
        logging.error(f"ERROR - ERROR - field [{keyfield}] not in fieldlist of 2nd file - NOT DIFFING!!")
        return
    if (len(fieldlist)) == 0:
        fieldlist = f1.fields
        logging.info(f"INFO - Using all fields of first file for diff.")
    logging.info(f"=== Preparing key [{keyfield}]")
    diffdict = []
    keydict = {}
    ## prepare the key-dictionary: key: value, haskey: ['left', 'right'] :
    for f1x, f1keyrow in enumerate(f1.records):
        if f1keyrow[keyfield] not in keydict:
            keydict[f1keyrow[keyfield]] = []
        keydict[f1keyrow[keyfield]].append(f1x)
        # print(f"adding f1[{f1keyrow[keyfield]}]")
    for f2x, f2keyrow in enumerate(f2.records):
        if f2keyrow[keyfield] not in keydict:
            keydict[f2keyrow[keyfield]] = []
        keydict[f2keyrow[keyfield]].append(f2x)
        # print(f"adding f2[{f2keyrow[keyfield]}]")
    print(keydict)

    ## start diffing - the right way (with key)
    logging.info(f"=== Diffing fields {fieldlist} via key {keyfield}")
    for rowkey in keydict:
        print(f"[{rowkey}] => {keydict[rowkey]}")

    ## start diffing - the bad way
    logging.info(f"=== Diffing fields {fieldlist}")
    f1rowiter = iter(f1.records)
    f2rowiter = iter(f2.records)
    for rowcount in range(0, len(f1.records)):
        rowdiff = {}
        f1row = next(f1rowiter)
        f2row = next(f2rowiter)
        for fieldname in fieldlist:
            if (f1row[fieldname] != f2row[fieldname]):
                logging.info(f"DIFFERENCE FOUND: row #{rowcount}: [{f1row[f1.displayfield]}][{fieldname}]:[{f1row[fieldname]}]<>[{f2row[fieldname]}]")
                rowdiff
    return


def main():

    logging.basicConfig(level=logging.INFO)
    logging.info('=== NORMAL START ===' + '=' * 111)

    chapter(f"Process arguments - configure")
    conf = configure()
    pprint.pprint(conf, sort_dicts=False, width=132, indent=10, depth=2)

    chapter(f"Load csv file 1 [{conf['files'][0]}]")
    file1_data = DataTable(displayfield=conf['keyfield'])
    file1_data.load_csv(conf['files'][0], conf['fielddelimiter'], conf['limit'])
    # print(file1_data.records)
    print(f"ROW #3: {file1_data.records[3]}")
    # file1_data.show_fields()

    chapter(f"Load csv file 2 [{conf['files'][1]}]")
    file2_data = DataTable(displayfield=conf['keyfield'] )
    file2_data.load_csv(conf['files'][1], conf['fielddelimiter'], conf['limit'])
    # print(file1_data.records)
    # file2_data.show_fields()
    # file2_data.show_fields(('Code', 'Wijn'))

    chapter(f"Diff them csv files")
    diff = diff_data(file1_data, file2_data, conf['keyfield'], conf['fieldlist'])

    # diffcsv = prestashop_table.generate_csv_array(delimiter='||')
    # print(resultcsv)

    # # Finally we write the resulting products csv file
    # chapter(f"Writing resulting csv - [{conf['outputfile']}]")
    # prestashop_table.write_csv(conf['outputfile'], delimiter=';')
    # logging.info('=== NORMAL END ===' + '=' * 113)

    exit(0)



if __name__ == '__main__':
    main()
