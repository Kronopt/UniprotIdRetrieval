#!python2
# coding: utf-8

"""
UNIPROT ID RETRIEVAL
Downloads protein sequences from Uniprot, in the desired output format, based on the given ids (either passed as
arguments or identified in a file)

DEPENDENCIES:
    - Python 2.7
    - requests

HOW TO RUN:
    Through the command line:

    UniprotIdRetrieval.py [-h] (-f <file> | -i <id ...>) [-fo {fasta, gff, tab, txt, rdf, xml}]

    - '-h, --help' shows the help text
    - '-f, --file' takes a file path to search for ids
    - '-i, --ids' takes 1 or more ids
    - '-fo, --format' defines the output format of downloaded files (fasta, gff, tab, txt, rdf or xml),
      defaults to 'fasta'
"""

import argparse
import re
import requests
import time

__author__ = 'Pedro HC David, https://github.com/Kronopt'
__credits__ = ['Pedro HC David']
__version__ = '2.0'
__status__ = 'Finished'


# http://www.uniprot.org/help/accession_numbers
UNIPROTREGEX = ("[A-NR-Z][0-9][A-Z][A-Z0-9]{2}[0-9][A-Z][A-Z0-9]{2}[0-9]"
                + "|[A-NR-Z][0-9][A-Z][A-Z0-9]{2}[0-9]|[OPQ][0-9][A-Z0-9]{3}[0-9]")


def extract_uniprot_ids(file_name):
    """
    Identifies valid uniprot accession numbers using a regular expression defined on the uniprot website

    Parameters
    ----------
    file_name: str
        Path/file name of the file to parse

    Returns
    -------
    Set with the indentified uniprot accession numbers
    """
    uniprot_regex = re.compile(UNIPROTREGEX)
    uniprot_ids = []

    try:
        with open(file_name, "rb") as file_with_ids:
            for line in file_with_ids:
                uniprot_ids.extend(uniprot_regex.findall(line))

            # Uniprot ids can only be 6 or 10 characters in size
            uniprot_ids = filter(lambda x: len(x) in [6, 10], uniprot_ids)

    except IOError, e:
        print 'Error with "' + e.filename + '" file: ' + e.strerror

    finally:
        return set(uniprot_ids)


def retrieve_sequences(ids_, output_format):
    """
    Searches for a protein sequence for each id and downloads it (if found) in the desired output format

    Parameters
    ----------
        ids_: set / list
            Uniprot ids
        output_format: str
            Output format

    Returns
    -------
        Fetching of each protein sequence file (on the desired output format) for each id
    """
    if len(ids_) > 0:
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

            # http not 200
            elif sequence_file.status_code != 200:
                print('http error ' + str(sequence_file.status_code))

            # If response is html, then it's invalid
            else:
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
            time.sleep(0.33)  # follow max of 3 requests per second rule of Uniprot


if __name__ == '__main__':
    parser = argparse.ArgumentParser(description='Uniprot id retrieval tool. Searches Uniprot for protein sequences and'
                                                 ' downloads them. Either uses the ids passed as arguments (-i, --ids) '
                                                 'OR ids found in a file (-f, --file)')

    file_or_ids = parser.add_mutually_exclusive_group(required=True)
    file_or_ids.add_argument('-f', '--file', metavar='<file>', help='file path')
    file_or_ids.add_argument('-i', '--ids', nargs='+', metavar='<id>', help='uniprot ids')

    parser.add_argument('-fo', '--format',
                        choices=['fasta', 'gff', 'tab', 'txt', 'rdf', 'xml'],
                        default='fasta',
                        help='output format (defaults to fasta)')

    parser = parser.parse_args()

    if parser.ids is None:
        ids = extract_uniprot_ids(parser.file)
        retrieve_sequences(ids, parser.format)
    else:
        retrieve_sequences(set(parser.ids), parser.format)
