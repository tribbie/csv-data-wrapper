#!/usr/bin/python3 -tt

### FYI - example input file 'data/input/Website2021.csv'
### FYI - header line of this example file:
###       "Code";"Type";"Wijn";"Land";"Regio";" Prijs/fles ";"Beschrijving";"Description";"Website";"Pakketactie"
##
## Run like so: python3 test-diff-csv.py --left data/test-data-in.csv --right data/test-data-in-different.csv --delimiter '|' --fields Name,Active,Color,Description --key Name

import csv
import time
import argparse
import logging
import pprint
from data_table import DataTable

def chapter(title):
    number_of_title_dashes = (132 - len(title) - 2)
    title_dashes = "-" * number_of_title_dashes
    # logging.info("-" * 132)
    logging.info(f"--- {title} {title_dashes}")
    # logging.info("-" * 132)
    return

def configure():
    parser = argparse.ArgumentParser(description='diff two csv files')
    parser.add_argument('--left', required=True, help='left file')
    parser.add_argument('--right', required=True, help='right file')
    parser.add_argument('--delimiter', default=';', help='field delimiter (default = ;)')
    parser.add_argument('--key', default='id', help='key field for diff (default = id)')
    parser.add_argument('--fields', default='', help='field list to diff (comma separated)')
    parser.add_argument('--limit', default=0, help='number of records to process (default = 0 processes them all)')
    args = parser.parse_args()
    configuration = {}
    configuration['limit']          = int(args.limit)
    configuration['left']           = args.left
    configuration['right']          = args.right
    configuration['fielddelimiter'] = args.delimiter
    configuration['keyfield']       = args.key
    if len(args.fields) == 0:
        configuration['fieldlist'] = []
    else:
        configuration['fieldlist'] = args.fields.split(',')
    configuration['stamp']          = time.strftime("%Y%m%d-%H%M%S")
    return configuration


def diff_data(left, right, keyfield, fieldlist):
    if keyfield not in left.fields:
        logging.error(f"ERROR - ERROR - field [{keyfield}] not in fieldlist of 1st file - NOT DIFFING!!")
        return
    if keyfield not in right.fields:
        logging.error(f"ERROR - ERROR - field [{keyfield}] not in fieldlist of 2nd file - NOT DIFFING!!")
        return
    if (len(fieldlist)) == 0:
        fieldlist = left.fields
        logging.info(f"INFO - Using all fields of first file for diff.")
    ## prepare the key-dictionary: key: value, haskey: ['left', 'right'] :
    logging.info(f"=== Preparing key [{keyfield}]")
    keydict = {}
    for leftx, leftkeyrow in enumerate(left.records):
        if leftkeyrow[keyfield] not in keydict:
            keydict[leftkeyrow[keyfield]] = {}
            keydict[leftkeyrow[keyfield]]['right'] = -1
        keydict[leftkeyrow[keyfield]]['left'] = leftx
    for rightx, rightkeyrow in enumerate(right.records):
        if rightkeyrow[keyfield] not in keydict:
            keydict[rightkeyrow[keyfield]] = {}
            keydict[rightkeyrow[keyfield]]['left'] = -1
        keydict[rightkeyrow[keyfield]]['right'] = rightx
    # print(keydict)

    ## start diffing - the better way (with key)
    logging.info(f"=== Diffing fields {fieldlist} via key [{keyfield}]")
    diffdict = {}
    for rowkey in keydict:
        if keydict[rowkey]['left'] == -1:
            # logging.info(f"NO LEFT RECORD for key [{rowkey}] - SKIPPING LEFT ROW")
            print(f"-> [{rowkey}] (right-only)")
            continue
        if keydict[rowkey]['right'] == -1:
            # logging.info(f"NO RIGHT RECORD: for key [{rowkey}] - SKIPPING RIGHT ROW")
            print(f"<- [{rowkey}] (left-only)")
            continue

        # print(f"getting rows [{rowkey}] => {keydict[rowkey]}")
        leftindex = keydict[rowkey]['left']
        leftrow = left.records[leftindex]
        rightindex = keydict[rowkey]['right']
        rightrow = right.records[rightindex]
        # print(f"diffing [{leftrow}] <=> [{rightrow}]")
        rowdiff = []
        for fieldname in fieldlist:
            if (leftrow[fieldname] != rightrow[fieldname]):
                # logging.info(f"DIFFERENCE FOUND: row [{rowkey}]: [{fieldname}]:[{leftrow[fieldname]}]<>[{rightrow[fieldname]}]")
                print(f"<> [{rowkey}].[{fieldname}]: [{leftrow[fieldname]}] <> [{rightrow[fieldname]}]")
                rowdiff.append({fieldname: {'left': leftrow[fieldname], 'right': rightrow[fieldname]}})
        if len(rowdiff) > 0:
            diffdict[rowkey] = rowdiff
    # print(diffdict)
    return diffdict


def main():

    logging.basicConfig(level=logging.INFO)
    logging.info('=== NORMAL START ===' + '=' * 111)

    chapter(f"Process arguments - configure")
    conf = configure()
    pprint.pprint(conf, width=132, indent=10, depth=2)

    chapter(f"Load left csv file [{conf['left']}]")
    left_data = DataTable(displayfield=conf['keyfield'])
    left_data.load_csv(conf['left'], conf['fielddelimiter'], conf['limit'])
    # print(left_data.records)
    # left_data.show_fields()

    chapter(f"Load right csv file [{conf['right']}]")
    right_data = DataTable(displayfield=conf['keyfield'])
    right_data.load_csv(conf['right'], conf['fielddelimiter'], conf['limit'])
    # print(left_data.records)
    # right_data.show_fields(('Name', 'Category', 'Type'))

    chapter(f"Check key is unique in both files")
    if left_data.is_unique_field(conf['keyfield']):
        logging.info(f"[{conf['keyfield']}] is unique in left file - OK")
    else:
        logging.error(f"[{conf['keyfield']}] is NOT unique in left file - exiting")
        exit(3)
    if right_data.is_unique_field(conf['keyfield']):
        logging.info(f"[{conf['keyfield']}] is unique in right file - OK")
    else:
        logging.error(f"[{conf['keyfield']}] is NOT unique in right file - exiting")
        exit(3)

    chapter(f"Diff them csv files")
    diff = diff_data(left_data, right_data, conf['keyfield'], conf['fieldlist'])
    # print(diff)

    logging.info('=== NORMAL END ===' + '=' * 113)
    exit(0)


if __name__ == '__main__':
    main()
