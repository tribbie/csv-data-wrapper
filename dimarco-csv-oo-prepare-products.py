#!/usr/bin/python3 -tt

### FYI - example input file 'test-info/Website2021.csv'
### FYI - header line of this example file: "Code";"Type";"Wijn";"Land";"Regio";" Prijs/fles ";"Beschrijving";"Description";"Website";"Pakketactie"
##
## Run like so: python3 dimarco-csv-oo-prepare-products.py --inputfile data/input/Website2021.csv --limit 5

import csv
import time
import argparse
import logging
# import pprint
from data_table import DataTable

def chapter(title):
    number_of_title_dashes = (132 - len(title)) // 2
    title_dashes = "-" * number_of_title_dashes
    # logging.info("-" * 132)
    logging.info(title_dashes + title + title_dashes)
    # logging.info("-" * 132)
    return

def configure():
    parser = argparse.ArgumentParser(description='Morph Excel-csv into Prestashop-products-csv.')
    parser.add_argument('--inputfile', required=True, help='input file')
    parser.add_argument('--limit', required=True, help='number of records to process (0 processes them all)')
    args = parser.parse_args()
    configuration = {}
    configuration['limit']          = int(args.limit)
    configuration['inputfile']      = args.inputfile
    configuration['stamp']          = time.strftime("%Y%m%d-%H%M%S")
    configuration['outputfile']     = 'data/output/generated-ProductsForPrestaShop-' + configuration['stamp'] + '.csv'
    configuration['imglocation']    = 'https://www.dimarco.be/testshop/img/dimarco/'
    configuration['taxid']          = '666'
    configuration['fixed-active']   = '1'
    configuration['featurelist']    = ('Type', 'Land', 'Regio')
    configuration['categorieslist'] = ('cat1', 'cat2')
    configuration['fieldmap'] = {
            'generated-id': "PRODUCT-ID",
            'Code': "REFERENCE",
            'Wijn': "NAME",
            ' Prijs/fles ': "PRICE-INC",
            'Beschrijving': "LONG-DESC",
            'combined-features': "FEATURES",
            'combined-categories': "CATEGORIES",
            'fixed-aantal': "STOCK",
            'fixed-active': "ACTIVE",
            'fixed-taxid': "TAX-ID",
            'generated-img-url': "IMG-URL",
            'generated-beschrijving-kort': "SHORT-DESC"
        }
    return configuration

def main():

    logging.basicConfig(level=logging.INFO)
    logging.info('=== NORMAL START ===' + '=' * 111)

    chapter(f"Process arguments - configure")
    conf = configure()
    # pprint.pprint(conf, sort_dicts=False, width=132, indent=10, depth=1)

    # First - read the CSV files into a csv-table
    dimarco_data = DataTable(displayfield='Code')
    chapter(f"Load Di Marco csv [{conf['inputfile']}]")
    dimarco_data.load_csv(conf['inputfile'], conf['limit'])
    dimarco_data.show_fields(('Code', 'Wijn'))

    # # Then - we add some fields
    # chapter(f"Add some working fields")

    # # Then - we correct some errors in Griets data - I'd rather do it here than in the excel - because I sometimes get new ones
    # chapter(f"Correct Di Marco csv data")
    # dimarco_corrections.append(['Fotos', 'Borduurpakket 029', 'Omschrijving', 'tuinshort', 'tuinshort bloemen en gieters'])

    # # Then - we filter out records that we do not need
    # chapter(f"Remove unwanted records")
    # # mergedkeydict = remove_records_where(mergedkeydict, {'Categorie1': 'Verkocht', 'Categorie2': 'Verkocht'})

    # # Then - we add some extra fields
    chapter(f"Add some extra fields")
    dimarco_data.add_counter_field('generated-id', initialvalue=10001)
    dimarco_data.add_fixed_field('fixed-taxid', conf['taxid'])
    dimarco_data.add_fixed_field('fixed-active', '1')
    dimarco_data.add_fixed_field('fixed-aantal', '1000')
    dimarco_data.copy_field(sourcefield='Code', newfield='generated-img-url', prefix=conf['imglocation'], suffix='.jpg')
    dimarco_data.copy_field(sourcefield='Beschrijving', newfield='generated-beschrijving-kort')
    dimarco_data.show_fields(('Code', 'Wijn', 'fixed-taxid', 'fixed-active', 'generated-img-url'))

    # # Then - we correct some possible shizzle (extra spaces, title-ize product name)
    # chapter(f"Correct some possible shizzle (extra spaces, title-ize product name)")
    # mergedkeydict = correct_some_shizzle(mergedkeydict, ('Prijs', 'Merk', 'Omschrijving', 'Artikelnr', 'Aantal'))

    # # Then - we replace some shizzle - image url..
    # chapter(f"Replace some shizzle")
    # dimarco_data.replace_in_field('Imgurl', config['testproductimglocation'], config['realproductimglocation'])

    # # Then - we replace the empty value for the specified field
    # chapter(f"Replace empty values")
    # dimarco_data.fill_empty_field('Inhoud', 'DMC zesdraad')

    # # Then - we generate the short and long description
    # chapter(f"Generate the (short) description")
    # mergedkeydict = add_combined_description_field(mergedkeydict, 'AddedDescriptionShort', {'Omschrijving': 'Handwerkpakket', 'Ontwerper': 'Ontwerp', 'Leeftijd': 'Leeftijd', 'Onderwerp': 'Onderwerp', 'Inhoud': 'Inhoud', 'Artikelnr': 'Artikelnr'})

    # # Then - we process missing image url...
    # chapter(f"Process missing image url")
    # process_missing_images(mergedkeydict, config['altimagesdirectory'], config['realproductimglocation'], 'Imgurl')

    # # Then - we generate a complex combined feature field from the fields describing a feature
    chapter(f"Generate complex combined feature field from the feature fields")
    dimarco_data.add_combined_features_field('combined-features', conf['featurelist'])
    dimarco_data.show_fields(('Code', 'Wijn', 'combined-features'))

    # # Then - we combine the category fields into one category (list)field
    chapter(f"Combine the category fields into one category (list)field")
    # dimarco_data.add_fixed_field('fixed-cat1', 'category1')
    # dimarco_data.add_fixed_field('fixed-cat2', 'category2')
    dimarco_data.add_combined_categories_field('combined-categories', conf['categorieslist'])
    dimarco_data.show_fields(('Code', 'Wijn', 'combined-categories'))

    chapter(f"Re-map field for Prestashop")
    prestashop_table = dimarco_data.re_map_table(conf['fieldmap'], displayfield='REFERENCE')

    chapter(f"Some tests - output to screen")
    # dimarco_data.show_fields(('generated-id', 'Code', 'Wijn', 'Type', 'Land', 'Regio'))
    # prestashop_table.show_fields(('PRODUCT-ID', 'REFERENCE', 'NAME', 'FEATURES'))

    chapter(f"Generate resulting csv")
    # logging.info(f'====================================== BEGIN RESULTING CSV ======================================')
    # resultcsv = prestashop_table.generate_csv_array(delimiter='||')
    # logging.info(f'======================================= END RESULTING CSV =======================================')
    # print(resultcsv)

    # # Finally we write the resulting products csv file
    chapter(f"Writing resulting csv - [{conf['outputfile']}]")
    prestashop_table.write_csv(conf['outputfile'], delimiter=';')
    logging.info('=== NORMAL END ===' + '=' * 113)

    exit(0)


if __name__ == '__main__':
    main()
