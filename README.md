# UniprotIdRetrieval
Finds valid Uniprot ids in text files and retrieves each respective sequence in the desired output format from Uniprot

#### Dependencies
* Python 2.7
* Module dependencies (can be installed by running `install_dependencies.py`):
  * requests

#### How to run
Runs through the command line, like so:

`UniprotIdRetrieval.py file [-f] [-h]`
	
* `file` is the name of the file to search for IDs (only required argument)
* `-f, --format` is the format of the output file (one of: txt, xml, fasta, rdf, gff or tab), defaults to 'fasta'
* `-h, --help` shows the help text
