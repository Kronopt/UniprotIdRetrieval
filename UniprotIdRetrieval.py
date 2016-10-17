#!/usr/bin/env python
# coding: utf-8

"""
UNIPROT ID RETRIEVAL
Retrieves valid Uniprot ids from text files (basically any file that can be opened
by a text editor) and retrieves, from Uniprot, each respective sequence in the desired
output format

DEPENDENCIES:
    - Python 2.7
    - requests library (type 'pip install requests' on the command line to install)

HOW TO RUN:
    Through the command line.
    For help call the script with the -h parameter
"""

import argparse
import re
import requests

__author__ = 'Pedro HC David, https://github.com/Kronopt'
__credits__ = ['Pedro HC David']
__version__ = '0.2'
__date__ = '19:00, 17/10/2016'
__status__ = 'Production'


def extract_uniprot_ids(file_name):
    """
    Identifies valid uniprot accession numbers using a regular expression defined on the
    uniprot website

    PARAMETERS:
        file_name : str
            Represents a path/file name of the file to parse

    REQUIRES:
        File must be a plain text type of file (no extension, .txt, .csv, .tab, etc)

    ENSURES:
        Set with the indentified uniprot accession numbers
    """

    # http://www.uniprot.org/help/accession_numbers
    uniprot_regex = re.compile(
        "[A-NR-Z][0-9][A-Z][A-Z0-9]{2}[0-9][A-Z][A-Z0-9]{2}[0-9]"
        + "|[A-NR-Z][0-9][A-Z][A-Z0-9]{2}[0-9]|[OPQ][0-9][A-Z0-9]{3}[0-9]"
    )

    uniprot_ids = []

    try:
        with open(file_name, "rb") as file_with_ids:
            for line in file_with_ids:
                uniprot_ids.extend(uniprot_regex.findall(line))

            # Uniprot ids can only be 6 or 10 characters in size
            uniprot_ids = filter(lambda x: len(x) in [6, 10], uniprot_ids)

    except IOError, e:
        print 'Error with "' + e.filename + '" file:'
        print e.strerror

    finally:
        return set(uniprot_ids)


def retrieve_sequences(ids_, output_format):
    """
    Retrieves a sequence file for each id in the desired output format

    PARAMETERS:
        ids_ : set / list
            Represents a group of unique valid uniprot ids
        output_format : str
            Represents an output format

    REQUIRES:
        - ids_ complying with uniprot standards for ids
        - Valid output_format

    ENSURES:
        Fetching of each sequence file (on the desired output format) for each id
    """

    print '\n' + output_format.upper() + ' sequences'

    for i in sorted(ids_):
        print i + ':',

        resource = i + '.' + output_format

        # Uniprot webservice
        sequence_file = requests.get('http://www.uniprot.org/uniprot/' + resource)

        # If response is empty
        if len(sequence_file.text) == 0:
            print 'not available in .' + output_format + ' or does not exist'
            continue

        # If response is html, then it's invalid
        html = False
        for line in sequence_file.iter_lines():
            if '<!DOCTYPE html' in line:
                print 'not available in .' + output_format + ' or does not exist'
                html = True
            break

        if html:
            continue

        with open(resource, "wb") as file_name:
            [file_name.write(line + '\n') for line in sequence_file.iter_lines()]

        print 'ok'

if __name__ == '__main__':
    parser = argparse.ArgumentParser(description='Uniprot id retrieval tool')

    parser.add_argument('file', metavar='file', help='File path or name')
    parser.add_argument('format', choices=['txt', 'xml', 'fasta', 'rdf', 'gff', 'tab'],
                        help='Output format')

    parser = parser.parse_args()

    ids = extract_uniprot_ids(parser.file)
    retrieve_sequences(ids, parser.format)
