#!/usr/bin/env python
# coding: utf-8

'''
UNIPROT ID RETRIEVAL
Retrieves valid Uniprot ids from text files (basically any file that can be opened
by a text editor) and retrieves, from Uniprot, each respective sequence with the desired
output format

DEPENDENCIES:
    - Python 2.7
    - requests library (type 'pip install requests' on the command line to install)

HOW TO RUN:
    Through the command line.
    For help call the script with the -h parameter
'''

import argparse
import re
import requests

__author__ = 'Pedro HC David, https://github.com/Kronopt'
__credits__ = ['Pedro HC David']
__version__ = '0.2'
__date__ = '15:58h, 22/06/2016'
__status__ = 'Production'

def extractUniprotIds(fileName):
    '''
    Identifies valid uniprot accession numbers using a regular expression defined on the
    uniprot website

    PARAMETERS:
        fileName : str
            Represents a path/file name of the file to parse

    REQUIRES:
        File must be a plain text type of file (no extension, .txt, .csv, .tab, etc)

    ENSURES:
        Set with the indentified uniprot accession numbers
    '''

    # http://www.uniprot.org/help/accession_numbers
    uniprotRegex = re.compile("[A-NR-Z][0-9][A-Z][A-Z0-9]{2}[0-9][A-Z][A-Z0-9]{2}[0-9]"
                              + "|[A-NR-Z][0-9][A-Z][A-Z0-9]{2}[0-9]|[OPQ][0-9][A-Z0-9]{3}[0-9]")
    
    uniprotIds = []

    try:
        with open(fileName, "rb") as fileWithIds:
            for line in fileWithIds:
                uniprotIds.extend(uniprotRegex.findall(line))

            # Uniprot ids can only be 6 or 10 characters in size
            uniprotIds = filter(lambda x: len(x) in [6, 10], uniprotIds)
        
    except IOError, e:
        print 'Error with "' + e.filename + '" file:'
        print e.strerror

    finally:
        return set(uniprotIds)

def retrieveSequences(ids, outputFormat):
    '''
    Retrieves a sequence file for each id in the desired output format

    PARAMETERS:
        ids : set / list
            Represents a group of unique valid uniprot ids
        outputFormat : str
            Represents an output format

    REQUIRES:
        - Ids complying with uniprot ids' standards
        - Valid outputFormat

    ENSURES:
        Fetching of each sequence file (on the desired output format) for each id
    '''

    for i in ids:
        resource = i + '.' + outputFormat
        
        # Uniprot webservice
        sequenceFile = requests.get('http://www.uniprot.org/uniprot/' + resource)

        # If response is empty
        if len(sequenceFile.text) == 0:
            print 'WARNING: ' + i + ' is not available in the designated output format or ' \
                  + 'does not exist'
            continue

        # If response is html, then it's invalid
        html = False
        for line in sequenceFile.iter_lines():
            if '<!DOCTYPE html' in line:
                print 'WARNING: ' + i + ' is not available in the designated output format or ' \
                      + 'does not exist'
                html = True
            break

        if html:
            continue

        with open(resource, "wb") as fileName:
            [fileName.write(line + '\n') for line in sequenceFile.iter_lines()]

if __name__ == '__main__':
    parser = argparse.ArgumentParser(description = 'Uniprot id retrieval tool')

    parser.add_argument('file', metavar = 'file', help = 'File path or name')
    parser.add_argument('format', choices = ['txt', 'xml', 'fasta', 'rdf', 'gff', 'tab'],
                        help = 'Output format ()')

    parser = parser.parse_args()

    ids = extractUniprotIds(parser.file)
    retrieveSequences(ids, parser.format)
