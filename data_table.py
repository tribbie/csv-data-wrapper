## A data wrapper class around a data dictionary from a csv kind of datafile
## Version 0.1

import os
import csv
import logging

class DataTable:

    def __init__(self, displayfield='id'):
        self.displayfield = displayfield
        self.fields = []
        self.records = []

    def load_csv(self, filename, fielddelimiter='|', limit = 0):
        logging.info(f"=== Loading CSV from [{filename}]")
        header = []
        csv_dict = {}
        try:
            rowcount = 1
            with open(filename, "r") as csvfile:
                csvreader = csv.DictReader(csvfile, delimiter=fielddelimiter, quotechar='"')
                self.fields = csvreader.fieldnames
                logging.info(f"HEADERLINE = {self.fields}")
                for row in csvreader:
                    self.records.append(row)
                    logging.debug(f" -> line [{csvreader.line_num}] -- [{row}]")
                    if limit > 0 and rowcount >= limit:
                        break
                    else:
                        rowcount += 1
        except FileNotFoundError:
            logging.error(f"ERROR - dude, file [{filename}] was not found")
        logging.info(f"RECORDS ===> [{rowcount}] data lines read from [{filename}]")
        return

    def show_fields(self, fieldnames=None):
        if fieldnames == None:
            fieldnames = self.fields
        logging.info(f"=== Showing fields {fieldnames}")
        logging.info(f" [HEADER]--[{']-['.join(fieldnames)}]")
        rowcount = 0
        for row in self.records:
            rowcount = rowcount + 1
            logging.debug(row)
            fieldvalues = []
            for fieldname in fieldnames:
                if fieldname in row:
                    fieldvalues.append(row[fieldname].strip())
                else:
                    fieldvalues.append('<' + fieldname.upper() + '>')
            logging.info(f" [#{str(rowcount)}]--[{']-['.join(fieldvalues)}]")
        return

    def show_record(self, id):
        logging.info(f"=== Showing record {id}")
        fieldnames = self.fields
        for record in self.records:
            if record[self.displayfield] == id:
                logging.debug(record)
                for fieldname in fieldnames:
                    logging.info(f" [{fieldname}]=[{record[fieldname]}]")
        return

    def remove_records(self, removedict):
        logging.info(f"=== Removing records where {removedict}")
        removefieldnames = removedict.keys()
        if len(removefieldnames) == 0:
            logging.warning(f" WARNING - no remove filter specified - not removing anything")
            return
        for removefieldname in removefieldnames:
            if removefieldname in self.fields:
                # logging.info(f" OK - remove field {removefieldname} exist")
                pass
            else:
                logging.error(f" ERROR - remove field {removefieldname} does not exist - not removing anything")
                return
        retainedrecords = []
        for row in self.records:
            logging.debug(row)
            # matchvalues = []
            matchcount = 0
            for fieldname in removefieldnames:
                # matchvalues.append(row[fieldname])
                if removedict[fieldname] == row[fieldname]:
                    matchcount += 1
            if matchcount == len(removefieldnames):
                logging.info(f" Exact match found for record [{row[self.displayfield]}] -- will be removed")
            else:
                # logging.info(f" Retaining [{row[self.displayfield]}]")
                retainedrecords.append(row)
            self.records = retainedrecords
        return

    def check_unique_field(self, fieldname):
        uniqueness = 0
        logging.info(f"=== Checking uniqueness of field [{fieldname}]")
        if fieldname not in self.fields:
            logging.error(f"ERROR - ERROR - field [{fieldname}] not found exists - NOT CHECKING UNIQUENESS!!")
        else:
            uniqueDict = {}
            for record in self.records:
                logging.debug(f"-- checking [{record[fieldname]}] to uniqueness check")
                uniqueDict[record[fieldname]] = ''
        if (len(self.records) == len(uniqueDict)):
            logging.info(f" Field [{fieldname}] -- appears to be unique")
            uniqueness = 1
        else:
            logging.warning(f" WARNING - Field [{fieldname}] -- is not unique")
        return uniqueness

    def add_fixed_field(self, newfield, value):
        logging.info(f"=== Adding fixed field [{newfield}] - with value [{value}]")
        if newfield in self.fields:
            logging.error(f"ERROR - ERROR - field [{newfield}] already exists - NOT ADDING FIELD!!")
        else:
            self.fields.append(newfield)
            for record in self.records:
                logging.debug(f"-- adding [{record[self.displayfield]}] - [{newfield}]=[{value}]")
                record[newfield] = str(value)
        return

    def add_counter_field(self, newfield, initialvalue):
        logging.info(f"=== Adding counter field [{newfield}] - starting at {initialvalue}")
        if newfield in self.fields:
            logging.error(f"ERROR - ERROR - field [{newfield}] already exists - NOT ADDING FIELD!!")
        else:
            self.fields.append(newfield)
            countervalue = initialvalue
            for record in self.records:
                logging.debug(f"-- adding to [{record[self.displayfield]}] - [{newfield}]=[{countervalue}]")
                record[newfield] = str(countervalue)
                countervalue += 1
        return

    def add_combined_field(self, newfield, fieldstocombine, delimiter=''):
        logging.info(f"=== Adding combined field [{newfield}] - combining {fieldstocombine}")
        if newfield in self.fields:
            logging.error(f"ERROR - ERROR - field [{newfield}] already exists - NOT ADDING FIELD!!")
        else:
            self.fields.append(newfield)
            for record in self.records:
                combinedfields = []
                for field in fieldstocombine:
                    if field in record.keys():
                        if record[field].strip() == '':
                            logging.warning(f"WARNING - WARNING - skipping empty field [{field}]")
                        else:
                            combinedfields.append(record[field].strip())
                    else:
                        logging.error(f"ERROR - ERROR - field [{field}] not found in this record - CANNOT COMBINE!!")
                record[newfield] = delimiter.join(combinedfields)
                logging.debug(f"-- adding to [{record[self.displayfield]}] - [{newfield}]=[{record[newfield]}]")
        return

    def add_combined_features_field(self, newfield, featurefields):
        logging.info(f"=== Adding combined features field [{newfield}] - combining {featurefields}")
        if newfield in self.fields:
            logging.error(f"ERROR - ERROR - field [{newfield}] already exists - NOT ADDING FIELD!!")
        else:
            self.fields.append(newfield)
            for record in self.records:
                combinedfeatures = ''
                for featurefield in featurefields:
                    if featurefield in record.keys():
                        # Moeilijkheid:gemakkelijk:1:1
                        combinedfeatures += featurefield + ':' + record[featurefield].strip().capitalize().replace(",", ".") + ':1:0,'
                    else:
                        logging.error(f"ERROR - ERROR - feature field [{featurefield}] not found in this record - CANNOT COMBINE!!")
                record[newfield] = combinedfeatures.strip(',')
                logging.debug(f"-- adding to [{record[self.displayfield]}] - [{newfield}]=[{record[newfield]}]")
        return

    def add_combined_categories_field(self, newfield, categoryfields):
        logging.info(f"=== Adding combined categories field [{newfield}] - combining {categoryfields}")
        if newfield in self.fields:
            logging.error(f"ERROR - ERROR - field [{newfield}] already exists - NOT ADDING FIELD!!")
        else:
            self.fields.append(newfield)
            for record in self.records:
                combinedcategories = ''
                for categoryfield in categoryfields:
                    if categoryfield in record.keys():
                        combinedcategories += ',' + record[categoryfield].strip().replace("/", "!")
                    else:
                        logging.error(f"ERROR - ERROR - category field [{categoryfield}] not found in this record - CANNOT COMBINE!!")
                record[newfield] = combinedcategories.strip(',')
                logging.debug(f"-- adding to [{record[self.displayfield]}] - [{newfield}]=[{record[newfield]}]")
        return

    def copy_field(self, sourcefield, newfield, prefix='', suffix=''):
        logging.info(f"=== Copying [{sourcefield}] into [{newfield}] with prefix=[{prefix}] and suffix=[{suffix}]")
        if newfield in self.fields:
            logging.error(f"ERROR - ERROR - field [{newfield}] already exists - NOT ADDING FIELD!!")
        else:
            self.fields.append(newfield)
            for record in self.records:
                if sourcefield in record:
                    record[newfield] = prefix + record[sourcefield] + suffix
                    logging.debug(f"-- adding to [{record[self.displayfield]}] -> copied [{record[sourcefield]}] to [{record[newfield]}]")
                else:
                    record[newfield] = ""
                    logging.debug(f"-- WARNING - WARNING - No [{sourcefield}] found for [{record[self.displayfield]}] -- adding empty field")
        return

    def add_existing_image_field(self, basefield, newfield, checklocation='./', outputlocation='https://domain.org/images/', suffix='.jpg'):
        logging.info(f"=== Adding existing images based on [{basefield}] into [{newfield}] with location=[{checklocation}] and suffix=[{suffix}]")
        if newfield in self.fields:
            logging.error(f"ERROR - ERROR - field [{newfield}] already exists - NOT ADDING FILE-EXISTS FIELD!!")
            return
        if not basefield in self.fields:
            logging.error(f"ERROR - ERROR - base field [{basefield}] does not exists - NOT ADDING FILE-EXISTS FIELD!!")
            return
        self.fields.append(newfield)
        for record in self.records:
            imagetocheck = checklocation + record[basefield] + suffix
            imagetoadd = outputlocation + record[basefield] + suffix
            if os.path.isfile(imagetocheck):
                logging.info(f"-- Image [{imagetocheck}] found for [{record[self.displayfield]}] -> added [{imagetoadd}]")
                record[newfield] = imagetoadd
            else:
                logging.info(f"-- WARNING - WARNING - Image [{imagetocheck}] not found for [{record[self.displayfield]}] -- adding empty field")
                record[newfield] = ""
        return

    def replace_in_field(self, field, frompart, topart):
        logging.info(f"=== Replacing [{frompart}] into [{topart}] in field [{field}]")
        if field in self.fields:
            for record in self.records:
                record[field] = record[field].replace(frompart, topart)
                logging.debug(f"-- after replacement in [{record[self.displayfield]}]: [{field}]=[{record[field]}]")
        else:
            logging.error(f"ERROR - ERROR - field [{field}] does not exists - NOT REPLACING IN FIELD!!")
        return

    def re_map_table(self, fieldmap, displayfield='id'):
        logging.info(f"=== Re-mapping the records for Prestashop import")
        remapped_table = DataTable(displayfield=displayfield)
        remapped_fieldlist = []
        for field in fieldmap.values():
            remapped_fieldlist.append(field)
        remapped_table.fields = remapped_fieldlist
        for record in self.records:
            remapped_record = {}
            for key in fieldmap.keys():
                mapped_key = fieldmap[key]
                if key in record:
                    remapped_record[mapped_key] = record[key].strip()
                else:
                    remapped_record[mapped_key] = "[__" + key.strip().upper() + "__]"
            remapped_table.records.append(remapped_record)
        return(remapped_table)

    def generate_csv_array(self, fieldnames=None, delimiter=';'):
        logging.info(f"=== Generating csv array")
        if fieldnames == None:
            fieldnames = self.fields
        csvlist = []
        headerline = delimiter.join(fieldnames)
        csvlist.append(headerline)
        logging.debug(f"{headerline}")
        for record in self.records:
            values = []
            for fieldname in fieldnames:
                if fieldname in record.keys():
                    values.append(record[fieldname].strip())
                else:
                    values.append('')
            valuesline = delimiter.join(values)
            logging.debug(valuesline)
            csvlist.append(valuesline)
        return(csvlist)

    def write_csv(self, filename, delimiter=';'):
        logging.info(f"=== Writing csv file into [{filename}]")
        headerline = delimiter.join(self.fields)
        file = open(filename, "w")
        file.write("%s\n" % headerline)
        for record in self.records:
            valuesline = delimiter.join(record.values())
            file.write("%s\n" % valuesline)
        file.close()
        return


if __name__ == '__main__':
    print("This is a python object - do not run me")
