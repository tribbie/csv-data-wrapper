# csv-data-wrapper
A csv data wrapper class

## features

This is a python class to fiddle with csv files.

It was developed to be able to transform a spreadsheet into a importable csv file for PrestaShop.

When receiving a product spreadsheet from someone, it can contains errors:
- blanks where they should not be
- delimiter characters in some text field
- inconsistent capitalization
- ...

Also, when importing product data in PrestaShop, you will need specially crafted fields for:
- Categories
- Features

This is the process:
- save the spreadsheet as (input) csv
- run a script that uses this csv data wrapper (eg. test-data-wrapper.py)
  - to read the input csv file
  - process all you need to process
  - write the output csv file
- import the newly generated (output) csv into PrestaShop

It can:
- read a csv file
- show fields (like a very basic sql select statement)
- show an individual record
- add fixed fields
- add counter field
- add combined field
- copy a field
- replace in field
- map data to a new structure
- write a csv file
