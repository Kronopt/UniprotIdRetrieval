# UniprotIdRetrieval
Downloads protein sequences from Uniprot, in the desired output format, based on the given ids (either passed as arguments or identified in a file)

#### Dependencies
* Python 2.7
* Module dependencies (run `pip install -r requirements.txt` to install):
  * requests

#### How to run
Runs through the command line, like so:

`UniprotIdRetrieval.py [-h] (-f <file> | -i <id ...>) [-fo {fasta, gff, tab, txt, rdf, xml}]`

* `-h, --help` shows the help text
* `-f, --file` takes a file path to search for ids
* `-i, --ids` takes 1 or more ids
* `-fo, --format` defines the output format of downloaded files (fasta, gff, tab, txt, rdf or xml), defaults to 'fasta'