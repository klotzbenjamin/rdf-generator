# RDF generator
The goal of this repository is to provide an easy way of generating triples from JSON/CSV sources and extend an extisting RDF triplestore.
The input must be a CSV/JSON file, as well as a pickle file for the mapping of the variables to find in the CDV/JSON file, and an ontological scheme of tose variables, in RDF.

## Installation
You will need to install RDFlib in order to use this code.

## Usage
### General example
This repository contains examples of input files, graph, mappings and a scheme.
'python rdf-generator.py -i input/input-flat.json -m mapping/mapping-flat.pkl -s scheme/SOSA-scheme.ttl'

This order will use data from input/input-flat.json to feed a scheme scheme/SOSA-scheme.ttl, mapped with mapping/mapping-flat.pkl.

### Arguments
-i: Input raw data. Currently it must be a CSV or JSON file.
-m: Mapping file, serialized in pickle. This contains a python dictionary mapping the variables present in the scheme with a path to access the values in the raw data file
-s: Ontological scheme file, serialized in turtle, containing triples of variables (written :var1, :var2...) and static constants (written: cst1, :cst2...)
-g: (Optional) Input graph to extend. CUrrently it must be serialized in turtle.
-o: (Optional) Output file to create. It will be serialized in turtle.

### Available examples
This repository contains 3 input files:
* input-flat.csv
* input-flat.json
* input-complex.json

They all contain the same information, an observation of car sensors.

We use here the VSSo ontology to model car signals, and the SOSA pattern. The Scheme will be a SOSA observation and its neighbours regardless of the format of the raw data.

We need a mapping between raw data and the variable in the scheme. We have 2 mappings here:
* mapping-flat.pkl: for both input-flat files
*mapping-complex.pkl: for input-complex.json
