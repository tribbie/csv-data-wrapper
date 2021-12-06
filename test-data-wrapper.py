#!/usr/bin/python3 -tt

## Run like so: python3 test-data-wrapper.py --inputfile data/test-data-in.csv --limit 5
## test-data header: "Active"|"Name"|"Category"|"Type"|"Country"|"Color"|"Description"

import csv
import time
import argparse
import logging
from data_table import DataTable

def chapter(title, filler='-'):
    number_of_title_dashes = (132 - len(title)) // 2
    title_dashes = filler * number_of_title_dashes
    logging.info(title_dashes + title + title_dashes)
    return

def configure():
    parser = argparse.ArgumentParser(description='Morph Excel-csv into Prestashop-products-csv.')
    parser.add_argument('--inputfile', required=True, help='input file')
    parser.add_argument('--limit', default=0, help='number of records to process (0 processes them all)')
    parser.add_argument('--delimiter', default=';', help='field delimiter')
    args = parser.parse_args()
    configuration = {}
    configuration['inputfile']      = args.inputfile
    configuration['delimiter']      = args.delimiter
    configuration['limit']          = int(args.limit)
    configuration['stamp']          = time.strftime("%Y%m%d-%H%M%S")
    configuration['outputfile']     = 'data/output/test-output-' + configuration['stamp'] + '.csv'
    # configuration['imglocation']    = 'https://www.dimarco.be/webshop/img/dimarcowines/'
    configuration['featurelist']    = ('Type', 'Country')
    configuration['categorieslist'] = ['fix-maincat', 'Category']
    configuration['finalfieldmap'] = {
            'gen-id': "UNIQUE-ID",
            'Active': "ACTIVE",
            'Name': "NAME",
            'Type': "TYPE",
            'Country': "COUNTRY",
            'Color': "COLOR",
            'Description': "DESCRIPTION",
            'fix-maincat': "CATEGORY",
            'Category': "SUBCATEGORY",
            'gen-short-description': "SHORT-DESCRIPTION",
            'gen-subtitle': "SUBTITLE",
            'combined-categories': "CATEGORIES",
            'combined-features': "FEATURES"
        }
    return configuration

def main():

    logging.basicConfig(level=logging.INFO)
    chapter(f" NORMAL START ", filler='=')

    chapter(f"Process arguments - configure")
    conf = configure()

    chapter(f"Load csv [{conf['inputfile']}]")
    input_data = DataTable(displayfield='Name')
    input_data.load_csv(conf['inputfile'], conf['delimiter'], conf['limit'])
    # input_data.show_fields(('Active', 'Name', 'Description'))
    input_data.show_fields()

    chapter(f"Remove unwanted records")
    input_data.remove_records({'Active': 'N'})

    chapter(f"Replace some shizzle - newlines, semicolons, etc")
    # input_data.replace_in_field(field='Description', frompart='\n', topart='<br/>')
    input_data.replace_in_field(field='Description', frompart=';', topart='.')
    # input_data.show_fields(('Active', 'Name', 'Description'))

    chapter(f"Checking uniqueness of field Name")
    isUnique = input_data.is_unique_field(fieldname='Name')

    chapter(f"Add some extra fields")
    input_data.add_counter_field('gen-id', initialvalue=10001)
    input_data.copy_field(sourcefield='Description', newfield='gen-short-description')
    input_data.add_fixed_field('fix-text-1', 'from')
    input_data.add_combined_field(newfield='gen-subtitle', fieldstocombine=['Type', 'fix-text-1', 'Country'], delimiter=' ')

    chapter(f"Generate complex combined feature field from the feature fields")
    input_data.add_combined_features_field('combined-features', conf['featurelist'])
    # input_data.show_fields(('Name', 'Product', 'combined-features'))

    chapter(f"Combine the category fields into one category (list)field")
    input_data.add_fixed_field('fix-maincat', 'Inhabitants')
    input_data.add_combined_categories_field('combined-categories', conf['categorieslist'])
    # input_data.show_fields(('Name', 'Product', 'combined-categories'))

    chapter(f"Re-map fields for Prestashop")
    output_data = input_data.re_map_table(conf['finalfieldmap'], displayfield='NAME')

    chapter(f"Some tests - output to screen")
    output_data.show_fields(('UNIQUE-ID', 'NAME', 'TYPE', 'CATEGORIES', 'FEATURES'))
    # output_data.show_record('Bollie')
    isUnique = output_data.is_unique_field(fieldname='NAME')

    # Finally we write the resulting products csv file
    chapter(f"Writing resulting csv - [{conf['outputfile']}]")
    output_data.write_csv(conf['outputfile'], delimiter=';')
    chapter(f" NORMAL END ", filler='=')

    exit(0)


if __name__ == '__main__':
    main()
